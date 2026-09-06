---
name: setup-repo
description: Prepare a GitHub repo for the skills workflow - create the workflow labels, verify tooling, and optionally configure branch protection. Use when the user says "set up this repo", "setup-repo", when labels are missing in a repo the workflow runs in, or when another skill offers setup after finding the labels missing.
---

# Setup Repo

Make a repository ready for the workflow skills (`labels`, `implement`, `review-pr`, `answer-review`, `finish-pr`, `to-issues`). Everything here is safe to run more than once. Nothing fails hard: whatever cannot be done (missing permissions, someone else's repo) is reported and left alone.

## How to talk to the user

Write to the user in plain, direct English, the way you would explain the work to a colleague. Use full sentences and everyday words, with no slogans and no invented terms. Lead with what you found, what you did, and what happens next. The full guide is [STYLE.md](../../STYLE.md).

## 1. Verify access

```sh
gh auth status
gh repo view --json nameWithOwner,defaultBranchRef,viewerPermission
```

If `viewerPermission` is below `WRITE`, report that setup needs a repo you can administer, list what would have been done, and stop.

## 2. Create the labels

The meaning of each label is in the `labels` skill; this is the procedure that creates them. `--force` updates the color and description of labels that already exist, so re-running never conflicts:

```sh
gh label create needs-grilling   --force --color D93F0B --description "Under-specified - grill into a spec first"
gh label create needs-diagnosis  --force --color E99695 --description "Bug with unknown root cause - diagnose first"
gh label create needs-input      --force --color FBCA04 --description "A named question waits on a human - maintainer or reporter"
gh label create ready-for-agent  --force --color 0E8A16 --description "Spec complete and unblocked - implementable now"
gh label create blocked          --force --color B60205 --description "Depends on an open issue - see 'Blocked by #N' in body"
gh label create ready-for-review --force --color 1D76DB --description "PR: implementation complete, review requested"
gh label create review-feedback  --force --color 5319E7 --description "PR: review left unresolved findings"
gh label create ready-to-merge   --force --color 0E8A16 --description "PR: review clean - merge via finish-pr"
```

## 3. Offer branch protection (optional; ask, do not assume)

For solo repos the signal that review passed is the `ready-to-merge` label, since GitHub does not allow the PR author to approve their own PR. So never require approving reviews. The protection that does fit the workflow, and that you can offer to apply to the default branch, is:

- **Required status checks.** Makes `finish-pr`'s CI gate enforced by GitHub. Ask which checks, or read the names from a recent PR's `gh pr checks`.
- **Require conversation resolution.** GitHub itself then blocks merging with open threads. This fits the loop: `review-pr` resolves threads that are done before marking `ready-to-merge`.
- **Rebase merging enabled.** `finish-pr` merges with `--rebase`. Verify that the repo allows it (`gh api repos/{owner}/{repo} --jq .allow_rebase_merge`) and enable it with `gh repo edit --enable-rebase-merge` if it is off.

Apply with `gh api` on the branch protection endpoint only after the user picks. Skipping this step entirely is a fine outcome.

## 4. Optional starter files

Offer these one at a time, only where missing. Never create content the user did not ask for:

- `CONTEXT.md`, created nearly empty in the `domain-modeling` format, when the user wants the glossary discipline from day one.
- A build, test, and format section in `CLAUDE.md`. The `implement` skill finds its commands from the repo docs, so writing the three commands down once saves every future run from having to find them.

## 5. Report

What was created, what already existed, what was skipped and why, and, if anything needed permissions the account lacks, exactly which step to rerun after access is granted.
