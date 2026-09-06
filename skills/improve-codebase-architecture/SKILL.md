---
name: improve-codebase-architecture
description: Survey a codebase for modules whose interfaces expose too much of their insides, then grill the user about the chosen one until it becomes a design decision. Use when the user says "improve the architecture", "/improve-codebase-architecture", asks which parts of the codebase are in the worst shape, or when diagnose finds a bug that the code's structure allowed.
---

# Improve Codebase Architecture

Find the places where the codebase makes future work harder than it needs to be, pick one together with the user, and grill it into a decision the rest of the pipeline can act on. This skill never changes code, neither during the survey nor during the grilling. Its output is an agreed design that `to-issues` turns into slices and `implement` builds.

## How to talk to the user

Write to the user in plain, direct English, the way you would explain the work to a colleague. Use full sentences and everyday words, with no slogans and no invented terms. Lead with what you found, what you did, and what happens next. The full guide is [STYLE.md](../../STYLE.md).

## Before you start

Read `CONTEXT.md` if it exists and the ADRs before surveying. Candidates are named in the project's own vocabulary, and a module that an ADR already decided to leave as it is does not come back as a candidate.

## What counts as a candidate

A module is doing its job when it hides a lot of behavior behind a small, stable interface. A module is a candidate when its interface is nearly as complicated as its implementation, so that callers have to know its internals to use it correctly. That is what this skill looks for. Size, ugliness, and test coverage are not what it looks for.

The deciding question for each candidate: if this module disappeared and its callers absorbed its work, would the complexity end up concentrated in one place, or spread across all of them? Only "concentrated" makes a real candidate. Anything else is either a module doing its job or a matter of taste presented as architecture.

## 1. Survey

Cover the whole repo unless the user names a path. Do not favor recently changed code. The worst structure is worth knowing about wherever it is, and code that looks dormant is often dormant because touching it is unpleasant.

Signs worth chasing:

- **Interface as complicated as the implementation.** Callers must know the module's internals to use it correctly.
- **Extracted only to be testable.** Pure functions pulled out so they can be tested, leaving the caller holding the real logic.
- **Internals leaking across the boundary.** Types, error shapes, or invariants from one module's insides appearing in another module's signatures.
- **One concept spread over many files.** A single domain idea whose rules live in three files that must change together, with nothing that names the idea.
- **Pass-through layers.** A module that mostly forwards calls, translating names without adding meaning.
- **Repeated boilerplate at every call site.** The same setup, teardown, or error handling around every call.

Rank candidates by how clearly the deciding question comes out in their favor and by how much friction they cause today, and give each one a rating:

| Rating | Meaning |
|---|---|
| **Strong** | The deciding question comes out clearly, and the friction is real and visible in the code |
| **Worth exploring** | A plausible improvement whose payoff depends on where the project goes next |
| **Speculative** | Listed for completeness, generally safe to ignore |

## 2. Report and stop

Publish the survey as an Artifact: one card per candidate with its rating, the files involved, the friction in one or two sentences, the proposed change in plain English, and how the deciding question came out. Load the `artifact-design` skill before writing it. If Artifacts are not available, deliver the same content as a numbered list in the terminal. Never drop candidates to make it fit.

Then ask which one to explore, with AskUserQuestion: the top candidates as options, the rating and a one-line payoff in each description, your recommendation first. Do not move forward without an explicit pick, either into design or into code.

## 3. Grill the chosen candidate

Interview the user in rounds, the way `grill-with-docs` does: AskUserQuestion, 2-4 options per question, your recommended answer first with "(Recommended)", trade-offs in the descriptions. Finding facts is your job; the decisions are the user's.

The questions for this kind of change follow a rough order, where each round unblocks the next:

1. **Constraints.** What must not change: public API, wire format, storage layout, performance requirements, deployment boundaries.
2. **The boundary.** Where exactly does the new interface sit, and what ends up behind it? Name it in the project's vocabulary.
3. **The interface.** The smallest surface that serves every current caller. Walk through the awkward callers explicitly; one caller that does not fit is how a good interface turns back into a leaky one.
4. **What gets simpler.** Name the boilerplate, the leaked type, or the scattered rule that this removes. If nothing concrete goes away, the candidate was speculative. Say so and stop.
5. **Tests.** What becomes testable through the interface that currently needs internals, and which existing tests test the boundary rather than the behavior.
6. **Migration.** One move or several steps? What lands first, what can coexist, and how much could break at each step.

Run `domain-modeling` alongside: resolved terms go into `CONTEXT.md` as they are decided, and the change itself is exactly the kind of hard-to-reverse, non-obvious trade-off that deserves an ADR.

## 4. Hand off

Confirm the shared understanding, then hand the agreed design to `to-issues` for thin end-to-end slices, labeled as the `labels` skill describes. The migration order from the grilling is the slice order.

Record rejections too. A candidate the user rejects on its merits (rather than just postponing) gets an ADR saying what was proposed and why it was turned down. That is what stops the next survey from bringing it up again.
