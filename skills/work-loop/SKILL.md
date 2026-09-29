---
name: work-loop
description: Work through the ready-for-agent backlog end to end - pick the oldest ready issue, implement it, run the review loop with a sub-agent reviewer, merge the PR, triage, and repeat until nothing is ready. Only invoked explicitly by the user via /work-loop.
disable-model-invocation: true
---

# Work Loop

Run the whole pipeline, issue after issue, until no `ready-for-agent` issues are left.

This skill does no work of its own. It runs the other skills in order: `implement`, `review-pr`, `answer-review`, `finish-pr`, `triage`. It decides which skill runs next, keeps the reviewer separate from the author, notices when a review is deadlocked, and decides when to stop.

## How to talk to the user

Write like an engineer reporting to a colleague who is short on time. These rules apply to chat and to everything you write into GitHub or into docs.

- Lead with the result: what happened or what you found, then what the reader has to do. If something failed or was skipped, that is the first line, with the output. Add details only when asked.
- Keep a chat reply under ten lines unless it is a list of findings. One idea per sentence.
- Say the literal thing. No metaphors or flourishes ("a landmine", "fold this in" for "add this"), no filler ("worth noting", "the key insight"), no coined names for things that have an ordinary description. Spell out an acronym the first time unless it is an established engineering term.
- Do not sell and do not narrate. A recommendation gets its reason in one clause or none. Do not describe what you are about to do or how you reasoned.
- Format plainly: bullets only for parallel items, no bold lead-ins, a period or a comma over an em-dash, commands, paths, and error text in backticks. Before sending, reread once and delete metaphors, justifications, and anything the reader did not ask for.

## Rules

- **One issue at a time, in sequence.** Never start a second issue while a PR is open. Every merge moves the base branch and `finish-pr` rebases onto it, so running issues in parallel produces conflicts rather than saving time.
- **Oldest first**, unless the invocation says otherwise (`/work-loop prioritize label:bug`, `newest`, a milestone). Age is measured by `createdAt` rather than by issue number.
- **Review always runs in a fresh sub-agent.** The reviewer must not see the context in which the code was written. A reviewer that saw the implementation already accepts the reasons given for it. A sub-agent that sees only the PR judges the diff by what it contains.
- **Everything else runs in this session.** `implement`, `answer-review`, `finish-pr`, and `triage` run here, as the author would run them. A sub-agent starts from nothing and re-reads the PR, the code, and the skill files, so use one only where independence requires it.
- **Models come from the skills.** `implement` sets `model: sonnet`; `answer-review` and `finish-pr` set `model: opus`, which returns the session to Opus after implementing. Pass `model: opus` on the reviewer's Agent call.
- **Decide from the PR's labels.** Do not rely on the reviewer's account of what it did. After the reviewer returns and after every `answer-review` run, re-read the PR's labels and threads yourself. `ready-to-merge` is the only thing that lets `finish-pr` run. Never merge because a review "looked clean".
- **Do not touch code outside the skills.** This session edits, commits, and pushes only inside an `implement` or `answer-review` run. If something needs fixing, the skill that owns it fixes it.
- **Only work on issues that are ready.** Do not move `needs-grilling`, `needs-diagnosis`, or `needs-input` issues into the queue, do not implement an issue that does not meet the `ready-for-agent` definition, and do not invent work. An empty queue is a successful finish.
- **When one issue gets stuck, move on to the next.** If `implement` halts, or CI fails for reasons outside this PR, record it, leave the labels and threads in a state that matches reality, and move to the next issue.
- **The loop ends when the queue is empty**, never on a round count or a clock.
- **Do not pause between issues.** Do not end a turn to announce the next step, to offer to continue, to list decisions that block nothing, or to report after a milestone. Put a status note in the same message as the next tool call. Stop only where the steps below say to. After an interruption (a session limit, a reboot, a permission prompt), resume by rebuilding the queue at step 0; the labels and threads on GitHub hold all the state.

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

Alternate a sub-agent reviewer and `answer-review` in this session until the PR is ready to merge. Each round:

1. **Review.** Spawn a sub-agent with fresh context, `model: opus`, and tools that can post to GitHub:

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

3. **Answer.** Invoke `answer-review` on the PR in this session, only after the reviewer has finished, because it commits and pushes and the two must never overlap. Fix or push back on every unresolved thread. Do not merge and do not resolve threads; the reviewer resolves them next round. Log the threads fixed (with SHAs) and the threads pushed back on (with the reason).

4. Re-read the PR again, then back to 1.

The reviewer and `answer-review` each work in their own worktree, so the shared checkout's state does not matter between rounds. Verify that `implement` removed its worktree rather than assuming it.

**There is no round limit.** Keep alternating until the PR reaches `ready-to-merge`. The one exception is a deadlock: a round with no new commits in which `answer-review` pushes back on the same threads with the same reasons as the round before. Then ask the user one question about the disputed points and wait for the answer, even in an unattended run. Apply the answer in the next `answer-review` run and continue the same PR.

### 4. Finish

When the PR is `ready-to-merge` with nothing outstanding, invoke `finish-pr` for it in this session: it merges, files follow-ups, and its next-work suggestions feed straight back into this loop. If it stops on something outstanding, that contradicts step 3's re-read. Trust `finish-pr`, log the discrepancy, and treat the PR as stuck as the rules above describe.

### 5. Triage, then loop

Sweep the tracker with the `triage` skill before the next pick, so that the next iteration chooses from an accurate queue. Triage is interactive by design, so inside the loop split it in two:

- **Apply without asking** the mechanical part: blockers that have closed, label combinations that should not exist, and issues the merge just unblocked (`finish-pr` already handles the ones this PR closed).
- **Defer** anything that needs the user's judgment: unlabeled issues, `needs-input` issues with a fresh human answer, stale states. Collect them for the final report. Blocking the loop on a question the user is not there to answer stalls the run, and a guessed state puts wrong issues in the queue with no way to notice.

Then back to step 0. Rebuild the queue from scratch rather than reusing the old one, since a merge, a triage fix, or a follow-up issue filed by `finish-pr` may have changed it.

### 6. Report

An empty queue ends the run. One terminal summary for the whole thing, one line per item:

- Per issue: number, PR link, merge status, and how many review rounds it took.
- Skipped issues, each with its reason (spec gap, wrong label, failed implement) and what was left behind.
- Stuck PRs, each with the reason and the state left on GitHub.
- Follow-up issues filed during the run.
- The deferred triage questions from step 5.
- What remains open and is not `ready-for-agent`, as the answer to "what is left".
