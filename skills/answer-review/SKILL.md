---
name: answer-review
description: Respond to a review on a GitHub pull request as the author - fix or push back on every comment, replying inline in the PR. Use when the user says "answer the review", "respond to the review on PR 98", "address review comments", or a PR they authored has been reviewed.
---

# Answer Review

Respond to a PR review as the author. Every reviewer comment gets exactly one response on GitHub: either a fix, with the commit that fixes it, or a reasoned pushback. Do not post a summary comment, and do not respond only in chat.

## How to talk to the user

Write like an engineer reporting to a colleague who is short on time. These rules apply to replies in the chat and to everything you write into GitHub or into docs.

- Lead with the result. First line: what happened or what you found. Then what the reader has to do. Stop there. Add details only when asked.
- If something failed or was skipped, that is the first line, with the output.
- Keep a chat reply under ten lines unless it is a list of findings. One idea per sentence. One sentence per bullet. A reply that repeats what a diff or a tool result already shows adds nothing.
- Say the literal thing. Mannered prose swaps a direct statement for a metaphor or a flourish: "a landmine with no warning sign" for "this breaks when vite is updated", "fold this in" for "add this", "silently" for "without an error", "the key insight" for nothing at all. Metaphors carry meanings you did not choose, and the reader has to translate them. When a literal phrase is available, use it.
- Do not sell and do not narrate. A recommendation gets its reason in one clause or none. Cut "this matters more than it looks", "in other words", "worth noting", "the real question is". Do not describe what you are about to do or how you reasoned.
- Use everyday words. Established engineering terms are fine when there is no short everyday equivalent (rebase, worktree, ADR, regression test, N+1 query). Spell out any other acronym the first time it appears. Do not coin a name for something that has an ordinary description.
- Format for the reader, not for effect. Bullets when there are several parallel items, a table when there are rows and columns, a heading only in a document that is long enough to navigate. No bold lead-ins on bullets. Bold at most the one thing the reader must not miss. Prefer a period or a comma to an em-dash. Commands, paths, and error text go in backticks or a code block, not in the middle of a sentence.
- Before sending, reread the draft once and delete: metaphors, sentences that justify a recommendation, anything the reader did not ask for.

## Rules

- **Every unresolved inline thread gets a response.** Fix or push back. Do not leave a thread hanging or skip one because it is inconvenient. Resolved threads are done; ignore them. Threads where the last reply is already ours are waiting on the reviewer; ignore them too. This is what makes re-runs safe.
- **Fix by default.** Push back only when the comment is factually wrong, would make the code worse, or is out of scope for this PR (then say so and propose where it belongs). A pushback is one or two sentences of technical reasoning, without apology and without "great point, but".
- **Reply, but do not resolve.** The reviewer verifies and resolves threads; that is the `review-pr` skill's job on its next round. Leave every thread open.
- **One commit per logical fix.** Each fixed thread's reply names the SHA that fixes it ("Fixed in `a1b2c3d`."). Related comments fixed by one change share a commit. Push once at the end, before posting replies, so that every SHA you cite exists on GitHub when the reviewer clicks it.
- **Review-body and PR-comment findings get one quote-reply comment.** Findings in a review body or in ordinary PR comments have no reply mechanism on GitHub, so respond to them in a single PR comment that quotes each point with `>` followed by its response. Post it only when such points exist. It answers specific points and does not summarize the work.

## Workflow

### 1. Gather

Take the PR number from the argument, or detect it from the current branch with `gh pr view --json number`.

Collect everything that needs an answer (queries in `reference/github-api.md`):

- unresolved inline review threads, skipping those where we replied last,
- review bodies that contain findings,
- ordinary PR comments that raise points no thread already covers.

### 2. Get on the branch

```sh
git status --porcelain    # must be clean - abort if dirty with unrelated changes
gh pr checkout <n>        # no-op if already on the branch; handles forks
git pull                  # put the fixes on top of the latest head
```

### 3. Decide each thread

Read the thread, the file as it is now, and enough surrounding code to judge whether the reviewer is right. Decide: fix or push back. When a reviewer left a ```suggestion``` block you agree with, apply it as a local edit. Do not accept it through the GitHub UI, because that creates commits your local branch does not have.

### 4. Fix

For each fix: edit, verify (run the targeted tests or build for the touched area when the project has them; the full CI run stays CI's job), and commit with a message naming the concern, for example `fix: handle empty batch in charger sync (review)`. Keep a record of which thread each SHA answers.

### 5. Push, then respond

```sh
git push
```

Then, for each thread, reply with `Fixed in <sha>.` plus one line on what changed if the fix is not self-evident, or with the pushback reasoning. Finally post the single quote-reply comment for any points that were not in inline threads. API calls: `reference/github-api.md`.

Change the PR's state label as the `labels` skill describes: `gh pr edit <n> --add-label ready-for-review --remove-label review-feedback`. The reviewer is up next. If the repo does not have these labels, still respond in full, skip the label change, and note "workflow labels not set up in this repo (see `setup-repo`)" in the terminal report.

### 6. Report

One status line in the terminal: N fixed (with commits), M pushed back, whether the quote-reply comment was posted, and anything you could not respond to and why. Do not repeat the responses themselves.
