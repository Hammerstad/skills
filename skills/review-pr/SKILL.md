---
name: review-pr
description: Review a GitHub pull request with inline comments posted on the PR itself. Use when the user says "review PR 98", "/review-pr 98", "review this pull request", or pastes a PR URL for review. Comments inline on exact file/lines, puts PR-wide findings in the review body, resolves addressed comment chains, approves when clean.
---

# Review PR

Review a pull request and deliver the findings on GitHub itself, inline on the exact file and line. Do not deliver them as a chat summary or as a summary comment on the PR.

## How to talk to the user

Write to the user in plain, direct English, the way you would explain the work to a colleague. Use full sentences and everyday words, with no slogans and no invented terms. Lead with what you found, what you did, and what happens next. The full guide is [STYLE.md](../../STYLE.md).

## Rules

- **Inline first.** Every finding that maps to a changed file and line becomes an inline review comment there. Findings that have no diff line to attach to (stale comments in untouched files, a rename that makes docs elsewhere wrong, a missing migration, and so on) go in the review body. If there are none, the body stays empty.
- **No praise and no filler.** Comment only where there is a real improvement to make. A good file gets nothing. A good PR gets zero comments; do not invent findings to look busy. This rule is about what survives step 3. It is not a budget for step 2: collect everything, then filter.
- **Full scope.** Correctness, edge cases, security, design, tests, and also style, naming, and consistency with the codebase's idioms when they are real improvements. Prefix small or taste-level findings with `nit:` so that the author can prioritize.
- **One review submission.** All inline comments and the body go out as a single review, so that the author gets one notification. Do not post a separate summary comment.
- **Verdict.** Zero new findings and no open threads that still apply means submit as `APPROVE`. Otherwise submit as `COMMENT`. Never `REQUEST_CHANGES`.
- **Close threads that are done.** For each existing unresolved review thread whose concern is now addressed or no longer applies, post a short reply saying why (for example "Addressed in `a1b2c3d`.") and then resolve it, regardless of who opened it. Threads that still have merit stay open and count as findings for the verdict.

## Workflow

### 1. Gather

Take the PR number from the argument (`98`, `#98`, or a URL).

```sh
gh pr view <n> --json number,title,body,state,headRefOid,baseRefName,files,author
gh pr diff <n>
```

Fetch the existing review threads before anything else (see `reference/github-api.md` for the GraphQL query). Their state decides what kind of round this is. Note which are unresolved, their path and line, what they asked for, and who replied last.

A previous review by you does not mean this pass is done. Every invocation is a full review round. If unresolved threads have author replies since your last review, this is a re-review round: the main work is verifying those replies (see step 4) and reviewing whatever commits landed since your last review, rather than redoing round one.

### 2. Investigate

Judge the diff in context rather than in isolation. Leave the working tree alone and read files at the PR's state with git plumbing instead of checking out:

```sh
git fetch origin pull/<n>/head          # updates FETCH_HEAD only
git show FETCH_HEAD:<path>              # any file exactly as the PR has it
```

For every non-trivial hunk: read the surrounding function or module at PR state, check the callers of changed signatures, check whether tests cover the changed behavior, and check whether comments, docs, or names elsewhere became stale because of this change (those become body findings). Do not run builds or tests; CI does that.

When the PR touches authentication, input handling, secrets, storage, or CI config, run the `review-security` checklist. When it touches hot paths, data access, or new I/O, run `review-performance`. Their findings go into this review's comments.

Collect everything at this step; filtering is step 3's job. Write down every candidate as you meet it, including the ones you would normally hold back: too small, probably intentional, not sure it is wrong. A candidate you never wrote down cannot be recovered later, while a weak one costs a single line in the next step. Do not decide what is worth reporting while you are still reading.

### 3. Decide the findings

Now filter. Keep a candidate only if you can say concretely what to improve and why it matters, based on the code in front of you. Drop it if you cannot defend it, if it is speculation about code the PR does not show, or if an existing open thread already raised it (handle that through the thread instead). Everything that survives is reported. There is no severity floor and no comment budget; `nit:` exists so that small but real findings have somewhere to go. Map each survivor to:

- an exact `path` plus a line or line range on the right-hand side of the diff, as an inline comment, or
- the review body, if it has no diff line to live on.

When the fix is a small in-place replacement, include a ```suggestion``` block so that the author can apply it with one click.

### 4. Handle existing threads

For each unresolved thread: if the PR's current state answers the concern (fixed, no longer relevant, or you verified it was not a problem), reply with one line of reasoning and then resolve it. Otherwise leave it open.

An author's reply saying "Fixed in `<sha>`" is a claim, and you need to check it: read that commit and the file at the PR head, and confirm that the fix addresses the finding. If it does, reply to confirm and resolve. If it does not, reply in the thread saying what is still missing and leave it open. That open thread counts as a finding for the verdict, so do not also post a duplicate new comment.

### 5. Submit

Build one review payload: `event` (`APPROVE` if clean per the rules, otherwise `COMMENT`), `body` (PR-wide findings only, or empty), and `comments` (all inline findings). Submit it, then post the thread replies and resolutions. Exact API calls: `reference/github-api.md`.

GitHub rejects approving your own PR. If that happens, report in the terminal that the PR is clean instead.

Then change the PR's state label as the `labels` skill describes. With findings: `gh pr edit <n> --add-label review-feedback --remove-label ready-for-review`. Approved or clean: `--add-label ready-to-merge --remove-label ready-for-review`, and also remove `review-feedback` if present. "Findings" means findings from this round: new comments posted now, or threads left open because they still apply. Comments from an earlier round whose threads you just resolved are done and do not count, so do not change the label to `review-feedback` because of them. If the repo does not have these labels, still do the full review, skip the label change, and note "workflow labels not set up in this repo (see `setup-repo`)" in the terminal report.

### 6. Report

Tell the user in the terminal, briefly: how many inline comments, how many body findings, how many threads resolved and left open, and the verdict. Link the review. This is a status line and should not repeat the review.
