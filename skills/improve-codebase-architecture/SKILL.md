---
name: improve-codebase-architecture
description: Survey a codebase for shallow modules worth deepening, then grill the chosen one into a design decision. Use when the user says "improve the architecture", "/improve-codebase-architecture", asks what's architecturally rotting, or when diagnose finds a bug the architecture allowed.
---

# Improve Codebase Architecture

Find places where the codebase makes future work harder than it needs to be, pick one with the user, and grill it into a decision the pipeline can act on. **This skill never changes code** — not during the survey, not during the grilling. Its output is a settled design that `to-issues` turns into slices and `implement` builds.

Read `CONTEXT.md` (if it exists) and the ADRs before surveying: candidates are named in the project's own domain vocabulary, and an ADR that already rejected a deepening means it does not come back as a candidate.

## Deep and shallow

A **deep** module hides substantial behavior behind a small, stable interface. A **shallow** one exposes an interface nearly as complex as its implementation, leaking its details across the seam. Shallowness is what this skill hunts — not size, not ugliness, not test coverage.

**The deletion test decides.** For each candidate ask: if this module vanished and its callers absorbed it, would complexity *concentrate* or *scatter*? Only "concentrates" is a real candidate — everything else is a module doing its job, or a preference dressed up as architecture.

## 1. Survey

Whole repo unless the user names a path. **Do not bias by recency** — the worst architecture is worth knowing about wherever it lives, and code that looks dormant is often dormant *because* touching it is unpleasant.

Friction signals worth chasing:

- **Interface ≈ implementation** — a module whose callers must know its internals to use it correctly.
- **Testability-only extraction** — pure functions carved out purely to be testable, leaving the caller holding the real logic.
- **Cross-seam leakage** — types, error shapes, or invariants from one module's insides appearing in another's signatures.
- **Scattered concept** — one domain idea whose rules live in three files that must change together, with nothing naming the idea.
- **Pass-through layers** — a module that mostly forwards, translating names without adding meaning.
- **Repeated caller ceremony** — the same setup/teardown/error-handling dance at every call site.

Rank by deletion-test strength × friction, and badge each candidate:

| Badge | Meaning |
|---|---|
| **Strong** | Deletion test passes clearly, friction is real and observable in the code |
| **Worth exploring** | Plausible deepening; the payoff depends on where the project goes next |
| **Speculative** | Surfaced for completeness — generally safe to ignore |

## 2. Report and stop

Publish the survey as an **Artifact**: one card per candidate with its badge, the files involved, the friction in one or two sentences, the proposed deepening in plain English, and what the deletion test showed. Load the `artifact-design` skill before writing it. If the Artifact capability isn't available, deliver the same content as a numbered terminal list — never silently drop candidates to fit.

Then ask which one to explore, via AskUserQuestion: the top candidates as options, badge and one-line payoff in each description, your recommendation first. **No forward motion without an explicit pick** — not into design, and never into code.

## 3. Grill the chosen candidate

Interview the user in rounds, exactly as `grill-with-docs` works the frontier — AskUserQuestion, 2-4 options per question, your recommended answer first with "(Recommended)", trade-offs in the descriptions. Finding facts is your job; the decisions are the user's.

The frontier for a deepening is architecture-specific. Work it roughly in this order, each round unblocking the next:

1. **Constraints** — what must not change: public API, wire format, persistence shape, performance envelope, deployment boundaries.
2. **The seam** — where exactly does the new interface sit, and what ends up behind it? Name it in domain vocabulary.
3. **Interface shape** — the smallest surface that serves every current caller. Walk the awkward callers explicitly; one caller that doesn't fit is how a deep module turns back into a shallow one.
4. **What gets simpler** — name the caller ceremony, the leaked type, or the scattered rule this removes. If nothing concrete goes away, the candidate was speculative — say so and stop.
5. **Test implications** — what becomes testable through the interface that currently needs internals, and which existing tests are testing the seam rather than the behavior.
6. **Migration** — one move or incremental? What lands first, what can co-exist, what is the blast radius per step.

Run `domain-modeling` alongside: resolved terms go into `CONTEXT.md` as they crystallise, and the deepening itself is exactly the hard-to-reverse, non-obvious, genuine-trade-off decision that earns an ADR.

## 4. Hand off

Confirm the shared understanding, then hand the settled design to `to-issues` — tracer-bullet slices, labeled per the `labels` skill. The migration order from the grilling is the slice order.

**Record rejections too.** A candidate the user rejects on its merits (not merely deferred) gets an ADR saying what was proposed and why it was turned down. That is what stops the next survey from resurfacing it.
