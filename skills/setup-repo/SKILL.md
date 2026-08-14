---
name: setup-repo
description: Prepare a GitHub repo for the skills workflow - create the label taxonomy, verify tooling, and optionally configure branch protection. Use when the user says "set up this repo", "setup-repo", when labels are missing in a repo the workflow runs in, or when another skill offers setup after detecting a missing taxonomy.
---

# Setup Repo

Make a repository ready for the workflow skills (`labels`, `implement`, `review-pr`, `answer-review`, `finish-pr`, `to-issues`). Everything here is idempotent — running it twice is safe. Nothing fails hard: whatever can't be done (missing permissions, foreign repo) is reported, not fought.

## 1. Verify access

```sh
gh auth status
gh repo view --json nameWithOwner,defaultBranchRef,viewerPermission
```

`viewerPermission` below `WRITE` → report that setup needs a repo you can administer, list what would have been done, stop politely.

## 2. Create the label taxonomy

The semantics live in the `labels` skill; this is the canonical creation procedure. `--force` updates color/description on existing labels, so re-running never conflicts:

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

## 3. Offer branch protection (optional — ask, don't assume)

For solo repos the workflow's verdict signal is the `ready-to-merge` label, **not** GitHub approvals — so never require approving reviews (the PR author's own approval is impossible). The protection that *does* fit the workflow, offer to apply to the default branch:

- **Required status checks** — makes `finish-pr`'s CI gate GitHub-enforced. Ask which checks (or read the names from a recent PR's `gh pr checks`).
- **Require conversation resolution** — GitHub itself then blocks merging with open threads. Compatible with the loop: `review-pr` resolves settled threads before `ready-to-merge`.
- **Rebase merging enabled** — `finish-pr` merges with `--rebase`; verify the repo allows it (`gh api repos/{owner}/{repo} --jq .allow_rebase_merge`, enable via `gh repo edit --enable-rebase-merge` if off).

Apply via `gh api` on the branch protection endpoint only after the user picks; skipping entirely is a fine outcome.

## 4. Optional seeds

Offer, individually, only where missing — never scaffold unasked content:

- `CONTEXT.md` — created empty-ish per the `domain-modeling` format when the user wants the glossary discipline from day one.
- A build/test/format section in `CLAUDE.md` — the `implement` skill discovers its toolchain from repo docs; writing the three commands down once saves every future discovery.

## 5. Report

What was created, what already existed, what was skipped and why, and — if anything needed permissions the account lacks — exactly which step to rerun after access is granted.
