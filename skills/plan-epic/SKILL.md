---
name: plan-epic
description: Plan a piece of work too big for one grill session (an epic, a large feature, a migration) as a map issue on GitHub with one sub-issue per open decision, then resolve those decisions one session at a time until nothing is left to decide and to-issues can slice it. Charting a new map starts only when the user asks ("plan this epic", "map out this feature", "this is too big to grill"). Working a ticket is also invoked by grill-issues when it meets an issue whose parent carries the `epic` label.
---

# Plan Epic

A loose idea has arrived that is too big to settle in one grill session, and the details are not known yet. This skill writes the idea down as a **map**: one GitHub issue that names where the work is going, with one sub-issue per question that has to be decided first. Sessions then resolve those questions one at a time. The output is decisions, not code. When nothing is left to decide, `to-issues` slices the result into build work.

## How to talk to the user

Write like an engineer reporting to a colleague who is short on time. These rules apply to chat and to everything you write into GitHub or into docs.

- Lead with the result: what happened or what you found, then what the reader has to do. If something failed or was skipped, that is the first line, with the output. Add details only when asked.
- Keep a chat reply under ten lines unless it is a list of findings. One idea per sentence.
- Say the literal thing. No metaphors or flourishes ("a landmine", "fold this in" for "add this"), no filler ("worth noting", "the key insight"), no coined names for things that have an ordinary description. Spell out an acronym the first time unless it is an established engineering term.
- Do not sell and do not narrate. A recommendation gets its reason in one clause or none. Do not describe what you are about to do or how you reasoned.
- Format plainly: bullets only for parallel items, no bold lead-ins, a period or a comma over an em-dash, commands, paths, and error text in backticks. Before sending, reread once and delete metaphors, justifications, and anything the reader did not ask for.

## Rules

- **Decide, do not build.** Every ticket resolves a question. The map is finished when nothing is left to decide before someone builds the thing; even then, building goes through `to-issues` and `implement`, not this skill.
- **One ticket per session.** A session resolves one ticket, updates the map, and stops. The user starts a new session for the next one. Research tickets are the exception: they run as sub-agents with their own context.
- **Claim before work.** Assign the ticket to the user before reading anything else. Other sessions skip assigned tickets. An open, unassigned ticket is free to take.
- **Refer to issues by title.** In everything the user reads, name a ticket by its title with the number in the link, never by a bare `#42`.
- **Facts are yours to find, decisions are the user's.** Read the code, the docs, and the tracker before asking anything. Every decision goes to the user through a question, as `grill-with-docs` describes.

## The map

The map is one issue labeled `epic` plus `needs-grilling` (see the `labels` skill). Its tickets are native sub-issues of it. The map is an index: it lists decisions in one line each and links to the ticket that holds the full answer. It never repeats the answer. Open tickets are not listed in the body. They are the open sub-issues, found by query.

Map body:

```markdown
## Destination

<What finished looks like: the spec, decision, or change this map leads to. One or two lines. Every session reads this before picking a ticket.>

## Notes

<Domain background, skills every session should load, standing preferences for this effort.>

## Decisions so far

<!-- one line per closed ticket, in the order they closed -->

- [<ticket title>](<url>): <one-line answer>

## Not yet specified

<!-- questions you can tell are coming but cannot state precisely yet; see "Not yet specified" -->

## Out of scope

<!-- work ruled outside the destination, with why; see "Out of scope" -->
```

## Tickets

Each ticket is a sub-issue of the map. Its body is one question, sized so one session can resolve it:

```markdown
## Question

<the decision or investigation this ticket resolves, and why the destination depends on it>

## Type

grilling | research | task

## Blocked by

#N - or "None"
```

The answer is not in the body. It is posted as a comment when the ticket closes.

### Types

Three types. Each maps to an existing state label, so `triage`, `grill-issues`, and `finish-pr` work on tickets without changes.

| Type | Who resolves it | Label while open |
|---|---|---|
| grilling | The user, in conversation. The default. Resolve with `grill-with-docs` and `domain-modeling`. When a question needs something concrete to react to, write a rough stub or outline first and link it from the ticket. | `needs-grilling` |
| research | A sub-agent alone. Reads documentation, third-party APIs, or the codebase to find a fact a decision waits on. See "Research". | `needs-input` |
| task | Manual work a decision waits on: signing up for a service, provisioning access, moving data so its shape can be seen. Nothing to decide, but the next decision cannot be made until it is done. The agent does it when it can; otherwise the body holds a checklist for the user. | `needs-input` |

A grilling ticket never answers its own questions. If the user is not there, the ticket stays open.

Tickets that depend on another open ticket also carry `blocked`, with `Blocked by #N` in the body and the native blocked-by relation set (see "GitHub commands"). `blocked` comes off when the blocker closes.

The **frontier** is the set of open sub-issues that are unassigned and not `blocked`. That is what a session picks from.

## Not yet specified

The map is incomplete on purpose. Do not create tickets for questions you cannot state yet. The **Not yet specified** section holds the questions you can see coming but cannot phrase precisely, because they depend on answers still open. Resolving a ticket usually sharpens some of them into tickets. Move each one out of the section the moment it becomes a ticket, so it lives in one place.

The test for ticket or not yet specified is whether you can state the question precisely now, not whether you can answer it now.

