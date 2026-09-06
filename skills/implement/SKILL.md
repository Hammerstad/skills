---
name: implement
description: Implement a ready-for-agent GitHub issue end to end - branch, build in small verified steps, and open a PR labeled ready-for-review. Use when the user says "implement issue 42", "/implement 42", "pick up issue 42", or asks to build the change an issue describes.
---

# Implement

Take an issue labeled `ready-for-agent` (see the `labels` skill) to a PR that is ready for review. The issue is the spec; it was grilled into shape before it got that label. The output is a branch and a PR. This skill does not merge; that is `finish-pr`'s job.

## How to talk to the user

Write to the user in plain, direct English, the way you would explain the work to a colleague. Use full sentences and everyday words, with no slogans and no invented terms. Lead with what you found, what you did, and what happens next. The full guide is [STYLE.md](../../STYLE.md).

## Rules

- **Check the label before writing code.** `ready-for-agent` means that everything needed to implement is in the issue or its linked docs, and that the issue depends on no open issue. Verify that this is actually true. If it is not, correct the label as the `labels` skill describes and stop. Implementing an issue that is not ready wastes the work.
- **Every task is committed on its own.** For each task the sequence is: code, build, test, format, stage the named files, commit. Do not combine tasks into one commit. Do not continue while the build, the tests, or the format check fail. The repo is green after every commit.
- **Tests are part of each task.** Each task includes the tests that prove its behavior. Do not claim a task is done if you have not run its verification commands.
- **The scope is the issue.** No invented features, and no refactoring beyond what the task needs. Improvements you notice along the way are listed in the PR body as candidates for follow-up issues, and are not implemented.
- **Spec gaps.** If a real ambiguity blocks a decision partway through: in an interactive session, ask the user and continue. When running unattended, post the question as an issue comment, change the label to `needs-input`, push the branch as it is without opening a PR, and stop.
- **Open the PR at the end.** Work stays local until everything is done and green. Then push once and open one PR labeled `ready-for-review`.

## Workflow

### 1. Read the spec

```sh
gh issue view <n> --json title,body,labels,url,comments
```

Read the whole issue including comments, since later comments often amend the spec. Read `CONTEXT.md` if it exists and any ADRs for the area. Then do the label check from the rules above.

If the repo has none of the workflow labels at all (`gh label list` shows none of them), the label cannot vouch for the issue. In an interactive session, offer to run `setup-repo` and to triage this issue properly first. If the user explicitly confirms, you may proceed anyway, treating the issue body as the spec at their risk. When running unattended, stop and report. Never treat an unlabeled issue as ready.

### 2. Set up an isolated worktree

Work in a dedicated git worktree so that the main checkout is never touched and parallel `implement` runs cannot collide:

```sh
git fetch origin
gh issue develop <n>                                   # creates a branch linked to the issue
git worktree add ../<repo>-issue-<n> <branch-name>     # sibling dir, own checkout
gh issue edit <n> --add-assignee @me
```

All further work happens inside the worktree directory. The main checkout does not need to be clean; its state does not matter. If a worktree for this issue already exists, resume in it instead of creating another.

The assignment signals that work is in progress. The label stays `ready-for-agent` until the PR closes the issue.

### 3. Find the build, test, and format commands

Read the repo's own instructions (`CLAUDE.md`, `CONTRIBUTING.md`, the README, CI config) for the build, test, and format or lint commands. Every "build", "test", and "format" below means those commands. Run the build and tests once to get a clean baseline. If the baseline is broken in a trivial way, fix it as the first commit. If it is broken in a way that is not trivial, that is a separate issue: stop and report.

### 4. Plan the tasks

Break the issue into small ordered tasks, each one committable and green on its own. Prefer thin end-to-end slices (a minimal path through every layer first, then widen it) over building one layer at a time. Each task names the tests that prove it. Show the task list in the terminal before starting. In an interactive session the user can object, but do not wait for approval.

### 5. Work through the tasks

For each task, in order:

1. Make the minimal changes, including the task's tests.
2. Build. Fix until it compiles.
3. Test. Fix until everything passes, re-running the build and tests after each fix.
4. Format and lint. Fix violations and re-verify.
5. `git add <file1> <file2> ...` with named files only, never `-A` or `.`.
6. Commit with an imperative header and a body that says what changed and why per file, when that is not obvious.

Only then move to the next task. If a later task reverses an earlier decision, that is a new task with its own commit, so that the history shows what actually happened.

### 6. Finish

1. Rebase onto the latest default branch (`git fetch`, then `git rebase origin/<base>`). On conflicts, understand what each side changed before resolving. Integrate both where possible and never take one side blindly. If it is truly ambiguous, treat it as a spec gap as described in the rules.
2. Run the full build, tests, and format check one more time, with zero failures. Do this after the rebase. Every task already passed on its own, so the only thing this run can still catch is a change in the base branch underneath you, including a conflict that resolved cleanly but wrongly.
3. Push, then:

```sh
gh pr create --title "<imperative summary>" --body "<what & why, notable decisions, follow-up candidates>

Closes #<n>"
gh pr edit --add-label ready-for-review   # skip silently if the repo lacks the label
```

4. Remove the worktree. The branch still exists on the remote and locally; only the checkout goes:

```sh
git worktree remove ../<repo>-issue-<n>
```

Exception: a run that stops early (a spec gap, or an unattended halt) leaves its worktree in place so that the next run can resume where it stopped.

### 7. Report

Tell the user in the terminal: the tasks completed with their commits, the final build and test result, the PR link, and any assumptions or follow-up candidates you listed in the PR body. The review loop (`review-pr`, then `answer-review`, then `finish-pr`) takes it from here.
