---
name: review-pr
description: Review a GitHub pull request with inline comments posted on the PR itself. Use when the user says "review PR 98", "/review-pr 98", "review this pull request", or pastes a PR URL for review. Comments inline on exact file/lines, puts PR-wide findings in the review body, resolves addressed comment chains, approves when clean.
---

# Review PR

Review a pull request and deliver the findings **on GitHub itself** — inline, on the exact file and line — never as a chat summary or a PR summary comment.

## Contract

- **Inline first.** Every finding that maps to a changed file/line becomes an inline review comment there. Findings that cannot be attributed to a diff line (stale comments in untouched files, a rename that makes docs elsewhere wrong, missing migration, etc.) go in the **review body**. If there are none, the body stays empty.
- **No praise, no filler.** Only comment where there is a genuine improvement. If a file is good, it gets nothing. If the whole PR is good, it gets zero comments — do not invent findings to look busy. This is a rule about what *survives* step 3, not a budget for step 2: generate exhaustively, then filter.
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

Fetch existing review threads (see `reference/github-api.md` for the GraphQL query) **before anything else** — their state decides what kind of round this is. Note which are unresolved, their path/line, what they asked for, and who replied last.

**A previous review by you does not mean this pass is done.** Every invocation is a full review round. If unresolved threads carry author replies since your last review, this is a **re-review round**: the primary work is verifying those replies (below), plus reviewing whatever commits landed since your last review — not re-deriving round one.

### 2. Investigate

Judge the diff **in context**, not in isolation. The working tree must stay untouched — read PR-state files via git plumbing instead of checking out:

```sh
git fetch origin pull/<n>/head          # updates FETCH_HEAD only
git show FETCH_HEAD:<path>              # any file exactly as the PR has it
```

For every non-trivial hunk: read the surrounding function/module at PR state, check callers of changed signatures, check whether tests cover the changed behavior, and check whether comments/docs/names elsewhere became stale because of this change (those become body findings). Do not run builds or tests — CI owns that.

When the PR touches auth, input handling, secrets, storage, or CI config, apply the `review-security` lens; when it touches hot paths, data access, or new I/O, apply `review-performance`. Their findings flow into this review's comments.

**Collect exhaustively here — filtering is step 3's job.** Write down every candidate as you hit it, including the ones you would normally self-censor: too small, probably intentional, not sure it's wrong. A candidate you never wrote down cannot be recovered later, while a weak one costs a single line in the next step. Do not decide what is worth reporting while you are still reading.

### 3. Decide findings

Now filter. Keep a candidate only if you can say concretely what to improve and why it matters, from the code in front of you. Drop it if you cannot defend it, if it is speculation about code the PR doesn't show, or if an existing open thread already raised it (handle that via the thread instead). Everything that survives is reported — there is no severity floor and no comment budget; `nit:` exists precisely so small-but-real findings have somewhere to go. Map each survivor to:

- an exact `path` + line (or line range) **on the RIGHT side of the diff** → inline comment, or
- the review body, if it has no diff line to live on.

When the fix is a small in-place replacement, include a ```suggestion``` block so the author can one-click apply it.

### 4. Settle existing threads

For each unresolved thread: if the PR's current state answers the concern (fixed, made moot, or you verified it was a non-issue), reply with one line of reasoning, then resolve it. Otherwise leave it open.

An author reply claiming "Fixed in `<sha>`" is a claim, not a settlement: read that commit and the file at the PR head, and confirm the fix actually addresses the finding. Confirmed → reply-confirm and resolve. Not actually fixed → reply in the thread saying what's still missing and leave it open (that open thread is a finding for the verdict — do not also post a duplicate new comment).

### 5. Submit

Build one review payload: `event` (`APPROVE` if clean per the contract, else `COMMENT`), `body` (PR-wide findings only, or empty), `comments` (all inline findings). Submit it, then run the thread replies/resolutions. Exact API calls: `reference/github-api.md`.

Note: GitHub rejects approving your own PR — if that happens, report the PR is clean in the terminal instead.

Then flip the PR's state label per the `labels` skill: findings → `gh pr edit <n> --add-label review-feedback --remove-label ready-for-review`; approved/clean → `--add-label ready-to-merge --remove-label ready-for-review` (also remove `review-feedback` if present). "Findings" means findings from **this round**: new comments posted now, or threads left open as still-valid now. Comments from an earlier round whose threads you just resolved are settled, not findings — never flip to `review-feedback` on their account. If the repo lacks these labels, still do the full review — just skip the flip and note "label taxonomy not set up in this repo (see `setup-repo`)" in the terminal report.

### 6. Report

Tell the user in the terminal, briefly: how many inline comments, body findings, threads resolved/left open, and the verdict. Link the review. This is a status line, not a second copy of the review.