- Ticket when the question is sharp, even if it is blocked.
- Not yet specified when it is not. Do not pre-slice it; one entry may become several tickets, or none.

The section excludes what is decided, what is already a ticket, and what is out of scope.

## Out of scope

The destination fixes the scope. Work beyond it is out of scope, not "not yet specified". It goes in the **Out of scope** section with one line saying why. It never becomes a ticket on this map; if it comes back, it is a new map.

When an existing ticket turns out to be beyond the destination, close it with a comment saying so, add a line to **Out of scope** linking it, and do not add it to **Decisions so far**.

## Charting a map

The user invokes this with a loose idea. Charting creates issues, so it never starts on the model's own judgment.

1. **Name the destination.** Run `grill-with-docs` and `domain-modeling` on one question: what does finished look like? A spec, a decision, or a change made in place. Settle this first because it fixes the scope of everything else.
2. **Find the open questions.** Grill again, wide rather than deep: cover the whole space, surface every decision that has to be made and which ones can be worked on now. If this turns up nothing that has to wait on something else, the work fits one grill session and does not need a map. Say so and ask how the user wants to proceed.
3. **Create the map issue** with the body above: Destination and Notes filled in, Decisions so far empty, the questions you cannot yet state under Not yet specified, anything ruled out under Out of scope. Labels: `epic`, `needs-grilling`.
4. **Create the tickets** you can state precisely, one sub-issue each with its type label. Then, in a second pass, set the blocking relations, `Blocked by #N` lines, and `blocked` labels (issues need numbers before they can refer to each other).
5. **Fire the research.** For every research ticket, start one sub-agent in parallel with the method under "Research". Wait for them, record each one as "Working a ticket" step 4 describes, then move on.
6. **Stop.** Report the map by title with its link, the number of tickets on the frontier, and the number blocked. Charting resolves no grilling tickets.

## Working a ticket

Invoked by the user with a map or ticket number or URL, or by `grill-issues` when its sweep meets a ticket whose parent is an `epic`.

1. **Load the map**: the body only, not every ticket. Read the Destination, Notes, and Decisions so far. Load any skills the Notes name.
2. **Pick the ticket.** If one was named, take it. Otherwise take the first frontier ticket in the sub-issue order. **Claim it** by assigning it to the user before doing anything else.
3. **Resolve it** by type. For grilling, run `grill-with-docs` and `domain-modeling` on the ticket's question; read related closed tickets and the repo's `CONTEXT.md` and ADRs as needed, not up front. For research, run the method under "Research". For a task, do the work or walk the user through the checklist.
4. **Record it.** Post the resolution comment (shape below), close the ticket, and append one line to the map's Decisions so far. Hard-to-reverse trade-offs go into an ADR and agreed terms into `CONTEXT.md`, as `domain-modeling` describes; check that it happened.
5. **Update the map.** Create the tickets the answer made possible to state, wire their blocking, and remove the matching entries from Not yet specified. Remove `blocked` from tickets this one was blocking. If the answer shows a ticket is beyond the destination, rule it out of scope. If it invalidates other tickets, edit or close them. Fire sub-agents for any new research tickets.
6. **Stop**, unless the map is finished. Report in two or three lines: the ticket by title and its answer, what was written to the docs, how many tickets remain on the frontier and how many are blocked.

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

A research ticket is resolved by a sub-agent with no user in the loop. Give it the ticket's question, the map's Destination and Notes, and this method:

1. Read the sources the question points at: documentation, an API, a library, the codebase. Prefer primary sources and quote them.
2. Answer the question. Say plainly when the sources do not settle it.
3. Post a comment in the shape below, close the ticket, and return the one-line answer for the map.

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

The sub-agent does not create tickets or edit the map. The calling session does that from the answer.

## Finishing the map

The map is finished when there are no open sub-issues and Not yet specified is empty. Confirm with the user that nothing is left to decide. Then:

1. Run `to-issues` with the map as the parent. Every slice's Parent field points at the map issue, and slices are labeled as the `labels` skill describes.
2. Close the map with a comment listing the slices by title.

## GitHub commands

Sub-issue and dependency endpoints take the database id, not the number:

```sh
gh api repos/{owner}/{repo}/issues/<n> --jq .id
```

Create the map and a ticket, then attach the ticket:

```sh
gh issue create --title "<map title>" --label epic,needs-grilling --body-file map.md
gh issue create --title "<ticket title>" --label needs-grilling --body-file ticket.md
gh api -X POST repos/{owner}/{repo}/issues/<map>/sub_issues -F sub_issue_id=<ticket db id>
```

Block ticket B on ticket A (native relation, body line, and label):

```sh
gh api -X POST repos/{owner}/{repo}/issues/<B>/dependencies/blocked_by -F issue_id=<A db id>
gh issue edit <B> --add-label blocked
```

Frontier of a map: open, unassigned, not blocked:

```sh
gh api repos/{owner}/{repo}/issues/<map>/sub_issues --paginate \
  --jq '.[] | select(.state=="open" and (.assignees|length)==0 and ([.labels[].name]|index("blocked")|not)) | "\(.number) \(.title)"'
```

Claim and close:

```sh
gh issue edit <n> --add-assignee @me
gh issue comment <n> --body-file resolution.md
gh issue close <n>
```

If the repo lacks the `epic` label, offer `setup-repo` and stop.
