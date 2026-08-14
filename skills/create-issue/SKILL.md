---
name: create-issue
description: Capture a thought, feature idea, or bug report as a well-grounded, truthfully-labeled GitHub issue. Use when the user says "create an issue for X", "file a bug", "add this to the backlog", or describes work that should be tracked rather than done now.
---

# Create Issue

Turn a description into an issue that tells the truth — about the problem, about the codebase, and about its own readiness (label per the `labels` skill). Capture is fast; depth is optional and offered at the end.

## Workflow

### 1. Target

Detect the repo from `git remote -v` (user override wins). Confirm the target in the report, not with a question.

### 2. Ground it

Before writing a word of the issue:

- **Search the codebase** for the code the description touches. Use the project's domain vocabulary (`CONTEXT.md`) in everything you write.
- **Redundancy check** — if the requested behavior already exists, say so and point at it instead of filing; if current behavior differs from what the user described, note the discrepancy in the issue.
- **Duplicate check** — `gh issue list --search "<key terms>"` (open issues); a duplicate gets a pointer, not a sibling.

### 3. Write it

- **Title**: concise, imperative.
- **Body**: **Problem** (current behavior or gap) · **Expected behavior** · **Acceptance criteria** (verifiable checkboxes) · **Context** (constraints, references, relevant findings from step 2 — file/component names only where they genuinely help; they go stale).
- Only what the user described plus what the codebase shows. No invented requirements.

### 4. Label truthfully

Per the `labels` skill: `needs-grilling` (the usual case for ideas and features), `needs-diagnosis` (bug with unknown root cause), `ready-for-agent` (only when the capture already passes its guarantee — small, fully specified, unblocked), `blocked` + `Blocked by #N` when a dependency is known. Add `bug`/`enhancement` if the repo uses them. Repo without the taxonomy: file the issue anyway and note the missing labels in the report (see `setup-repo`).

### 5. File and offer depth

```sh
gh issue create --title "..." --body-file issue.md --label <labels>
```

Report the number and URL. Then offer — don't start unasked: **"Grill it to ready-for-agent now?"** If yes, run `grill-with-docs`, fold the settled decisions back into the issue body, and re-label. If the session reveals the issue is really several slices, hand over to `to-issues`.
