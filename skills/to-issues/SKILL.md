---
name: to-issues
description: Break a plan, spec, or grill-session outcome into GitHub issues that can each be picked up on their own, as thin end-to-end slices, labeled as the labels skill describes. Use when the user wants to convert a plan into issues, create implementation tickets, break down work, or after a grilling session settles a design.
---

# To Issues

Break a plan into issues an agent can pick up and finish. This is the bridge between an agreed design (usually from a `grill-with-docs` session) and the `implement` skill. The output is issues whose labels match their real state, as the `labels` skill describes.

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

## Process

### 1. Gather

Work from the conversation context; a just-finished grill session is the common case. If the user passes an issue, URL, or path, read all of it, body and comments.

### 2. Check against the codebase

Explore enough to slice realistically. Titles and bodies use the project's own vocabulary from `CONTEXT.md` and respect the ADRs in the area.

### 3. Draft the slices

Each issue is a thin slice that goes through every layer it touches (schema, API, UI, tests) and is complete on its own. Do not slice by layer.

- A finished slice can be demonstrated or verified on its own.
- Prefer many thin slices over a few thick ones.
- Order matters: the first slice proves the path from end to end, and later slices widen it.

### 4. Label each slice

For each slice, pick the state label as the `labels` skill defines them:

- **`ready-for-agent`**: the grill session decided everything this slice needs, and no other slice must land first. This should be the case for most slices.
- **`needs-input`**: one named decision is still open, and the issue body states the exact question.
- **`needs-grilling`**: the slice brought up design questions the session did not cover.
- **`blocked`**: another slice must land first, and the body says `Blocked by #N`. If the slice is fully specified and only waiting on the dependency, it carries `blocked` alone; it becomes `ready-for-agent` when the blocker closes (`finish-pr` does this automatically). If it is blocked and also under-specified, it carries `blocked` plus the fitting `needs-*` state. Never `blocked` together with `ready-for-agent`.

### 5. Check with the user

Present the breakdown as a numbered list, with the title, proposed labels, what it is blocked by, and which requirements it covers for each slice. Ask: is the granularity right? Are the dependencies right? Should anything be merged or split? Repeat until the user approves.

### 6. Publish

Publish in dependency order, blockers first, so that `Blocked by #N` refers to real numbers:

```sh
gh issue create --title "<slice title>" --label <labels> --body-file <slice>.md
```

Issue body template:

```markdown
## Parent

#<parent issue> (omit if none)

## What to build

End-to-end behavior of this slice, in the project's vocabulary. No file paths
or code snippets, because they go stale. Exception: a decision-heavy artifact
from the grill session or a prototype (a state machine, schema, or type shape)
may be inlined, trimmed to the parts that encode the decision.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

#N — or "None - can start immediately"
```

Do not close or modify the parent issue.
