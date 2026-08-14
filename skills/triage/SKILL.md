---
name: triage
description: Sweep the issue tracker and route existing issues through the label state machine - unlabeled issues, answered needs-input, stale states, dead blockers. Use when the user says "triage", "what needs my attention on the tracker", "go through the issues", or names an issue to triage.
---

# Triage

Keep the tracker truthful. Every open issue should carry a state that names its next action (`labels` skill); triage is the sweep that makes that so — for issues that arrived from outside, went stale, or changed under their labels.

New thoughts don't come here — that's `create-issue`. Triage works on what already exists.

## Disclaimer rule

Comments posted on issues **authored by someone else** start with:

```
> *This comment was written by an AI agent during triage.*
```

Comments on the maintainer's own issues are posted plainly.

## Bare invocation — the sweep

Present four buckets, oldest first, with counts and a one-line summary per issue; the user picks what to work through:

1. **Unlabeled** — never triaged.
2. **`needs-input` with a human answer** since the label was applied — someone replied; re-route.
3. **Stale** — `needs-grilling` / `needs-diagnosis` sitting untouched long enough that they rot; also `ready-for-agent` issues older than the rest of the pool (are they still true?).
4. **Dead blockers** — `blocked` issues whose named blockers have closed, and any illegal label combination (two states, `blocked`+`ready-for-agent`). Fix these directly per the `labels` skill; they need no discussion.

## Triaging one issue

1. **Gather** — full body, all comments, labels, author, dates. Parse prior triage notes so nothing gets re-asked. Ground in the codebase (domain vocabulary, ADRs in the area).
2. **Reality checks** — (a) *redundancy*: search the codebase for the requested behavior by domain concept, not just the reporter's wording — already built means close-with-pointer; (b) *claim verification* for bugs: attempt a cheap reproduction from the reported steps. Reproduces → strong basis; doesn't → a specific question for the reporter; needs real investigation → that's `needs-diagnosis`, not triage work.
3. **Recommend** — category and state with one-paragraph reasoning; wait for the user's call. Quick override applies: "move #42 to ready-for-agent" is trusted and applied without ceremony.
4. **Apply the outcome:**
   - `ready-for-agent` — the issue body must pass the label's guarantee first; fold in anything established during triage.
   - `needs-grilling` / `needs-diagnosis` — label, plus a comment only if triage established something worth recording.
   - `needs-input` — label, plus a comment with the questions (template below).
   - **Close** — rejected or already implemented: polite one-paragraph explanation (pointer to the existing implementation when that's the reason), then close.
   - `blocked` — flag plus `Blocked by #N` in the body, per the `labels` skill.

## Needs-input comment template

```markdown
## Triage notes

**Established so far:**
- point 1

**Still needed (@reporter or maintainer):**
- specific, answerable question 1
```

Never "please provide more info" — every question must be answerable in one reply.

## Repos without the taxonomy

Sweep buckets degrade to what exists (unlabeled issues can still be listed and discussed); label application is skipped with a note pointing at `setup-repo`.
