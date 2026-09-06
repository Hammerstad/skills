---
name: grill-with-docs
description: Grill the user about a plan, decision, or idea until every open question is decided, and write the outcome into CONTEXT.md and ADRs as you go. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

# Grill With Docs

Interview the user until the two of you agree on the whole plan, and write the decisions down as they are made.

## How to talk to the user

Write to the user in plain, direct English, the way you would explain the work to a colleague. Use full sentences and everyday words, with no slogans and no invented terms. Lead with what you found, what you did, and what happens next. The full guide is [STYLE.md](../../STYLE.md).

## The method

Treat the plan as a set of decisions where some depend on others. Deciding one thing opens up the questions that hang off it.

Work in rounds. In each round, ask every question whose prerequisites are already decided, so that you are never guessing at an answer you have not heard yet. Then wait for the user's answers before starting the next round. A question that depends on another question still open in this round waits for a later round.

## Presenting a round

Do not present a round as a long block of text. Use AskUserQuestion, which shows the questions as option cards:

- Split the round into consecutive calls of up to 4 questions each until the round is done. Only then work out the next round.
- For each question, give 2-4 concrete options. Put your recommended answer first with "(Recommended)" after it, and give the trade-off of each option in its description. Use multi-select where the choices are not mutually exclusive.
- An open-ended question with no natural options (naming something, describing an experience) is asked as plain text in the same round instead of being forced into cards.

If the harness does not have AskUserQuestion, fall back to numbered text:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each set of answers changes the picture: decided questions unblock the questions that depended on them. Work out the new set of askable questions and run the next round.

## Facts are yours to find, decisions are the user's

When a question needs a fact from the environment (the filesystem, tools, and so on), look it up yourself. Do not ask the user for anything you could find. Use a sub-agent only when the lookup is a wide investigation across many files that would otherwise hold up the round. One sub-agent is enough, and a lookup that a few tool calls would settle does not need one at all. While that investigation runs, only the questions that depend on it wait. Ask the rest of the round now.

Every decision goes to the user. Put it to them and wait for the answer.

## Writing the docs

As decisions are made, run the `domain-modeling` skill alongside: check the user's terms against `CONTEXT.md`, sharpen vague language, and write the docs the moment something is decided. Resolved terms go into `CONTEXT.md`, and hard-to-reverse trade-offs go into ADRs. This is what the "with docs" in the name means. A session that only produces chat has lost its output.

## When you are done

The session is done when there are no askable questions left: every decision has been visited and nothing is left silently assumed. Do not act on the plan until the user confirms that you share the same understanding of it.
