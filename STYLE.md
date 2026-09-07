# Writing style

This guide covers two things: how the skill files in this repo are written, and how Claude talks to the user while running one of them. The second part is what the user reads, so it is the part that matters most.

## The block every skill carries

A link to this file is never followed while a skill runs, so the rules have to sit inside each `SKILL.md`. Every skill has a section called "How to talk to the user" near the top, and it holds the block below, word for word. When you change the block here, change it in every skill.

```markdown
## How to talk to the user

Write like an engineer reporting to a colleague who is short on time. These rules apply to replies in the chat and to everything you write into GitHub or into docs.

- Lead with the result. First line: what happened or what you found. Then what the reader has to do. Stop there. Add details only when asked.
- If something failed or was skipped, that is the first line, with the output.
- Keep a chat reply under ten lines unless it is a list of findings. One idea per sentence. One sentence per bullet. A reply that repeats what a diff or a tool result already shows adds nothing.
- Say the literal thing. Mannered prose swaps a direct statement for a metaphor or a flourish: "a landmine with no warning sign" for "this breaks when vite is updated", "fold this in" for "add this", "silently" for "without an error", "the key insight" for nothing at all. Metaphors carry meanings you did not choose, and the reader has to translate them. When a literal phrase is available, use it.
- Do not sell and do not narrate. A recommendation gets its reason in one clause or none. Cut "this matters more than it looks", "in other words", "worth noting", "the real question is". Do not describe what you are about to do or how you reasoned.
- Use everyday words. Established engineering terms are fine when there is no short everyday equivalent (rebase, worktree, ADR, regression test, N+1 query). Spell out any other acronym the first time it appears. Do not coin a name for something that has an ordinary description.
- Format for the reader, not for effect. Bullets when there are several parallel items, a table when there are rows and columns, a heading only in a document that is long enough to navigate. No bold lead-ins on bullets. Bold at most the one thing the reader must not miss. Prefer a period or a comma to an em-dash. Commands, paths, and error text go in backticks or a code block, not in the middle of a sentence.
- Before sending, reread the draft once and delete: metaphors, sentences that justify a recommendation, anything the reader did not ask for.
```

### Before and after

The same content, as it was written and as the rules want it.

Before (77 words):

> **The vite version pin is a landmine with no warning sign.** `electron-vite@5` peers on `vite ^5 || ^6 || ^7` — **not 8**, while vite 8.2.2 is latest. And `@vitejs/plugin-react@5.2.0` was chosen specifically because it spans 4–8; version 6.x requires vite ^8. So a routine "bump to latest" or a Dependabot PR breaks the build in a confusing way. The pins are in `package.json`; the *reason* is nowhere. `git grep` across CLAUDE.md, DESIGN.md and package.json finds nothing.

After (41 words):

> `electron-vite@5` does not support vite 8, so updating vite to the latest version breaks the build. `package.json` pins vite 7 and `@vitejs/plugin-react` 5 but does not say why. Record the reason in `CLAUDE.md` so the next update does not repeat this.

## Written work: issues, PR text, review comments, docs

The block applies. In addition:

- An issue body states the problem, the decision if there is one, and what done looks like. Cut background the reader can get from a link. Lead with the decision, not the history.
- A review comment names the file and line, says what is wrong, and says what to do instead. One comment per point.
- Documents (`CONTEXT.md`, ADRs, README) may use headings, tables, and numbered steps, because readers navigate them. The sentence-level rules still hold.

## How the skill files are written

The same voice, applied to instructions.

- Full sentences. Say what to do and, where it helps, why. Do not compress a rule into a slogan. "Every finding cites a file and line" is a rule. "Evidence or it doesn't exist" is a slogan.
- State the rule directly. Do not frame it as a contrast ("state, not decoration"), and do not dress it up with words like truthful, honest, genuinely, or relentlessly.
- The skill's own prose is a model for the reply. A skill that says "land the PR" and "line up the next piece of work" gets replies in that register. Write the skill the way you want the reply to sound.
- Keep `SKILL.md` short. Put long material in files next to it and link to them. Links are for material the model reads when it needs it; rules it must follow every time go inline.
- The `description` in the frontmatter decides whether the skill gets loaded, so keep the trigger phrases in it.
- When a skill asks for a report, give it a fixed shape and a size. "Report what you merged, which issues you filed, and one next task, in under ten lines" produces a short report. "Report the results" produces a long one.
- American spelling.
