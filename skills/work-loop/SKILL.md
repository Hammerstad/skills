---
name: work-loop
description: Drain the ready-for-agent backlog end to end - pick the oldest ready issue, implement it, drive the review loop with sub-agents, land the PR, triage, and repeat until nothing is ready. Only invoked explicitly by the user via /work-loop.
disable-model-invocation: true
---

# Work Loop

Run the whole pipeline, issue after issue, until the `ready-for-agent` pool is empty.

This skill is **orchestration only**. Every piece of real work belongs to the skill that owns it — `implement`, `review-pr`, `answer-review`, `finish-pr`, `triage`. What this skill owns is choosing what runs next, keeping the reviewer independent of the author, recognising a stuck PR, and knowing when to stop.

## Contract

- **One issue at a time, strictly sequential.** Never start a second issue while a PR is in flight. Every merge moves the base branch and `finish-pr` rebases onto it; parallelism here buys conflicts, not speed.
- **Oldest first**, unless the invocation says otherwise (`/work-loop prioritize label:bug`, `newest`, a milestone). Age is by `createdAt`, not by issue number.
- **Review always runs in a fresh sub-agent.** The point is not parallelism — it is that the reviewer must not inherit the implementer's context. A reviewer who watched the code get written already believes every justification for it; a sub-agent that sees only the PR reviews the diff on its merits.
- **Answering runs in its own sub-agent too**, for the same reason in reverse: it argues from the PR and the code, not from a remembered intent that never made it into either.
- **The label is the verdict, not the sub-agent's narration.** After every sub-agent returns, re-read the PR's labels and threads yourself. `ready-to-merge` is the only thing that lets `finish-pr` run — never merge because a review "looked clean".
- **Own no code.** The orchestrator never edits, commits, or pushes. If something needs fixing, the owning skill fixes it in its own run.
- **Never lower the bar to keep working.** Do not promote `needs-grilling` / `needs-diagnosis` / `needs-input` issues into the queue, do not implement an issue that fails the `ready-for-agent` guarantee, and do not invent work. An empty pool is a successful finish.
- **Stuck stops the issue, not the loop.** A halted `implement`, a review loop that will not converge, CI red for reasons outside this PR — record it, leave the artifacts in a truthful state, move to the next issue.
- **The loop ends on an empty pool** — never on a round count or a clock.

## Workflow

### 0. Build the queue

```sh
gh issue list --state open --label ready-for-agent --json number,title,createdAt,labels,body,url,assignees
gh pr list --state open --json number,title,headRefName,body,labels        # what is already in flight
```

Filter the candidates:

- Drop any issue an open PR already closes (`Closes #<n>` in a PR body, or an `<n>-…` branch name) — that issue is mid-pipeline, and it gets picked up at step 3 rather than step 2.
- Drop and **fix** mislabels per the `labels` skill: `blocked` alongside `ready-for-agent`, or a body naming `Blocked by #N` / `Depends on #N` with #N still open. Swapping the label to the truthful state is part of the sweep, not a digression.

No taxonomy in the repo at all → the pool cannot be trusted to exist. Offer `setup-repo` and stop; never read an empty list as "backlog done".

Print the queue before starting — number, title, age, one line each — and say plainly that the run continues until the pool empties. Then start. The user can interrupt; don't wait for approval.

### 1. Pick

Take the head of the queue. Re-verify the `ready-for-agent` guarantee against the live issue — it may have been edited since step 0. Fails the guarantee → fix the label, log the skip, take the next one.

### 2. Implement

Invoke the `implement` skill for the issue, in this session. It ends in one of three states — check which, don't assume:

| Outcome | Next |
|---|---|
| PR opened, labeled `ready-for-review` | Step 3 |
| Halted on a spec gap (`needs-input`, branch pushed, no PR) | Log the skip with the question it posted; back to step 1 |
| Failed (broken baseline, unresolvable conflict) | Log it; back to step 1 |

### 3. Review loop

Alternate two sub-agents against the PR until it settles. Each round:

1. **Review** — spawn a sub-agent with fresh context and tools that can post to GitHub:

   ```
   Invoke the /hammerstad-skills:review-pr skill on PR #<P> in <repo>.
   You have no prior context on this PR by design — review the diff on its own merits.
   Do not merge, do not implement fixes, do not touch the branch.
   Report back: the label you left on the PR, the number of findings you posted,
   and one line per finding.
   ```

2. Re-read the PR yourself: `gh pr view <P> --json labels,reviewDecision,mergeStateStatus` plus the unresolved-thread query from `review-pr`'s `reference/github-api.md`.
   - `ready-to-merge`, no unresolved threads → step 4.
   - `review-feedback` or unresolved threads → continue.

3. **Answer** — spawn a second sub-agent, only after the reviewer has finished (it commits and pushes; the two must never overlap):

   ```
   Invoke the /hammerstad-skills:answer-review skill on PR #<P> in <repo>.
   You are the author responding to review. Fix or push back on every unresolved thread.
   Do not merge and do not resolve threads — the reviewer resolves them next round.
   Report back: threads fixed (with SHAs), threads pushed back on (with the reason),
   and the label you left.
   ```

4. Re-read the PR again, then back to 1.

`answer-review` works in the main checkout (`gh pr checkout`), so the tree must be clean between rounds — `implement` removes its worktree at the end, but verify rather than assume.

**Bound the ping-pong.** Three full round-trips without reaching `ready-to-merge` means the two sub-agents are arguing, not converging. Stop this PR: leave every thread and label exactly as they are, log the specific points still in dispute, and move to the next issue. Interactively, this is worth one question to the user before moving on — a human call settles in a sentence what another round will not.

### 4. Finish

`ready-to-merge` with nothing outstanding → invoke `finish-pr` for the PR, in this session, not a sub-agent: it merges, files follow-ups, and its next-work suggestions feed straight back into this loop. If it stops on something outstanding, that contradicts step 3's re-read — trust `finish-pr`, log the discrepancy, and treat the PR as stuck per step 3.

### 5. Triage, then loop

Sweep the tracker with the `triage` skill before the next pick, so the next iteration chooses from a truthful pool. Triage is interactive by design; inside a loop, split it:

- **Apply without asking** — the mechanical bucket: dead blockers whose blocker has closed, illegal label combinations, issues the merge just unblocked (`finish-pr` already handles the ones this PR closed).
- **Defer, don't block** — anything needing the user's judgment: unlabeled issues, `needs-input` with a fresh human answer, stale states. Collect them for the final report. Blocking the loop on a question the user isn't there to answer stalls the run; guessing a state silently corrupts the pool.

Then back to step 0 — rebuild the queue from scratch rather than reusing the stale one. A merge, a triage fix, or a follow-up issue filed by `finish-pr` may have changed it.

### 6. Report

An empty queue ends the run. One terminal summary for the whole thing:

- Per issue: number, PR link, merge status, how many review rounds it took.
- Skipped issues, each with its reason (spec gap, mislabel, failed implement) and the artifact left behind.
- Stuck PRs, each with the disputed points and the state left on GitHub.
- Follow-up issues filed during the run.
- The deferred triage questions from step 5.
- What remains open and not `ready-for-agent` — the honest answer to "what's left".
