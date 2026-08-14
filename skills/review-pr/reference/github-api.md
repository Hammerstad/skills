# GitHub API mechanics for review-pr

All commands use the authenticated `gh` CLI. `<owner>/<repo>` comes from
`gh repo view --json nameWithOwner -q .nameWithOwner` (or the PR URL).

## Fetch existing review threads (GraphQL)

```sh
gh api graphql -f query='
  query($owner: String!, $repo: String!, $pr: Int!) {
    repository(owner: $owner, name: $repo) {
      pullRequest(number: $pr) {
        reviewThreads(first: 100) {
          pageInfo { hasNextPage endCursor }
          nodes {
            id
            isResolved
            isOutdated
            path
            line
            comments(first: 20) {
              nodes { author { login } body }
            }
          }
        }
      }
    }
  }' -f owner=<owner> -f repo=<repo> -F pr=<n>
```

If `hasNextPage` is true, page with `reviewThreads(first: 100, after: $cursor)`.
The `id` on each node is the thread id used for replying and resolving.

## Submit the review (REST, one call)

Write the payload to a temp file, then:

```sh
gh api repos/<owner>/<repo>/pulls/<n>/reviews --input payload.json
```

`payload.json`:

```json
{
  "commit_id": "<headRefOid>",
  "event": "COMMENT",
  "body": "PR-wide findings go here; empty string if none",
  "comments": [
    {
      "path": "src/file.ts",
      "line": 42,
      "side": "RIGHT",
      "body": "Finding text. Optionally a ```suggestion block."
    },
    {
      "path": "src/other.ts",
      "start_line": 10,
      "start_side": "RIGHT",
      "line": 14,
      "side": "RIGHT",
      "body": "Multi-line comment covering lines 10-14."
    }
  ]
}
```

Rules:

- `event` is `COMMENT` or `APPROVE` (this skill never sends `REQUEST_CHANGES`).
- For `APPROVE` with no findings, omit `comments` and send an empty `body`.
- `line`/`side: "RIGHT"` = line numbers in the **new** file version; use
  `side: "LEFT"` only to comment on deleted lines. Lines must appear in the
  diff, or GitHub rejects the comment — findings on undiffed lines belong in
  `body`.
- Approving your own PR fails with HTTP 422 — catch it and fall back to
  reporting "clean" in the terminal.

## Reply to a thread, then resolve it (GraphQL)

```sh
gh api graphql -f query='
  mutation($thread: ID!, $body: String!) {
    addPullRequestReviewThreadReply(
      input: { pullRequestReviewThreadId: $thread, body: $body }
    ) { comment { id } }
  }' -f thread=<threadId> -f body="Addressed in abc123."

gh api graphql -f query='
  mutation($thread: ID!) {
    resolveReviewThread(input: { threadId: $thread }) {
      thread { isResolved }
    }
  }' -f thread=<threadId>
```

Reply first, then resolve, so the reasoning lands inside the thread before it
collapses.
