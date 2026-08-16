---
name: grill-with-docs
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled — the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier each round, then wait for the user's answers before the next round.

## Presenting a round

**Never dump a round as a wall of text.** Present the round through AskUserQuestion — the option cards:

- Chunk the frontier into consecutive calls of up to 4 questions until the round is exhausted; only then recompute the frontier.
- Per question: 2-4 concrete options, your recommended answer as the **first** option with "(Recommended)" appended, and the trade-off of each option in its description. Use multi-select where choices aren't mutually exclusive.
- A genuinely open-ended question (naming, describing an experience) that has no natural options is asked as plain text in the same round instead of being forced into cards.

In the rare harness without it, fall back to numbered text:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree — settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), look it up yourself — never ask the user for anything you could find. Delegate to a sub-agent only when the lookup is a wide multi-file investigation that would otherwise stall the round; one sub-agent, not several, and never for something a handful of tool calls settles. While a delegated exploration runs it is an unsettled prerequisite: only the questions downstream of it wait — ask the rest of the frontier now. The _decisions_ are the user's — put each to them and wait.

As decisions settle, run the `domain-modeling` skill alongside: challenge terms against `CONTEXT.md`, sharpen fuzzy language, and write the docs inline the moment something crystallises — resolved terms into `CONTEXT.md`, hard-to-reverse trade-offs into ADRs. That is what puts the docs in grill-with-docs; a session that only produces chat has lost its output.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.
