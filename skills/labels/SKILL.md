---
name: labels
description: The GitHub labels for issues and PRs that drive the skill workflow (grilling, diagnose, review-pr, answer-review, finish-pr). Use when setting up labels in a repo, labeling an issue or PR, asking "what state is this issue in", or when another skill needs to know which label to apply or trust.
---

# Labels

One set of labels shared by all repos, designed around the skill pipeline. Each label names the next thing that should happen to the issue or PR, and the skills both read the labels and update them.

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

## Issue states: exactly one per open issue

| Label | Meaning | Next action |
|---|---|---|
| `needs-grilling` | Captured, but not specified well enough to build; the scope or design is still open | `/grill-with-docs` (or `/grill-me`) it into a spec |
| `needs-diagnosis` | A bug whose root cause is unknown, so there is no point specifying a fix yet | `/diagnose` to find the cause, then re-label |
| `needs-input` | A specific, named question is waiting on a human, either the maintainer or the reporter | They answer, then re-label (the `triage` sweep brings these back up) |
| `ready-for-agent` | Fully specified and blocked by nothing; an agent can start now | Implement |

`ready-for-agent` means exactly this: everything needed to implement is in the issue or its linked docs, and the issue depends on no open issue. If either stops being true, remove the label at once.

## Blocked: added alongside a state

`blocked` sits alongside a state label (for example `blocked` plus `needs-grilling`) when the issue depends on another open issue. The body must name the dependency: `Blocked by #N`. Remove `blocked` when #N closes.

- `blocked` and `ready-for-agent` never appear together, by definition.
- `needs-input` does not count as blocked. Waiting for a human's answer is the normal flow.
- An issue that is fully specified and waits only on its dependency carries `blocked` alone, with no state label. When the blocker closes, `blocked` comes off and it becomes `ready-for-agent`. An issue that is blocked and also under-specified carries `blocked` plus the fitting `needs-*` state.

## Categories (optional)

GitHub's built-in `bug` and `enhancement` may be added for filtering. They are not states, and the workflow does not read them.

## PR states: exactly one per open PR

| Label | Meaning | Next action |
|---|---|---|
| `ready-for-review` | The author considers it complete | `/review-pr` |
| `review-feedback` | The review left unresolved findings | `/answer-review` |
| `ready-to-merge` | The review came back clean or approved | `/finish-pr` |

The loop: open PR → `ready-for-review` → review finds issues → `review-feedback` → author responds → `ready-for-review` → … → clean review → `ready-to-merge` → merged.

## Who changes which label

- **Creating an issue**: apply the state that matches how far along it is (`needs-grilling` for ideas, `needs-diagnosis` for unexplained bugs, `ready-for-agent` only when it meets the definition above). Add `blocked` plus `Blocked by #N` when a dependency is known.
- **After grilling**: the spec is decided, so `ready-for-agent` (or `needs-input` if a question came up).
- **After diagnosis**: the cause is known, so `ready-for-agent` if the fix is now clear and specified, otherwise `needs-grilling` for a design discussion.
- **Opening a PR**: `ready-for-review`.
- **`review-pr`**: findings mean `review-feedback`; approval means `ready-to-merge`.
- **`answer-review`**: after responding, `ready-for-review`.
- **`finish-pr`**: merges `ready-to-merge` PRs and labels any follow-up issues it files.

Change labels with:

```sh
gh issue edit <n> --add-label ready-for-agent --remove-label needs-grilling
gh pr edit <n> --add-label review-feedback --remove-label ready-for-review
```

## Setting up a repo

Run the `setup-repo` skill. It owns the creation procedure: label creation that is safe to repeat, plus optional branch protection that matches these labels.

## When the labels are missing

Skills still do what they can and say what they skipped. `review-pr` and `answer-review` do their job, skip the label changes, and say so in their report. `implement` and `finish-pr`, whose behavior depends on the labels, stop at the affected step and offer to run `setup-repo` when the user is present.

## Consistency rules

When any skill touches an issue or PR and sees a combination that should not exist (two states, `blocked` plus `ready-for-agent`, or a `ready-for-agent` issue whose body says `Blocked by #N` with #N still open), fix it to the correct state and mention the correction in its report.
