---
name: finish-pr
description: Land a finished pull request as the implementer once review is complete - check nothing is outstanding, file follow-up issues, rebase-merge, delete the branch, and suggest what to work on next. Use when the user says "finish PR 98", "/finish-pr", "land this PR", "merge and clean up", or asks what to work on after a merge.
---

# Finish PR

The implementer's landing procedure once the review loop is done. Check → follow-ups → merge → clean up → line up the next piece of work. Uses the label taxonomy from the `labels` skill.

## Contract

- **Merge only what's settled.** Outstanding = unresolved review threads, failing CI, changes-requested, merge conflicts. All clear → merge **without asking**. Anything needing the user's judgment → one consolidated question, never a drip.
- **Merge method is always rebase**, and the branch dies with the merge — remote and local.
- **Follow-ups become issues, not memories.** Deferred review points ("out of scope, follow-up"), accepted-but-not-required suggestions, and TODOs introduced by this PR each become a labeled issue linking back to the PR.
- **Next-work suggestions must be unblocked.** Suggest only `ready-for-agent` issues (that label *guarantees* spec'd + unblocked); verify the guarantee anyway and fix mislabels per the `labels` skill. Needing the user's input is **not** blocked — surface `needs-input` issues as a secondary list with the question each one is waiting on.
- **Default order: oldest first.** The user's invocation can override ("prioritize label:x", "newest", a milestone, ...).

## Workflow

### 1. Assess

```sh
gh pr view <n> --json number,title,state,headRefName,baseRefName,reviewDecision,mergeStateStatus,mergeable,author,url
gh pr checks <n>
```

Plus unresolved review threads — same GraphQL query as the `review-pr` skill (reviewThreads → isResolved).

- CI still running → `gh pr checks <n> --watch` and wait it out.
- CI failing, unresolved threads, or `reviewDecision: CHANGES_REQUESTED` → these are not finish-pr's job to fix. Report what's outstanding and stop; the fix path is `answer-review` / the review loop.
- `mergeStateStatus: DIRTY` (conflicts) → rebase locally: clean tree required, `gh pr checkout <n>`, `git rebase origin/<base>`. Conflicts that don't resolve trivially → stop and ask. Clean → `git push --force-with-lease`, wait for CI again.

### 2. Collect follow-ups

Scan the review threads and PR conversation for anything settled as "later": pushbacks accepted as out-of-scope, deferred suggestions, `nit:`s the author skipped with agreement, TODO/FIXME comments the diff introduces. For each, draft an issue: title, 2-5 line body with context, `From #<pr>` link, and a state label per the `labels` skill (`ready-for-agent` if the review thread fully specified it, else `needs-grilling`).

Unambiguous ones: file them (`gh issue create --title ... --body ... --label ...`). Genuinely unclear whether something deserves an issue → put it in the step-3 question.

### 3. Ask only if something needs the user

If anything above needs a call — a debatable follow-up, a non-trivial conflict, an unresolved thread the user might want to waive — ask **once**, with everything in one question. If nothing does, proceed silently.

### 4. Merge and clean up

```sh
gh pr merge <n> --rebase --delete-branch
```

This deletes the remote branch; when the branch is checked out locally it also switches back to the base branch and deletes the local one. Verify the local side (`git branch --list <headRefName>`) — if it survived (e.g. invoked from another branch), `git branch -D <headRefName>`. Finish with `git pull` on the base branch.

### 5. Suggest next work

```sh
gh issue list --state open --label ready-for-agent --json number,title,labels,createdAt,body,url
```

- Apply the user's prioritization from the invocation if given; otherwise oldest first.
- Verify each candidate really is unblocked: no `blocked` label, no `Blocked by #N` / `Depends on #N` in the body pointing at a still-open issue. A mislabeled one gets fixed (swap `ready-for-agent` for `blocked` per the `labels` skill) and skipped.
- Present the top 3-5: number, title, age, one line on what it involves, and mark one as recommended (with why).
- Secondary list, clearly separated: open `needs-input` issues, each with the specific question it's waiting on — the user can unblock these with an answer.

### 6. Report

Terminal summary: merged (link), branch deletion confirmed, follow-up issues filed (links), then the suggestions. This is the one place where a summary belongs.
