---
name: grill-me
description: Interview the user about a plan or design until every decision has been made and the two of you share the same understanding. Only invoked explicitly by the user via /grill-me.
disable-model-invocation: true
---

## How to talk to the user

Write to the user in plain, direct English, the way you would explain the work to a colleague. Use full sentences and everyday words, with no slogans and no invented terms. Lead with what you found, what you did, and what happens next. The full guide is [STYLE.md](../../STYLE.md).

## The method

Interview me about every part of this plan until we share the same understanding of it. Some decisions depend on others; work through them one at a time, starting with the ones that nothing else depends on. For each question, give your recommended answer.

Ask the questions one at a time with AskUserQuestion, and wait for my answer before asking the next one. If a question can be answered by exploring the codebase, explore the codebase instead of asking me.

Do not stop until we share the same understanding of the plan and every decision has been made.
