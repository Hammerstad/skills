---
name: work-loop
description: Work through the ready-for-agent backlog end to end - pick the oldest ready issue, implement it, run the review loop with sub-agents, land the PR, triage, and repeat until nothing is ready. Only invoked explicitly by the user via /work-loop.
disable-model-invocation: true
---

# Work Loop

Run the whole pipeline, issue after issue, until no `ready-for-agent` issues are left.

This skill only coordinates. Every piece of real work belongs to the skill that owns it: `implement`, `review-pr`, `answer-review`, `finish-pr`, `triage`. What this skill owns is choosing what runs next, keeping the reviewer independent of the author, recognizing a stuck PR, and knowing when to stop.

## How to talk to the user

Write to the user in plain, direct English, the way you would explain the work to a colleague. Use full sentences and everyday words, with no slogans and no invented terms. Lead with what you found, what you did, and what happens next. The full guide is [STYLE.md](../../STYLE.md).

## Rules

- **One issue at a time, in sequence.** Never start a second issue while a PR is open. Every merge moves the base branch and `finish-pr` rebases onto it, so running issues in parallel produces conflicts rather than saving time.
- **Oldest first**, unless the invocation says otherwise (`/work-loop prioritize label:bug`, `newest`, a milestone). Age is measured by `createdAt` rather than by issue number.
- **Review always runs in a fresh sub-agent.** This is about independence rather than speed: the reviewer must not inherit the implementer's context. A reviewer who watched the code get written already believes every justification for it. A sub-agent that sees only the PR reviews the diff on its own merits.
- **Answering runs in its own sub-agent too**, for the same reason in reverse: it argues from the PR and the code, without a remembered intent that never made it into either.
- **The label is the verdict.** Do not rely on the sub-agent's account of what it did. After every sub-agent returns, re-read the PR's labels and threads yourself. `ready-to-merge` is the only thing that lets `finish-pr` run. Never merge because a review "looked clean".
- **Do not touch code.** The coordinating session never edits, commits, or pushes. If something needs fixing, the skill that owns it fixes it in its own run.
- **Never lower the bar to keep working.** Do not move `needs-grilling`, `needs-diagnosis`, or `needs-input` issues into the queue, do not implement an issue that does not meet the `ready-for-agent` definition, and do not invent work. An empty queue is a successful finish.
- **A stuck issue stops that issue, and the loop continues.** A halted `implement`, a review loop that will not converge, or CI failing for reasons outside this PR: record it, leave the labels and threads in a state that matches reality, and move to the next issue.
- **The loop ends when the queue is empty**, never on a round count or a clock.

## Workflow

### 0. Build the queue

```sh
gh issue list --state open --label ready-for-agent --json number,title,createdAt,labels,body,url,assignees
gh pr list --state open --json number,title,headRefName,body,labels        # what is already in progress
```

Filter the candidates:

- Drop any issue that an open PR already closes (`Closes #<n>` in a PR body, or an `<n>-…` branch name). That issue is partway through the pipeline, and it gets picked up at step 3 rather than step 2.
- Drop wrongly labeled issues and fix their labels as the `labels` skill describes: `blocked` alongside `ready-for-agent`, or a body naming `Blocked by #N` or `Depends on #N` with #N still open. Correcting the label is part of the sweep.

If the repo has none of the workflow labels, there is no queue to trust. Offer `setup-repo` and stop. Never read an empty list as "backlog done".

Print the queue before starting (number, title, age, one line each) and say plainly that the run continues until the queue is empty. Then start. The user can interrupt; do not wait for approval.

### 1. Pick

Take the first issue in the queue. Re-check the `ready-for-agent` definition against the live issue, since it may have been edited since step 0. If it no longer qualifies, fix the label, log the skip, and take the next one.

### 2. Implement

Invoke the `implement` skill for the issue, in this session. It ends in one of three states. Check which, rather than assuming:

| Outcome | Next |
|---|---|
| PR opened, labeled `ready-for-review` | Step 3 |
| Halted on a spec gap (`needs-input`, branch pushed, no PR) | Log the skip with the question it posted; back to step 1 |
| Failed (broken baseline, unresolvable conflict) | Log it; back to step 1 |

### 3. Review loop

Alternate two sub-agents against the PR until it settles. Each round:

1. **Review.** Spawn a sub-agent with fresh context and tools that can post to GitHub:

   ```
   Invoke the /hammerstad-skills:review-pr skill on PR #<P> in <repo>.
   You have no prior context on this PR by design. Review the diff on its own merits.
   Do not merge, do not implement fixes, do not touch the branch.
   Report back: the label you left on the PR, the number of findings you posted,
   and one line per finding.
   ```

2. Re-read the PR yourself: `gh pr view <P> --json labels,reviewDecision,mergeStateStatus` plus the unresolved-thread query from `review-pr`'s `reference/github-api.md`.
   - `ready-to-merge` and no unresolved threads: go to step 4.
   - `review-feedback` or unresolved threads: continue.

3. **Answer.** Spawn a second sub-agent, only after the reviewer has finished, because this one commits and pushes and the two must never overlap:

   ```
   Invoke the /hammerstad-skills:answer-review skill on PR #<P> in <repo>.
   You are the author responding to review. Fix or push back on every unresolved thread.
   Do not merge and do not resolve threads. The reviewer resolves them next round.
   Report back: threads fixed (with SHAs), threads pushed back on (with the reason),
   and the label you left.
   ```

4. Re-read the PR again, then back to 1.

`answer-review` works in the main checkout (`gh pr checkout`), so the tree must be clean between rounds. `implement` removes its worktree at the end, but verify that rather than assuming it.

**Limit the back-and-forth.** Three full rounds without reaching `ready-to-merge` means the two sub-agents are arguing rather than converging. Stop this PR: leave every thread and label exactly as they are, log the specific points still in dispute, and move to the next issue. In an interactive session, ask the user one question before moving on, since a human can settle in a sentence what another round will not.

### 4. Finish

When the PR is `ready-to-merge` with nothing outstanding, invoke `finish-pr` for it in this session rather than in a sub-agent: it merges, files follow-ups, and its next-work suggestions feed straight back into this loop. If it stops on something outstanding, that contradicts step 3's re-read. Trust `finish-pr`, log the discrepancy, and treat the PR as stuck as described in step 3.

### 5. Triage, then loop

Sweep the tracker with the `triage` skill before the next pick, so that the next iteration chooses from an accurate queue. Triage is interactive by design, so inside the loop split it in two:

- **Apply without asking** the mechanical part: blockers that have closed, label combinations that should not exist, and issues the merge just unblocked (`finish-pr` already handles the ones this PR closed).
- **Defer** anything that needs the user's judgment: unlabeled issues, `needs-input` issues with a fresh human answer, stale states. Collect them for the final report. Blocking the loop on a question the user is not there to answer stalls the run, and guessing a state silently corrupts the queue.

Then back to step 0. Rebuild the queue from scratch rather than reusing the old one, since a merge, a triage fix, or a follow-up issue filed by `finish-pr` may have changed it.

### 6. Report

An empty queue ends the run. One terminal summary for the whole thing:

- Per issue: number, PR link, merge status, and how many review rounds it took.
- Skipped issues, each with its reason (spec gap, wrong label, failed implement) and what was left behind.
- Stuck PRs, each with the disputed points and the state left on GitHub.
- Follow-up issues filed during the run.
- The deferred triage questions from step 5.
- What remains open and is not `ready-for-agent`, as the answer to "what is left".
