---
name: review-pr
description: Review a GitHub pull request with inline comments posted on the PR itself. Use when the user says "review PR 98", "/review-pr 98", "review this pull request", or pastes a PR URL for review. Comments inline on exact file/lines, puts PR-wide findings in the review body, resolves addressed comment chains, approves when clean.
---

# Review PR

Review a pull request and deliver the findings **on GitHub itself** — inline, on the exact file and line — never as a chat summary or a PR summary comment.

## Contract

- **Inline first.** Every finding that maps to a changed file/line becomes an inline review comment there. Findings that cannot be attributed to a diff line (stale comments in untouched files, a rename that makes docs elsewhere wrong, missing migration, etc.) go in the **review body**. If there are none, the body stays empty.
- **No praise, no filler.** Only comment where there is a genuine improvement. If a file is good, it gets nothing. If the whole PR is good, it gets zero comments — do not invent findings to look busy.
- **Full scope.** Correctness, edge cases, security, design, tests — and also style, naming, and idiom-consistency issues when they are real improvements. Prefix minor/taste-level findings with `nit:` so the author can triage.
- **One review submission.** All inline comments and the body are submitted as a single review (single notification). Never post a separate summary comment.
- **Verdict:** zero new findings and no still-valid open threads → submit as `APPROVE`. Otherwise → submit as `COMMENT`. Never `REQUEST_CHANGES`.
- **Close settled threads.** For each existing unresolved review thread whose concern is now addressed or moot: post a short reply stating why (e.g. "Addressed in `a1b2c3d`."), then resolve it — regardless of who opened it. Threads that still have merit stay open and count as findings for the verdict.

## Workflow

### 1. Gather

Parse the PR number from the argument (`98`, `#98`, or a URL).

```sh
gh pr view <n> --json number,title,body,state,headRefOid,baseRefName,files,author
gh pr diff <n>
```

Fetch existing review threads (see `reference/github-api.md` for the GraphQL query). Note which are unresolved, their path/line, and what they asked for.

### 2. Investigate

Judge the diff **in context**, not in isolation. The working tree must stay untouched — read PR-state files via git plumbing instead of checking out:

```sh
git fetch origin pull/<n>/head          # updates FETCH_HEAD only
git show FETCH_HEAD:<path>              # any file exactly as the PR has it
```

For every non-trivial hunk: read the surrounding function/module at PR state, check callers of changed signatures, check whether tests cover the changed behavior, and check whether comments/docs/names elsewhere became stale because of this change (those become body findings). Do not run builds or tests — CI owns that.

### 3. Decide findings

For each candidate finding, keep it only if you can say concretely what to improve and why it matters. Drop anything you cannot defend. Map each survivor to:

- an exact `path` + line (or line range) **on the RIGHT side of the diff** → inline comment, or
- the review body, if it has no diff line to live on.

Skip findings already raised by an existing open thread — handle those via the thread instead. When the fix is a small in-place replacement, include a ```suggestion``` block so the author can one-click apply it.

### 4. Settle existing threads

For each unresolved thread: if the PR's current state answers the concern (fixed, made moot, or you verified it was a non-issue), reply with one line of reasoning, then resolve it. Otherwise leave it open.

### 5. Submit

Build one review payload: `event` (`APPROVE` if clean per the contract, else `COMMENT`), `body` (PR-wide findings only, or empty), `comments` (all inline findings). Submit it, then run the thread replies/resolutions. Exact API calls: `reference/github-api.md`.

Note: GitHub rejects approving your own PR — if that happens, report the PR is clean in the terminal instead.

### 6. Report

Tell the user in the terminal, briefly: how many inline comments, body findings, threads resolved/left open, and the verdict. Link the review. This is a status line, not a second copy of the review.
