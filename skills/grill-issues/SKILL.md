---
name: grill-issues
description: Work through the needs-grilling issues one at a time, oldest first - explain each in plain English, grill it into a spec, and write the outcome back to the issue. Use when the user says "grill the backlog", "/grill-issues", "grill all needs-grilling issues", or asks to get the tracker's under-specified issues spec'd.
disable-model-invocation: true
---

# Grill Issues

Take the open `needs-grilling` issues (see the `labels` skill) and work through them one at a time. Each issue gets explained, grilled with `grill-with-docs`, and written back to GitHub as a real spec.

The user is a technical product manager. They own the product decisions and know the domain, and they have not read the code. Everything you put in front of them is in plain English.

## How to talk to the user

Write to the user in plain, direct English, the way you would explain the work to a colleague. Use full sentences and everyday words, with no slogans and no invented terms. Lead with what you found, what you did, and what happens next. The full guide is [STYLE.md](../../STYLE.md).

## Rules

- **Oldest first**, unless the invocation narrows it (`/grill-issues 42`, `label:bug`, "just the oldest three").
- **Explain before you ask.** Every issue opens with the brief described in step 2. The user should never have to work out what an issue is about from your first question.
- **No jargon in anything the user reads.** Describe behavior and consequences rather than classes, layers, or patterns. Name a file only when they need to open it. Explain a term the first time you need it, or find a plainer one.
- **Describe options by their outcomes.** "Slower to build, but the import cannot lose rows" is better than "use a transactional outbox". The user picks between outcomes, costs, and risks.
- **Facts are yours to find, decisions are the user's.** Read the code before asking anything. Never ask the user something the repo can answer.

## Workflow

### 1. Build the list

```sh
gh issue list --state open --label needs-grilling --json number,title,createdAt,body,labels,url,comments
```

Sort oldest first by `createdAt`. Show the list (number, title, age, one plain line each), then start on the first.

Three kinds of issue leave the list instead of being grilled. Say which kind and why, and let the user confirm:

- **`blocked`**: the design depends on an open issue, so grilling it now means guessing at that outcome. Skip it until the blocker closes.
- **A bug with no known cause**: there is nothing to design yet. Relabel it `needs-diagnosis` and point at `diagnose`.
- **Already built, or clearly not wanted**: close it with a one-paragraph explanation and a pointer to what exists. If it is debatable, that decision belongs to `triage`.

If the repo has none of the workflow labels, offer `setup-repo` and stop.

### 2. Brief the issue

Read the issue and every comment, then read enough of the code to know what already exists in the area. Read `CONTEXT.md` and the ADRs first if the repo has them.

Then present it, briefly:

```
**#42 — <title>**

**What it asks for:** one or two sentences, in the user's language.
**Why it exists:** who wanted it and what problem it solves. Say so if the issue never explains.
**What's already there:** what the product does today in this area.
**What's undecided:** the open questions, as questions. These become the grilling.
```

If the code contradicts the issue (the behavior it describes does not exist, or already works), say so here, before grilling something that is not true.

### 3. Grill it

Run the `grill-with-docs` skill on the issue, with two adjustments for this audience:

- Options in the question cards are described by what they cost and what they get, never by the technique behind them.
- When a decision only makes sense with background, give the background in the question instead of assuming the user has it.

Anything the user cannot answer themselves (it needs the original reporter, or an answer from outside) stops being a grilling question. It goes to step 4 as a `needs-input` question instead of being guessed at.

### 4. Write it back

Everything this session produces goes on GitHub:

- **Rewrite the issue body** as the agreed spec: what should happen, the decisions made and why, and what is out of scope on purpose. Keep the original description below a `---` if it is worth keeping.
- **Relabel** as the `labels` skill describes: `ready-for-agent` once the body meets that label's definition (everything needed to implement is in it, and it depends on no open issue), otherwise `needs-input` with the specific question in a comment.
- **Split if it grew.** If grilling turned one issue into several pieces of work, hand it to `to-issues` and close or narrow the original.
- `grill-with-docs` already writes agreed terms into `CONTEXT.md` and hard-to-reverse trade-offs into ADRs. Check that it happened rather than assuming.

### 5. Next, or stop

Report in one or two lines: what #42 became, its new label, anything filed alongside it, and how many issues are left. Ask whether to continue.

When the list is empty: list what got specified, what was skipped and why, and any `needs-input` questions now waiting on someone else.
