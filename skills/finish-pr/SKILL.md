---
name: finish-pr
description: Land a finished pull request as the implementer once review is complete - check nothing is outstanding, file follow-up issues, rebase-merge, delete the branch, and suggest what to work on next. Use when the user says "finish PR 98", "/finish-pr", "land this PR", "merge and clean up", or asks what to work on after a merge.
---

# Finish PR

The implementer's procedure for landing a PR once the review loop is done: check, file follow-ups, merge, clean up, and line up the next piece of work. Uses the labels from the `labels` skill.

## How to talk to the user

Write to the user in plain, direct English, the way you would explain the work to a colleague. Use full sentences and everyday words, with no slogans and no invented terms. Lead with what you found, what you did, and what happens next. The full guide is [STYLE.md](../../STYLE.md).

## Rules

- **Merge only when nothing is outstanding.** Outstanding means unresolved review threads, failing CI, a changes-requested review, or merge conflicts. When all of those are clear, merge without asking. When something needs the user's judgment, ask one combined question rather than several small ones.
- **Always merge with rebase**, and delete the branch on both the remote and locally as part of the merge.
- **Anything deferred during review becomes an issue.** Review points set aside as "out of scope, follow-up", suggestions that were accepted but not required, and TODOs this PR introduces each become a labeled issue that links back to the PR.
- **Suggest only work that can start now.** Suggest only `ready-for-agent` issues, since that label means fully specified and blocked by nothing. Verify that anyway and fix wrong labels as the `labels` skill describes. Waiting on the user's input does not count as blocked: list `needs-input` issues separately, with the question each one is waiting on.
- **Default order is oldest first.** The user's request can override this ("prioritize label:x", "newest", a milestone, and so on).

## Workflow

### 1. Assess

```sh
gh pr view <n> --json number,title,state,headRefName,baseRefName,reviewDecision,mergeStateStatus,mergeable,author,url
gh pr checks <n>
```

Also fetch the unresolved review threads, with the same GraphQL query the `review-pr` skill uses (reviewThreads, then isResolved).

- If CI is still running, run `gh pr checks <n> --watch` and wait for it.
- If CI is failing, threads are unresolved, or `reviewDecision` is `CHANGES_REQUESTED`, fixing that is not this skill's job. Report what is outstanding and stop. The fix path is `answer-review` and the review loop.
- If `mergeStateStatus` is `DIRTY` (conflicts), rebase locally: the tree must be clean, then `gh pr checkout <n>` and `git rebase origin/<base>`. If the conflicts do not resolve trivially, stop and ask. If they do, `git push --force-with-lease` and wait for CI again.

### 2. Collect follow-ups

Look through the review threads and the PR conversation for anything that was agreed as "later": pushbacks accepted as out of scope, deferred suggestions, `nit:` comments the author skipped with agreement, and TODO or FIXME comments the diff introduces. For each, draft an issue: a title, a 2-5 line body with context, a `From #<pr>` link, and a state label as the `labels` skill describes (`ready-for-agent` if the review thread fully specified it, otherwise `needs-grilling`).

File the clear-cut ones with `gh issue create --title ... --body ... --label ...`. If it is unclear whether something deserves an issue, put it in the step 3 question.

### 3. Ask only if something needs the user

If anything above needs the user's call (a debatable follow-up, a non-trivial conflict, an unresolved thread the user might want to waive), ask once, with everything in one question. If nothing does, proceed without asking.

### 4. Merge and clean up

```sh
gh pr merge <n> --rebase --delete-branch
```

This deletes the remote branch. When the branch is checked out locally it also switches back to the base branch and deletes the local one. If the branch lives in a leftover `implement` worktree (check `git worktree list`), remove that worktree first, because a branch checked out in a worktree cannot be deleted. Verify the local side with `git branch --list <headRefName>`. If the local branch is still there (for example because you ran this from another branch), run `git branch -D <headRefName>`. Finish with `git pull` on the base branch.

### 5. Suggest next work

A note on solo repos: GitHub does not allow approving your own PR, so `reviewDecision` never reads `APPROVED` on your own PRs. The `ready-to-merge` label is the signal that review passed, and the approval state only means something when a second account reviews. Steps 1-4 do not depend on the labels (threads, CI, and conflicts all work without them). This step does. If the repo does not have the workflow labels: in an interactive session, offer to run `setup-repo`; when running unattended, say plainly that no suggestions are possible until the repo is set up. Do not present an empty list as "nothing to do".

```sh
gh issue list --state open --label ready-for-agent --json number,title,labels,createdAt,body,url
```

- Apply the user's prioritization if they gave one; otherwise oldest first.
- Verify that each candidate really can start: no `blocked` label, and no `Blocked by #N` or `Depends on #N` in the body pointing at an issue that is still open. Fix a wrongly labeled one (swap `ready-for-agent` for `blocked` as the `labels` skill describes) and skip it.
- If this PR closed an issue, check what that issue was blocking with `gh issue list --state open --label blocked --search "Blocked by #<closed>"`. Any issue whose blockers have now all closed loses the `blocked` label, and if it carries no `needs-*` state it becomes `ready-for-agent` and joins this round's candidates. Blocked issues unrelated to this merge are for `triage` to sweep up.
- Present the top 3-5: number, title, age, one line on what it involves, and mark one as recommended, with the reason.
- Then, clearly separated, the open `needs-input` issues, each with the specific question it is waiting on. The user can unblock these with an answer.

### 6. Report

A summary in the terminal: merged (link), branch deletion confirmed, follow-up issues filed (links), then the suggestions. This is the one skill where a summary is the right output.
