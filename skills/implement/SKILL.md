---
name: implement
description: Implement a ready-for-agent GitHub issue end to end - branch, build in small verified increments, and open a PR labeled ready-for-review. Use when the user says "implement issue 42", "/implement 42", "pick up issue 42", or asks to build the change an issue describes.
---

# Implement

Take a `ready-for-agent` issue (see the `labels` skill) to a PR that is genuinely ready for review. The issue is the spec — it was grilled into shape before it got that label. The output is a branch and a PR; **merging is `finish-pr`'s job, never this skill's**.

## Contract

- **The label is the spec guarantee.** Before writing code, verify the issue carries `ready-for-agent` and actually passes its test: everything needed to implement is in the issue or its linked docs, and it depends on no open issue. If it doesn't, fix the label to the truthful state per the `labels` skill and stop — implementing an unready issue produces the wrong thing efficiently.
- **Every task lands in isolation.** The sequence for every task is: **code → build → test → format → stage named files → commit**. Never batch tasks into one commit. Never proceed while build, tests, or format check fail. The repo is green after every single commit.
- **Tests are part of the task, not a phase.** Each task includes the tests that prove its behavior. Never claim done for work whose verification commands you have not actually run.
- **Scope is the issue.** No invented features, no drive-by refactors beyond what the task needs. Adjacent improvements you notice become follow-up issue candidates in the PR body, not code.
- **Spec gaps:** if a real ambiguity blocks a decision mid-flight — interactive session: ask the user, then continue. Unattended: post the question as an issue comment, flip the label to `needs-input`, push the branch as-is (no PR), and stop cleanly.
- **PR only at the end.** Work stays local until everything is done and green; then one push, one PR, labeled `ready-for-review`.

## Workflow

### 1. Absorb the spec

```sh
gh issue view <n> --json title,body,labels,url,comments
```

Read the full issue including comments — later comments often amend the spec. Read `CONTEXT.md` (if it exists) and ADRs touching the area. Then run the readiness check from the contract.

If the repo has no label taxonomy at all (`gh label list` shows none of the workflow labels), the spec guarantee cannot exist: interactively, offer to run `setup-repo` and to triage this issue properly first — with explicit user confirmation the implementation may proceed anyway, treating the issue body as the spec at the user's risk. Unattended: stop and report; never treat an unlabeled issue as ready.

### 2. Set up — isolated worktree

Work in a dedicated git worktree so the main checkout is never touched and parallel `implement` runs can't collide:

```sh
git fetch origin
gh issue develop <n>                                   # creates a branch linked to the issue
git worktree add ../<repo>-issue-<n> <branch-name>     # sibling dir, own checkout
gh issue edit <n> --add-assignee @me
```

**All subsequent work happens inside the worktree directory.** No clean-tree requirement on the main checkout — its state is irrelevant. If a worktree for this issue already exists, resume in it instead of creating another.

The assignment is the in-progress signal — the label stays `ready-for-agent` until the PR closes the issue.

### 3. Discover the toolchain

Read the repo's own instructions (`CLAUDE.md`, `CONTRIBUTING.md`, README, CI config) for the **build**, **test**, and **format/lint** commands. Every "build/test/format" below means those discovered commands. Run build + tests once for a clean baseline: a trivially broken baseline gets fixed as its own first commit; a non-trivially broken one is its own issue — stop and report.

### 4. Plan the tasks

Break the issue into small ordered tasks, each one committable and green on its own. Prefer vertical slices (a thin end-to-end path first, then widen) over horizontal layers. Each task names its verification: which tests prove it. Show the task list in the terminal before starting; in an interactive session the user can object — don't wait for approval.

### 5. Execute, task by task

For each task, in order:

1. Apply the minimal changes, including the task's tests.
2. Build — fix until it compiles.
3. Test — fix until everything passes (fixes re-run build + tests).
4. Format/lint — fix violations, re-verify.
5. `git add <file1> <file2> ...` — named files only, never `-A` or `.`.
6. Commit: imperative header, body saying what changed and why per file when it isn't obvious.

Only then the next task. If a later task invalidates an earlier decision, that's a new task with its own commit — history stays honest.

### 6. Finish

1. Final full build + test + format run — zero failures.
2. Rebase onto the latest default branch (`git fetch`, `git rebase origin/<base>`). On conflicts: understand what each side changed before resolving — integrate both where possible, never blindly take one side; if genuinely ambiguous, treat it as a spec gap (contract above).
3. Push, then:

```sh
gh pr create --title "<imperative summary>" --body "<what & why, notable decisions, follow-up candidates>

Closes #<n>"
gh pr edit --add-label ready-for-review   # skip silently if the repo lacks the label
```

4. Remove the worktree — the branch lives on remote and locally; only the checkout goes:

```sh
git worktree remove ../<repo>-issue-<n>
```

Exception: a run that stops early (spec gap, unattended halt) **leaves its worktree in place** so the next run resumes exactly where it stopped.

### 7. Report

Terminal status: tasks completed with their commits, final build/test result, PR link, and any assumptions or follow-up candidates flagged in the PR body. The review loop (`review-pr` → `answer-review` → `finish-pr`) takes it from here.
