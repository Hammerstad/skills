---
name: triage
description: Sweep the issue tracker and give existing issues the correct workflow label - unlabeled issues, needs-input issues that got an answer, stale states, blockers that have closed. Use when the user says "triage", "what needs my attention on the tracker", "go through the issues", or names an issue to triage.
---

# Triage

Keep the tracker accurate. Every open issue should carry a state label that names its next action (see the `labels` skill). Triage is the sweep that makes that true for issues that came in from outside, went stale, or changed under their labels.

New thoughts do not come here; that is `create-issue`. Triage works on what already exists.

## How to talk to the user

Write to the user in plain, direct English, the way you would explain the work to a colleague. Use full sentences and everyday words, with no slogans and no invented terms. Lead with what you found, what you did, and what happens next. The full guide is [STYLE.md](../../STYLE.md).

## Disclaimer rule

Comments posted on issues written by someone else start with:

```
> *This comment was written by an AI agent during triage.*
```

Comments on the maintainer's own issues are posted without it.

## Invoked without arguments: the sweep

Present four groups, oldest first, with counts and a one-line summary per issue. The user picks what to work through:

1. **Unlabeled**: never triaged.
2. **`needs-input` with a human answer** since the label was applied. Someone replied, so the issue needs re-routing.
3. **Stale**: `needs-grilling` and `needs-diagnosis` issues that have sat untouched long enough to go out of date, and `ready-for-agent` issues that are older than the rest of the pool (are they still true?).
4. **Blockers that have closed**: `blocked` issues whose named blockers are closed, plus any label combination that should not exist (two states, or `blocked` plus `ready-for-agent`). Fix these directly as the `labels` skill describes; they need no discussion.

## Triaging one issue

1. **Gather**: the full body, all comments, labels, author, and dates. Read any earlier triage notes so that nothing gets asked twice. Check the codebase (the project's vocabulary, and the ADRs in the area).
2. **Reality checks**: (a) Is it already built? Search the codebase for the requested behavior by concept, and not only by the reporter's wording. If it exists, close with a pointer. (b) For bugs, verify the claim: try a cheap reproduction from the reported steps. If it reproduces, that is a strong basis. If it does not, that gives you a specific question for the reporter. If it needs real investigation, that is `needs-diagnosis`, and not triage work.
3. **Recommend** a category and state with one paragraph of reasoning, and wait for the user's decision. A quick instruction like "move #42 to ready-for-agent" is trusted and applied without further discussion.
4. **Apply the outcome:**
   - `ready-for-agent`: the issue body must meet the label's definition first; fold in anything established during triage.
   - `needs-grilling` or `needs-diagnosis`: the label, plus a comment only if triage established something worth recording.
   - `needs-input`: the label, plus a comment with the questions (template below).
   - **Close**: rejected or already implemented. A polite one-paragraph explanation (with a pointer to the existing implementation when that is the reason), then close.
   - `blocked`: the label plus `Blocked by #N` in the body, as the `labels` skill describes.

## Needs-input comment template

```markdown
## Triage notes

**Established so far:**
- point 1

**Still needed (@reporter or maintainer):**
- specific, answerable question 1
```

Never write "please provide more info". Every question must be answerable in one reply.

## Repos without the workflow labels

The sweep groups fall back to what exists (unlabeled issues can still be listed and discussed). Applying labels is skipped, with a note pointing at `setup-repo`.
