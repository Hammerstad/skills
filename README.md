# hammerstad-skills

Personal collection of AI/LLM **skills** for software development. Several are
borrowed from [Matt Pocock](https://github.com/mattpocock/skills) and adapted;
the rest are built around one workflow.

## The workflow

The skills form a pipeline around GitHub issues and PRs, driven by the labels
defined in [skills/labels](skills/labels/SKILL.md):

```
idea/bug
  → create-issue / triage             (capture and route onto the board)
  → grill-with-docs / diagnose        (settle the design / find the cause)
  → to-issues                         (thin end-to-end slices, labeled)
  → implement                         (ready-for-agent issue → PR)
  → review-pr ⇄ answer-review         (ready-for-review ⇄ review-feedback)
  → finish-pr                         (ready-to-merge → merged, next work suggested)
```

`review-security` and `review-performance` are focused reviews that `review-pr`
runs when a PR touches their areas. `improve-codebase-architecture` enters the
pipeline from the side: it surveys the codebase for modules that leak their
internals, grills the chosen one with the user, and hands the design to
`to-issues`. `grill-me` is a quick grill that only the user can invoke;
`domain-modeling` keeps `CONTEXT.md` and the ADRs up to date during grill
sessions.

Two skills run the pipeline over the whole backlog instead of one issue at a
time. [grill-issues](skills/grill-issues/SKILL.md) works through every
`needs-grilling` issue, explaining each one in plain English before grilling
it into a spec. [work-loop](skills/work-loop/SKILL.md) then works through the
`ready-for-agent` issues unattended: `implement`, then `review-pr` and
`answer-review` in fresh sub-agents, then `finish-pr`, then `triage`, and
repeat. Only the user can invoke `work-loop`, since it runs until the backlog
is empty.

**These skills are a system.** They reference each other (`finish-pr` reuses
`review-pr`'s queries, `implement` trusts what the `labels` mean, the focused
reviews deliver through `review-pr`). Install them as a set. Picking individual
skills leaves references pointing at skills that are not there.

## Installing

Built for Claude: the CLI, the desktop app, and the VS Code extension. The
skills assume Claude Code capabilities (AskUserQuestion option cards, Artifacts)
rather than a lowest-common-denominator harness.

```sh
claude plugin marketplace add Hammerstad/skills
claude plugin install hammerstad-skills@hammerstad-skills
```

For local development, add the marketplace from disk instead:

```sh
claude plugin marketplace add <path-to-this-repo>
```

## Per-repo setup

The workflow skills expect the labels to exist in the target repo. Run the
[setup-repo](skills/setup-repo/SKILL.md) skill once per repo (labels, plus
optional branch protection that matches the workflow). On repos without the
labels, the skills still do what they can and say what they skipped: reviews
still work, while `implement` and `finish-pr` offer to run setup instead of
guessing.

## Writing style

The skills, and Claude's replies while running them, are written in plain
English. The rules are in [STYLE.md](STYLE.md). Every skill carries the same
"How to talk to the user" block near the top, copied from STYLE.md word for
word, because a link to the file is not followed while a skill runs.

`scripts/measure-replies.py` reads the transcripts under `~/.claude/projects`
and reports reply length and banned phrasing per skill. Run it before and after
a change to the style rules to see whether the change did anything.

## Adding a skill

1. Create `skills/<skill-name>/SKILL.md` with `name` and `description`
   frontmatter.
2. The `description` carries the triggers. It is the only part an agent sees
   before deciding to load the skill. Add `disable-model-invocation: true` for
   skills that should only run when explicitly invoked.
3. Copy the "How to talk to the user" block from STYLE.md, unchanged, and follow
   the rest of STYLE.md for the skill's own text. Give every report the skill
   asks for a fixed shape and a size.
4. Keep `SKILL.md` short; push long material into files next to it
   (`reference/`, formats, scripts) and link them.
