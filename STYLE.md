# Writing style

This guide covers two things: how the skill files in this repo are written, and how Claude talks to the user while running one of them. The same rules apply to both.

## The rules

Write the way you would explain the work to a colleague who knows the field but was not in the room.

- **Full sentences.** Say what to do and, where it helps, why. Do not compress a rule into a slogan or a fragment. "Every finding cites a file and line" is a rule. "Evidence or it doesn't exist" is a slogan.
- **Everyday words.** Do not coin a name for something that has an ordinary description. "The questions you can ask now" needs no special term.
- **Established engineering terms are fine** when there is no short everyday equivalent: bisect, feedback loop, ADR, regression test, rebase, worktree, N+1 query. Spell out an acronym the first time it appears.
- **State the rule directly.** Do not frame it as a contrast ("state, not decoration"), and do not dress it up with words like truthful, honest, genuinely, or relentlessly. If the rule needs a reason, give the reason.
- **No metaphors in place of an explanation.** For example, "the reviewer is up next" says what "the ball is in the reviewer's court" means.
- **Keep the structure that helps a reader.** Headings, numbered steps, checklists, tables, and code blocks are all fine. Use bold for the few things on a page the reader must not miss.
- **American spelling.**

## When talking to the user

- Lead with the outcome: what you found, what you did, and what happens next.
- Keep it short by leaving things out. Packing more into each sentence does not make it quicker to read.
- If something failed or was skipped, say so first, and show the output.
- Put commands, file paths, and error text in code blocks or backticks, and keep them out of the middle of sentences where you can.
- Do not narrate your own reasoning or announce what you are about to say.

## When writing or editing a skill

- Keep `SKILL.md` short. Put long material in files next to it and link to them.
- The `description` in the frontmatter decides whether the skill gets loaded, so keep the trigger phrases in it. Write the rest of it in the same plain voice.
- Every skill has a short "How to talk to the user" section near the top that links here. Copy it from an existing skill so the wording stays the same everywhere.
