---
name: labels
description: The GitHub label taxonomy for issues and PRs that drives the skill workflow (grilling, diagnose, review-pr, answer-review, finish-pr). Use when setting up labels in a repo, labeling an issue or PR, asking "what state is this issue in", or when another skill needs to know which label to apply or trust.
---

# Labels

One label taxonomy shared by all repos, designed around the skill pipeline. Labels are **state, not decoration**: each label names the next action, and skills both read and flip them.

## Issue states — exactly one per open issue

| Label | Meaning | Next action |
|---|---|---|
| `needs-grilling` | Captured, but under-specified — scope/design not settled | `/grill-with-docs` (or `/grill-me`) it into a spec |
| `needs-diagnosis` | Bug with unknown root cause — no point spec'ing a fix yet | `/diagnose` to find the cause, then re-label |
| `needs-input` | A **named question** waits on a human — maintainer or reporter | They answer, then re-label (the `triage` sweep re-surfaces these) |
| `ready-for-agent` | Spec complete **and** unblocked — an agent can start now | Implement |

`ready-for-agent` is a guarantee, not a hope: everything needed to implement is in the issue (or linked docs), and it depends on no open issue. If either stops being true, the label must come off immediately.

## Blocked — a flag, not a state

`blocked` sits **alongside** a state (e.g. `blocked` + `needs-grilling`) when the issue depends on another open issue. The body must name the dependency: `Blocked by #N`. Remove the flag when #N closes.

- `blocked` and `ready-for-agent` are mutually exclusive by definition.
- `needs-input` is **not** blocked — waiting on a human's answer is normal flow.
- An issue that is fully specified and waits **only** on its dependency carries `blocked` alone (no state label). When the blocker closes, the flag comes off and it becomes `ready-for-agent`. An issue that is blocked *and* under-specified carries `blocked` plus the fitting `needs-*` state.

## Categories (optional flavor)

GitHub's built-in `bug` / `enhancement` may be added for filtering. They are not states and carry no workflow meaning.

## PR states — exactly one per open PR

| Label | Meaning | Next action |
|---|---|---|
| `ready-for-review` | Author considers it complete | `/review-pr` |
| `review-feedback` | Review left unresolved findings | `/answer-review` |
| `ready-to-merge` | Review came back clean / approved | `/finish-pr` |

The loop: open PR → `ready-for-review` → review finds issues → `review-feedback` → author responds → `ready-for-review` → … → clean review → `ready-to-merge` → merged.

## Who flips what

- **Creating an issue**: apply the state that matches its maturity (`needs-grilling` for ideas, `needs-diagnosis` for unexplained bugs, `ready-for-agent` only when the spec test above passes). Add `blocked` + `Blocked by #N` when known.
- **After grilling**: the spec is settled → `ready-for-agent` (or `needs-input` if a question emerged).
- **After diagnosis**: cause known → `ready-for-agent` if the fix is now obvious and spec'd, else `needs-grilling` for a design discussion.
- **Opening a PR**: `ready-for-review`.
- **`review-pr`**: findings → `review-feedback`; approval → `ready-to-merge`.
- **`answer-review`**: after responding → `ready-for-review`.
- **`finish-pr`**: merges `ready-to-merge` PRs; labels any follow-up issues it files.

Flip with:

```sh
gh issue edit <n> --add-label ready-for-agent --remove-label needs-grilling
gh pr edit <n> --add-label review-feedback --remove-label ready-for-review
```

## Setting up a repo

Run the `setup-repo` skill — it owns the creation procedure (idempotent label creation, plus optional branch protection aligned with this taxonomy).

## When the taxonomy is missing

Skills degrade loudly, never silently and never fatally: `review-pr` and `answer-review` do their job, skip label flips, and say so in their report; `implement` and `finish-pr` (whose semantics depend on the labels) stop at the affected step and offer to run `setup-repo` when the user is present.

## Consistency rules

When any skill touches an issue/PR and sees an illegal combination (two states, `blocked`+`ready-for-agent`, a `ready-for-agent` issue whose body says `Blocked by #N` with #N open), fix it to the truthful state and mention the correction in its report.
