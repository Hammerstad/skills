---
name: answer-review
description: Respond to a review on a GitHub pull request as the author — fix or push back on every comment, replying inline in the PR. Use when the user says "answer the review", "respond to the review on PR 98", "address review comments", or a PR they authored has been reviewed.
---

# Answer Review

Respond to a PR review as the author. Every reviewer comment gets exactly one response **on GitHub**: either a fix (with the commit that fixes it) or a reasoned pushback. Never a summary comment, never a response in chat only.

## Contract

- **Every unresolved inline thread gets a response.** Fix or pushback — no thread left hanging, none skipped because it's inconvenient. Resolved threads are settled; ignore them. Threads where the last reply is already ours are awaiting the reviewer; ignore them too (this makes re-runs safe).
- **Fix by default.** Push back only when the comment is factually wrong, would make the code worse, or is genuinely out of scope for this PR (then say so and propose where it belongs). Pushback is technical reasoning, not defensiveness — one or two sentences, no apology, no "great point, but".
- **Reply only, never resolve.** The reviewer verifies and resolves threads (that's the `review-pr` skill's job on its next round). Leave every thread open.
- **One commit per logical fix.** Each fixed thread's reply cites the SHA that fixes it ("Fixed in `a1b2c3d`."). Related comments fixed by one change share a commit. Push once at the end, **before** posting replies, so every cited SHA is live when the reviewer clicks it.
- **Non-inline review content gets one quote-reply comment.** Findings in a review body or in regular PR comments have no reply mechanism on GitHub, so respond to them in a single PR comment that `>` quotes each point followed by its response. Post it only when such points exist — this is a targeted response, not a summary of the work.

## Workflow

### 1. Gather

Parse the PR number from the argument, or detect it from the current branch (`gh pr view --json number`).

Collect everything that needs answering (queries in `reference/github-api.md`):

- unresolved inline review threads (skip those where we replied last),
- review bodies containing findings,
- regular PR comments raising points not already covered by a thread.

### 2. Get on the branch

```sh
git status --porcelain    # must be clean — abort if dirty with unrelated changes
gh pr checkout <n>        # no-op if already on the branch; handles forks
git pull                  # make sure the fixes land on top of the latest head
```

### 3. Triage each thread

Read the thread, the file at its current state, and enough surrounding code to judge whether the reviewer is right. Decide: **fix** or **pushback**. When a reviewer left a ```suggestion``` block you agree with, apply it as a local edit (do not accept via the GitHub UI — it would create commits behind your local branch).

### 4. Fix

For each fix: edit, verify (run the targeted tests or build for the touched area when the project has them — full CI stays CI's job), and commit with a message naming the concern, e.g. `fix: handle empty batch in charger sync (review)`. Record thread → SHA as you go.

### 5. Push, then respond

```sh
git push
```

Then, per thread: reply with `Fixed in <sha>.` (plus one line of what changed, if the fix isn't self-evident) or the pushback reasoning. Finally post the single quote-reply comment for any non-inline points. API calls: `reference/github-api.md`.

Flip the PR's state label per the `labels` skill: `gh pr edit <n> --add-label ready-for-review --remove-label review-feedback` — the ball is back in the reviewer's court. Skip silently if the repo doesn't have these labels.

### 6. Report

Terminal status line: N fixed (with commits), M pushed back, quote-reply posted or not, plus anything you couldn't respond to and why. Not a second copy of the responses.
