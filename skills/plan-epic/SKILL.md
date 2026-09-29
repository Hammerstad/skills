---
name: plan-epic
description: Plan a piece of work too big for one grill session (an epic, a large feature, a migration) as an epic issue on GitHub with one sub-issue per open decision, then resolve those decisions one session at a time until nothing is left to decide and to-issues can split it into build issues. Create a new epic only when the user asks ("plan this epic", "map out this feature", "this is too big to grill"). grill-issues also invokes it to work a ticket when it meets an issue whose parent carries the `epic` label.
---

# Plan Epic

Use this when the user has an idea that is too big to settle in one grill session and whose details are not known yet. This skill records the idea as an **epic issue** on GitHub. The epic issue states the goal, and it has one sub-issue, called a **ticket**, for each question that has to be decided before the work can be built. Each later session resolves one ticket. This skill only records decisions and writes no code. When nothing is left to decide, `to-issues` splits the result into build issues.

## How to talk to the user

Write like an engineer reporting to a colleague who is short on time. These rules apply to chat and to everything you write into GitHub or into docs.

- Lead with the result: what happened or what you found, then what the reader has to do. If something failed or was skipped, that is the first line, with the output. Add details only when asked.
- Keep a chat reply under ten lines unless it is a list of findings. One idea per sentence.
- Say the literal thing. No metaphors or flourishes ("a landmine", "fold this in" for "add this"), no filler ("worth noting", "the key insight"), no coined names for things that have an ordinary description. Spell out an acronym the first time unless it is an established engineering term.
- Do not sell and do not narrate. A recommendation gets its reason in one clause or none. Do not describe what you are about to do or how you reasoned.
- Format plainly: bullets only for parallel items, no bold lead-ins, a period or a comma over an em-dash, commands, paths, and error text in backticks. Before sending, reread once and delete metaphors, justifications, and anything the reader did not ask for.

## Rules

- **Resolve questions, and do not build.** Every ticket answers a question. The epic is finished when nothing is left to decide. Even then, `to-issues` and `implement` do the building, not this skill.
- **One ticket per session.** A session resolves one ticket, updates the epic issue, and stops. The user starts a new session for the next ticket. Research tickets are the exception: each one runs in its own sub-agent.
- **Assign the ticket before working on it.** Assign it to the user before reading anything else. Other sessions skip assigned tickets, so an open, unassigned ticket is free to take.
- **Refer to issues by title.** In everything the user reads, name a ticket by its title with the number in the link, never by a bare `#42`.
- **Look up facts yourself, and ask the user for decisions.** Read the code, the docs, and the tracker before asking anything. Every decision goes to the user as a question, as `grill-with-docs` describes.

## The epic issue

The epic issue carries the labels `epic` and `needs-grilling` (see the `labels` skill). Its tickets are native GitHub sub-issues of it. The body is an index: each decision gets one line with a link to the ticket that holds the full answer, and the answer is not repeated in the body. Open tickets are not listed in the body. Find them with the query under "GitHub commands".

Epic issue body:

```markdown
## Goal

<What finished looks like: the spec, decision, or change this epic leads to. One or two lines. Every session reads this before picking a ticket.>

## Notes

<Domain background, skills every session should load, standing preferences for this work.>

## Decisions so far

<!-- one line per closed ticket, in the order they closed -->

- [<ticket title>](<url>): <one-line answer>

## Not yet specified

<!-- questions you expect to come up but cannot state precisely yet; see "Not yet specified" -->

## Out of scope

<!-- work ruled outside the goal, and why; see "Out of scope" -->
```

Epic issues created before this format use the heading `## Destination` for the goal. Treat it as the same section.

## Tickets

Each ticket is a sub-issue of the epic issue. Its body is one question, small enough for one session to resolve:

```markdown
## Question

<the decision or investigation this ticket resolves, and why the goal depends on it>

## Type

grilling | research | task

## Blocked by

#N - or "None"
```

