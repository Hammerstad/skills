# hammerstad-skills

Personal collection of AI/LLM **skills** and **custom agents**. Several skills are borrowed from [Matt Pocock](https://github.com/mattpocock/skills) and adapted to my use where appropriate.

## Installing

There are two distribution routes, and they serve different content:

### 1. `skills` CLI (cross-agent, **skills only**)

The [Vercel `skills` CLI](https://github.com/vercel-labs/skills) works with
75+ coding agents (Claude Code, Cursor, Codex, ...) but only distributes
skills - it discovers `skills/<name>/SKILL.md` and installs them into the
target agent. It does **not** handle custom agents.

```sh
npx skills@latest add <github-user>/skills
```

### 2. Claude Code plugin (skills **and** agents)

This repo doubles as a Claude Code plugin marketplace. Installing the plugin
gives you everything: skills from `skills/` AND custom agents from `agents/`
(plus commands/hooks if added later).

```sh
claude plugin marketplace add <github-user>/skills
claude plugin install hammerstad-skills@hammerstad-skills
```

For local development, add the marketplace from disk instead:

```sh
claude plugin marketplace add /your/code/folder/skills
```

## Skills vs. agents, in one line each

- **Skill**: instructions loaded *into the current conversation* when relevant
  - same context, same model.
- **Agent**: a separate subprocess with its own context window, system prompt,
  and tool restrictions, which reports back when done.
