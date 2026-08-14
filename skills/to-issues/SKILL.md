---
name: to-issues
description: Break a plan, spec, or grill-session outcome into independently-grabbable GitHub issues using tracer-bullet vertical slices, labeled per the labels skill. Use when the user wants to convert a plan into issues, create implementation tickets, break down work, or after a grilling session settles a design.
---

# To Issues

Break a plan into issues an agent can grab and finish. This is the bridge between a settled design (usually a `grill-with-docs` session) and the `implement` skill: the output is issues whose labels tell the truth per the `labels` skill.

## Process

### 1. Gather

Work from the conversation context (a just-finished grill session is the common case). If the user passes an issue/URL/path, read it fully — body and comments.

### 2. Ground in the codebase

Explore enough to slice realistically. Titles and bodies use the project's domain vocabulary (`CONTEXT.md`) and respect ADRs in the area.

### 3. Draft vertical slices

Each issue is a **tracer bullet**: a thin but COMPLETE path through every layer it touches (schema, API, UI, tests) — never a horizontal layer.

- A completed slice is demoable or verifiable on its own.
- Prefer many thin slices over few thick ones.
- Slice order matters: the first slice proves the path end-to-end; later slices widen it.

### 4. Label honestly

Per slice, decide the state label (`labels` skill semantics):

- **`ready-for-agent`** — the grill session settled everything this slice needs, and no other slice must land first. This should be the goal for most slices.
- **`needs-input`** — one named decision is still open; the issue body states the exact question.
- **`needs-grilling`** — the slice surfaced design territory the session didn't cover.
- **`blocked`** — another slice must land first; body says `Blocked by #N`. Fully specified and only waiting on the dependency → `blocked` **alone**; it becomes `ready-for-agent` when the blocker closes (`finish-pr` does this automatically). Blocked *and* under-specified → `blocked` + the fitting `needs-*` state. Never `blocked` + `ready-for-agent`.

### 5. Quiz the user

Present the breakdown as a numbered list — per slice: title, proposed labels, blocked-by, and which requirements it covers. Ask: granularity right? dependencies right? merge/split anything? Iterate until approved.

### 6. Publish

Publish in dependency order (blockers first) so `Blocked by #N` cites real numbers:

```sh
gh issue create --title "<slice title>" --label <labels> --body-file <slice>.md
```

Issue body template:

```markdown
## Parent

#<parent issue> (omit if none)

## What to build

End-to-end behavior of this slice, in domain vocabulary. No file paths or code
snippets — they go stale. Exception: a decision-rich artifact from the grill
session or a prototype (state machine, schema, type shape) may be inlined,
trimmed to the parts that encode the decision.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

#N — or "None - can start immediately"
```

Do not close or modify the parent issue.
