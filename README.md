# hammerstad-skills

Personal collection of AI/LLM **skills** for software development. Several are
borrowed from [Matt Pocock](https://github.com/mattpocock/skills) and adapted;
the rest are built around one workflow.

## The workflow

The skills form a pipeline around GitHub issues and PRs, driven by the label
state machine defined in [skills/labels](skills/labels/SKILL.md):

```
idea/bug
  → create-issue / triage             (capture and route onto the board)
  → grill-with-docs / diagnose        (settle the design / find the cause)
  → to-issues                         (tracer-bullet slices, labeled)
  → implement                         (ready-for-agent issue → PR)
  → review-pr ⇄ answer-review         (ready-for-review ⇄ review-feedback)
  → finish-pr                         (ready-to-merge → merged, next work suggested)
```

`review-security` and `review-performance` are deep lenses `review-pr` pulls
in when a PR touches their domains. `improve-codebase-architecture` enters the
pipeline from the side: it surveys for shallow modules, grills the chosen one,
and hands the design to `to-issues`. `grill-me` is a user-invoked-only
quick-grill; `domain-modeling` keeps `CONTEXT.md` and ADRs honest during
grill sessions.

[work-loop](skills/work-loop/SKILL.md) drives the right-hand half of the
pipeline unattended — oldest `ready-for-agent` issue → `implement` →
`review-pr` ⇄ `answer-review` in fresh sub-agents → `finish-pr` → `triage` →
repeat until the pool is empty. It is user-invoked only, since it runs until
the backlog is drained.

**These skills are a system.** They reference each other (`finish-pr` reuses
`review-pr`'s queries, `implement` trusts the `labels` guarantees, the lenses
deliver through `review-pr`). Install them as a set — cherry-picking
individual skills leaves dangling references.

## Installing

Built for Claude — the CLI, the desktop app, and the VS Code extension. The
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

The workflow skills expect the label taxonomy to exist in the target repo —
run the [setup-repo](skills/setup-repo/SKILL.md) skill once per repo (labels,
plus optional branch protection aligned with the workflow). Skills degrade
loudly but not fatally on repos without it: reviews still work, while
`implement` and `finish-pr` offer setup instead of guessing.

## Adding a skill

1. Create `skills/<skill-name>/SKILL.md` with `name` and `description`
   frontmatter.
2. The `description` carries the triggers — it is the only part an agent sees
   before deciding to load the skill. Add `disable-model-invocation: true` for
   skills that should only run when explicitly invoked.
3. Keep `SKILL.md` short; push long material into files next to it
   (`reference/`, formats, scripts) and link them.
