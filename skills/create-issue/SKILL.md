---
name: create-issue
description: Capture a thought, feature idea, or bug report as a GitHub issue that is checked against the codebase and labeled with its real state. Use when the user says "create an issue for X", "file a bug", "add this to the backlog", or describes work that should be tracked rather than done now.
---

# Create Issue

Turn a description into an issue that is accurate about the problem, about the codebase, and about how ready it is to work on (labeled as the `labels` skill describes). Capturing is quick. Going deeper is optional and is offered at the end.

## How to talk to the user

Write to the user in plain, direct English, the way you would explain the work to a colleague. Use full sentences and everyday words, with no slogans and no invented terms. Lead with what you found, what you did, and what happens next. The full guide is [STYLE.md](../../STYLE.md).

## Workflow

### 1. Pick the repo

Detect the repo from `git remote -v`. If the user names one, use that instead. Confirm the target in the report rather than asking.

### 2. Check it against the codebase

Before writing a word of the issue:

- **Search the codebase** for the code the description touches. Use the project's own vocabulary from `CONTEXT.md` in everything you write.
- **Check whether it already exists.** If the requested behavior is already there, say so and point at it instead of filing. If the current behavior differs from what the user described, note the difference in the issue.
- **Check for duplicates** with `gh issue list --search "<key terms>"` over open issues. If there is a duplicate, point at it instead of filing another.

### 3. Write it

- **Title**: short and imperative.
- **Body**: **Problem** (current behavior or gap), **Expected behavior**, **Acceptance criteria** (checkboxes that can be verified), **Context** (constraints, references, relevant findings from step 2). Include file or component names only where they help, since they go stale.
- Only what the user described plus what the codebase shows. Do not invent requirements.

### 4. Label it

Following the `labels` skill: `needs-grilling` for most ideas and features, `needs-diagnosis` for a bug with an unknown root cause, `ready-for-agent` only when the issue already meets that label's bar (small, fully specified, blocked by nothing), and `blocked` plus `Blocked by #N` in the body when a dependency is known. Add `bug` or `enhancement` if the repo uses them. If the repo does not have the workflow labels, file the issue anyway and note the missing labels in the report (see `setup-repo`).

### 5. File it and offer to go deeper

```sh
gh issue create --title "..." --body-file issue.md --label <labels>
```

Report the number and URL. Then offer, without starting on your own: "Grill it to ready-for-agent now?" If yes, run `grill-with-docs`, fold the decisions back into the issue body, and re-label. If the session shows that the issue is really several slices, hand over to `to-issues`.
