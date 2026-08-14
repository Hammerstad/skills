---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Only invoked explicitly by the user via /grill-me.
disable-model-invocation: true
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time using vscode builtin questions, and wait for the user's answer before asking the next question. If a question can be answered by exploring the codebase, explore the codebase instead.

Do not stop until we have reached a shared understanding of the plan, and all branches of the decision tree have been resolved.