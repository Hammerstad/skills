---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a CONTEXT.md, or recording or editing an ADR.
---

# Domain Modeling

Build and sharpen the project's domain model as you design: challenge terms, invent edge-case scenarios, and write the glossary and the decisions down the moment they are decided. Just reading `CONTEXT.md` for vocabulary is a one-line habit any skill can do and does not need this skill. This skill is for when you are changing the model rather than only using it.

## How to talk to the user

Write to the user in plain, direct English, the way you would explain the work to a colleague. Use full sentences and everyday words, with no slogans and no invented terms. Lead with what you found, what you did, and what happens next. The full guide is [STYLE.md](../../STYLE.md).

## File structure

Most repos have a single context:

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

Create files only when you have something to write. If no `CONTEXT.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## During the session

### Check terms against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, say so right away. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen vague language

When the user uses a vague or overloaded term, propose a precise one. "You are saying 'account'. Do you mean the Customer or the User? Those are different things."

### Talk through concrete scenarios

When domain relationships come up, test them with specific scenarios. Invent scenarios that probe edge cases and make the user be precise about where one concept ends and another begins.

### Compare with the code

When the user states how something works, check whether the code agrees. If you find a contradiction, point it out: "Your code cancels whole Orders, but you just said partial cancellation is possible. Which is right?"

### Update CONTEXT.md as you go

When a term is resolved, update `CONTEXT.md` right then. Do not save these up; write them as they happen. Use the format in [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

`CONTEXT.md` contains no implementation details. It is a glossary and nothing else. Do not use it as a spec, a scratch pad, or a place to record implementation decisions.

### Offer ADRs sparingly

Offer to create an ADR only when all three of these are true:

1. **Hard to reverse.** Changing your mind later would cost something real.
2. **Surprising without context.** A future reader will wonder why it was done this way.
3. **The result of a real trade-off.** There were real alternatives and you picked one for specific reasons.

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).