The answer does not go in the body. It is posted as a comment when the ticket closes.

### Types

There are three types. Each one uses an existing state label, so `triage`, `grill-issues`, and `finish-pr` handle tickets without changes.

| Type | Who resolves it | Label while open |
|---|---|---|
| grilling | The user, in conversation. This is the default. Resolve it with `grill-with-docs` and `domain-modeling`. When the user needs something concrete to react to, write a rough draft or outline first and link it from the ticket. | `needs-grilling` |
| research | A sub-agent, without the user. It reads documentation, third-party APIs, or the codebase to find a fact that a decision depends on. See "Research". | `needs-input` |
| task | Manual work that a decision depends on: signing up for a service, getting access, moving data so its shape can be seen. There is nothing to decide, but the next decision cannot be made until the task is done. The agent does it when it can. Otherwise the body holds a checklist for the user. | `needs-input` |

A grilling ticket is never answered without the user. If the user is not there, the ticket stays open.

A ticket that depends on another open ticket also carries `blocked`, has `Blocked by #N` in its body, and has the native blocked-by relation set (see "GitHub commands"). Remove `blocked` when all its blocking tickets have closed.

A session picks from the **available tickets**: sub-issues that are open, unassigned, and not `blocked`.

## Not yet specified

Do not create a ticket for a question you cannot state yet. The Not yet specified section lists the questions you expect to come up but cannot phrase precisely, because they depend on answers that are still open. Resolving a ticket often makes some of them precise enough to become tickets. When one does, create the ticket and remove the entry, so that each question is recorded in one place.

Create a ticket when you can state the question precisely, even if you cannot answer it yet or it is blocked. Otherwise add it to Not yet specified, and do not split it in advance: one entry may later become several tickets, or none.

The section does not hold decided questions, questions that already have a ticket, or work that is out of scope.

## Out of scope

The goal sets the scope. Work beyond the goal goes in the Out of scope section, with one line saying why. It never becomes a ticket in this epic. If it comes up again later, it needs a new epic.

When an existing ticket turns out to be beyond the goal, close it with a comment saying so, add a line to Out of scope that links it, and leave it out of Decisions so far.

## Creating an epic

The user starts this with a rough idea. Creating an epic creates issues, so do it only when the user asks.

1. **Agree on the goal.** Run `grill-with-docs` and `domain-modeling` on one question: what does finished look like? A spec, a decision, or a change to existing code. Settle this first, because it sets the scope for everything else.
2. **List the open questions.** Grill again, covering the whole area broadly rather than one part in depth. List every decision that has to be made, and which ones can be worked on now. If no question has to wait for another, the work fits in one grill session and needs no epic. Say so and ask how the user wants to proceed.
3. **Create the epic issue** with the body above: Goal and Notes filled in, Decisions so far empty, the questions you cannot state yet under Not yet specified, and anything ruled out under Out of scope. Labels: `epic`, `needs-grilling`.
4. **Create the tickets** you can state precisely, one sub-issue each, with the label for its type. Then, in a second pass, add the blocked-by relations, the `Blocked by #N` lines, and the `blocked` labels. The second pass is needed because issues must exist before they can refer to each other's numbers.
5. **Start the research.** For each research ticket, start a sub-agent with the method under "Research", all in parallel. Wait for them to finish, record each result as step 4 of "Working a ticket" describes, then continue.
6. **Stop.** Report the epic by title with its link, how many tickets are available, and how many are blocked. Creating an epic does not resolve any grilling tickets.

## Working a ticket

The user invokes this with an epic or ticket number or URL, or `grill-issues` invokes it when it meets a ticket whose parent issue has the `epic` label.

