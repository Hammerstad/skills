---
name: grill-issues
description: Work through the needs-grilling issues one at a time, oldest first - explain each in plain English, grill it into a spec, and write the outcome back to the issue. Use when the user says "grill the backlog", "/grill-issues", "grill all needs-grilling issues", or asks to get the tracker's under-specified issues spec'd.
disable-model-invocation: true
---

# Grill Issues

Take the `needs-grilling` pile (see the `labels` skill) and empty it, one issue at a time. Each issue gets explained, grilled with `grill-with-docs`, and written back to GitHub as a real spec.

The user is a technical product manager. They own the product decisions and know the domain; they have not read the code. Everything you put in front of them is in **plain English**.

## Contract

- **Oldest first**, unless the invocation narrows it (`/grill-issues 42`, `label:bug`, "just the oldest three").
- **Explain before you ask.** Every issue opens with the brief below. The user should never have to reverse-engineer what an issue is about from your first question.
- **No jargon in anything the user reads.** Describe behaviour and consequences, not classes, layers, or patterns. Name a file only when they need to open it. Expand a term the first time you need it, or find a plainer one.
- **Frame options as trades, not techniques.** "Slower to build, but the import can't lose rows" beats "use a transactional outbox". The user picks between outcomes, costs, and risks.
- **Facts are yours, decisions are theirs.** Read the code before asking anything — never ask the user something the repo answers.

## Workflow

### 1. Build the pile

```sh
gh issue list --state open --label needs-grilling --json number,title,createdAt,body,labels,url,comments
```

Sort oldest first by `createdAt`. Show the list — number, title, age, one plain line each — then start on the first.

Three kinds of issue leave the pile instead of being grilled; say which and why, and let the user confirm:

- **`blocked`** — the design depends on an open issue, so grilling it means guessing at that outcome. Skip until the blocker closes.
- **A bug with no known cause** — nothing to design yet. Relabel `needs-diagnosis` and point at `diagnose`.
- **Already built, or clearly not wanted** — close it with a one-paragraph explanation and a pointer to what exists (`triage` owns this call if it's debatable).

No taxonomy in the repo → offer `setup-repo` and stop.

### 2. Brief the issue

Read the issue and every comment, then read enough of the code to know what already exists in the area. `CONTEXT.md` and the ADRs first if the repo has them.

Then present it, short:

```
**#42 — <title>**

**What it asks for:** one or two sentences, in the user's language.
**Why it exists:** who wanted it and what problem it solves. Say so if the issue never explains.
**What's already there:** what the product does today in this area.
**What's undecided:** the open questions, as questions — this becomes the grilling.
```

If reading the code contradicts the issue — the behaviour it describes doesn't exist, or already works — say that here, before grilling something that isn't true.

### 3. Grill it

Run the `grill-with-docs` skill on the issue, with two adjustments for this audience:

- Options in the question cards are described by what they cost and what they get, never by their technique.
- When a decision only makes sense with background, give the background in the question rather than assuming it.

Anything the user genuinely can't answer — it needs the original reporter, or an answer from outside — stops being a grilling question: it goes to step 4 as a `needs-input` question instead of being guessed at.

### 4. Write it back

The session's output is on GitHub, not in chat:

- **Rewrite the issue body** as the settled spec: what should happen, the decisions made and why, and what is deliberately out of scope. Keep the original description below a `---` if it's worth keeping.
- **Relabel** per the `labels` skill: `ready-for-agent` once the body passes that label's test (everything needed to implement is in it, and it depends on no open issue), otherwise `needs-input` with the specific question in a comment.
- **Split if it grew.** If grilling turned one issue into several pieces of work, hand it to `to-issues` and close or narrow the original.
- `grill-with-docs` already writes settled terms into `CONTEXT.md` and hard-to-reverse trade-offs into ADRs — check it happened rather than assuming.

### 5. Next, or stop

Report in one or two lines: what #42 became, its new label, anything filed alongside it, and how many issues are left in the pile. Ask whether to continue.

When the pile is empty: list what got spec'd, what was skipped and why, and any `needs-input` questions now waiting on someone else.
