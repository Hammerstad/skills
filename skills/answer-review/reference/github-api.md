# GitHub API mechanics for answer-review

All commands use the authenticated `gh` CLI. `<owner>/<repo>` comes from
`gh repo view --json nameWithOwner -q .nameWithOwner` (or the PR URL).

## What needs answering

### Unresolved inline threads (GraphQL)

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
            comments(first: 50) {
              nodes { author { login } body createdAt }
            }
          }
        }
      }
    }
  }' -f owner=<owner> -f repo=<repo> -F pr=<n>
```

Keep nodes where `isResolved` is false **and** the last comment's author is not
us (`gh api user -q .login` gives our login). Page via `after: $cursor` if
`hasNextPage`.

### Review bodies and PR comments (REST)

```sh
gh api repos/<owner>/<repo>/pulls/<n>/reviews \
  --jq '.[] | select(.body != "") | {author: .user.login, state, body}'

gh api repos/<owner>/<repo>/issues/<n>/comments \
  --jq '.[] | {author: .user.login, body}'
```

From these, collect concrete points that are not already covered by an inline
thread. Ignore bot boilerplate and our own comments.

## Responding

### Reply to an inline thread (GraphQL)

```sh
gh api graphql -f query='
  mutation($thread: ID!, $body: String!) {
    addPullRequestReviewThreadReply(
      input: { pullRequestReviewThreadId: $thread, body: $body }
    ) { comment { id } }
  }' -f thread=<threadId> -f body='Fixed in `a1b2c3d`.'
```

Do **not** call `resolveReviewThread` — resolution belongs to the reviewer.

### Quote-reply comment for non-inline points (only when they exist)

```sh
gh pr comment <n> --body-file response.md
```

`response.md` shape — one quoted point, one response, repeated:

```markdown
> The migration in this PR isn't referenced from the changelog.

Added in `d4e5f6a`.

> Consider batching these writes.

The writes are already coalesced by the outbox worker (`OutboxWorker.Flush`),
so batching here would double-buffer. Leaving as is.
```

## Commit SHAs in replies

Cite the short SHA (`git rev-parse --short HEAD` after each fix commit, or
collect from `git log --oneline` before pushing). Push **before** posting any
reply so every cited SHA resolves on GitHub.