1. **Read the epic issue**: its body only, not every ticket. Read the Goal, Notes, and Decisions so far. Load any skills the Notes name.
2. **Pick the ticket.** If the user named one, take it. Otherwise take the first available ticket in sub-issue order. Assign it to the user before doing anything else.
3. **Resolve it** according to its type. Grilling: run `grill-with-docs` and `domain-modeling` on the ticket's question, and read related closed tickets, `CONTEXT.md`, and the ADRs when you need them rather than all at the start. Research: run the method under "Research". Task: do the work, or walk the user through the checklist.
4. **Record it.** Post the resolution comment (shape below), close the ticket, and add one line to Decisions so far in the epic issue. Hard-to-reverse trade-offs go into an ADR and agreed terms into `CONTEXT.md`, as `domain-modeling` describes. Check that this happened.
5. **Update the epic issue.** Create tickets for the questions the answer made precise, set their blocked-by relations, and remove the matching entries from Not yet specified. Remove `blocked` from tickets whose blocking tickets have now all closed. If the answer shows that a ticket is beyond the goal, move it to Out of scope. If the answer makes other tickets wrong or unnecessary, edit or close them. Start sub-agents for any new research tickets.
6. **Stop**, unless the epic is finished. Report in two or three lines: the ticket by title and its answer, what was written to the docs, how many tickets are available, and how many are blocked.

Resolution comment:

```markdown
## Decision

<the answer, complete enough that nobody needs the chat>

## Why

<the reason and the options rejected, one line each>

## Written to

- `CONTEXT.md`: <term> - or "nothing"
- `docs/adr/NNNN-<slug>.md` - or "no ADR"

## Opened

- [<new ticket title>](<url>) - or "nothing"
```

## Research

A sub-agent resolves a research ticket without the user. Give it the ticket's question, the epic's Goal and Notes, and this method:

1. Read the sources the question points at: documentation, an API, a library, the codebase. Prefer primary sources and quote them. For facts that may have changed since your training (versions, limits, prices, API behavior), check a current source even when you are confident.
2. Answer the question. Say plainly when the sources do not settle it.
3. Post a comment in the shape below, close the ticket, and return the one-line answer for Decisions so far.

Research comment:

```markdown
## Question

<repeated from the ticket>

## Answer

<the finding>

## Sources

- <URL or path, what it says>

## Open points

- <what the sources did not settle, and what would> - or "none"
```

The sub-agent does not create tickets or edit the epic issue. The session that started it does that, using the answer.

## Finishing the epic

The epic is finished when it has no open sub-issues and Not yet specified is empty. Confirm with the user that nothing is left to decide. Then:

1. Run `to-issues` with the epic issue as the parent. Every build issue's Parent field points at the epic issue, and each is labeled as the `labels` skill describes.
2. Close the epic issue with a comment listing the build issues by title.

## GitHub commands

Sub-issue and dependency endpoints take the database id, not the issue number:

```sh
gh api repos/{owner}/{repo}/issues/<n> --jq .id
```

Create the epic issue and a ticket, then attach the ticket:

```sh
gh issue create --title "<epic title>" --label epic,needs-grilling --body-file epic.md
gh issue create --title "<ticket title>" --label needs-grilling --body-file ticket.md
gh api -X POST repos/{owner}/{repo}/issues/<epic>/sub_issues -F sub_issue_id=<ticket db id>
```

Block ticket B on ticket A (native relation, body line, and label):

```sh
gh api -X POST repos/{owner}/{repo}/issues/<B>/dependencies/blocked_by -F issue_id=<A db id>
gh issue edit <B> --add-label blocked
```

Available tickets of an epic (open, unassigned, not blocked):

```sh
gh api repos/{owner}/{repo}/issues/<epic>/sub_issues --paginate \
  --jq '.[] | select(.state=="open" and (.assignees|length)==0 and ([.labels[].name]|index("blocked")|not)) | "\(.number) \(.title)"'
```

Assign and close:

```sh
gh issue edit <n> --add-assignee @me
gh issue comment <n> --body-file resolution.md
gh issue close <n>
```

If the repo does not have the `epic` label, offer `setup-repo` and stop.
