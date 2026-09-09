---
name: global-preferences
description: Keep the user's global Claude preferences in one file in this repo and shared across machines - install them on a machine, or add a new preference. Use when the user says "add this to my global preferences", "make this a global rule for all projects", "remember this everywhere", "set up my global CLAUDE.md on this machine", or asks why a preference is not in effect on one machine.
---

# Global Preferences

The user's global preferences live in one file in this repo, [global-CLAUDE.md](../../global-CLAUDE.md). On each machine `~/.claude/CLAUDE.md` is a single line that imports it, so `git pull` updates every machine at once.

This skill does two jobs. Pick from what the user asked:

- **Install** the preferences on this machine (new machine, or the import is missing or broken).
- **Add** a preference to the shared file so every machine picks it up.

Always start with step 1. It is what makes both jobs safe.

## How to talk to the user

Write like an engineer reporting to a colleague who is short on time. These rules apply to replies in the chat and to everything you write into GitHub or into docs.

- Lead with the result. First line: what happened or what you found. Then what the reader has to do. Stop there. Add details only when asked.
- If something failed or was skipped, that is the first line, with the output.
- Keep a chat reply under ten lines unless it is a list of findings. One idea per sentence. One sentence per bullet. A reply that repeats what a diff or a tool result already shows adds nothing.
- Say the literal thing. Mannered prose swaps a direct statement for a metaphor or a flourish: "a landmine with no warning sign" for "this breaks when vite is updated", "fold this in" for "add this", "silently" for "without an error", "the key insight" for nothing at all. Metaphors carry meanings you did not choose, and the reader has to translate them. When a literal phrase is available, use it.
- Do not sell and do not narrate. A recommendation gets its reason in one clause or none. Cut "this matters more than it looks", "in other words", "worth noting", "the real question is". Do not describe what you are about to do or how you reasoned.
- Use everyday words. Established engineering terms are fine when there is no short everyday equivalent (rebase, worktree, ADR, regression test, N+1 query). Spell out any other acronym the first time it appears. Do not coin a name for something that has an ordinary description.
- Format for the reader, not for effect. Bullets when there are several parallel items, a table when there are rows and columns, a heading only in a document that is long enough to navigate. No bold lead-ins on bullets. Bold at most the one thing the reader must not miss. Prefer a period or a comma to an em-dash. Commands, paths, and error text go in backticks or a code block, not in the middle of a sentence.
- Before sending, reread the draft once and delete: metaphors, sentences that justify a recommendation, anything the reader did not ask for.

## 1. Find the checkout and pull it first

Never read or edit `global-CLAUDE.md` before the checkout is current. A stale checkout means editing a file that has already changed on another machine.

Find the clone. Try, in order: the path in the existing `~/.claude/CLAUDE.md` import line, then `~/code/skills`, then a search of the usual parents (`~/code`, `~/src`, `~/projects`, `~/dev`). If there is none, clone it:

```sh
git clone git@github.com:Hammerstad/skills.git ~/code/skills
```

Then bring it up to date:

```sh
git -C <repo> fetch --prune origin
git -C <repo> status --short --branch
```

- Checkout on `master` and clean: `git -C <repo> pull --ff-only`.
- Checkout on another branch, or dirty: do not switch it and do not stash. Another session may be working there. `fetch` was enough for this skill's own work, which happens in a worktree off `origin/master`. Tell the user in one line that the shared checkout is parked on `<branch>`, because the import reads the file as that branch has it, so a preference just pushed to `master` will not be in effect there until the checkout returns to `master`.

## 2. Install on this machine

Read `~/.claude/CLAUDE.md` before writing anything to it. There are three cases:

1. **Missing.** Write the import line.
2. **Already the import line**, pointing at this clone. Nothing to do. Say so.
3. **Real content.** Diff it against `global-CLAUDE.md`. If it matches, replace it with the import line. If it differs, show the user the lines that only exist locally and ask whether to move them into `global-CLAUDE.md` (step 3) or leave the machine as it is. Never overwrite preferences that exist only on this machine.

The import line, with the real path (a `~` path is fine and travels better than an absolute one):

```
@~/code/skills/global-CLAUDE.md
```

Imports are read when a session starts, so the current session does not see the change. Tell the user to start a new session and run `/memory`, which lists the loaded files, to confirm the import resolved. If it does not resolve on that machine, the fallback is a copy of the file instead of the import, and the cost of the copy is that it has to be re-copied after every pull.

## 3. Add a preference

Only genuinely global preferences belong in this file. Everything else has a better home, and putting it here spends context in every session on every project:

- Applies to every project and every repo: this file.
- Applies to one repo: that repo's `CLAUDE.md`.
- Applies to one session: nothing to write.
- Automated behavior ("whenever X happens, do Y"): a hook in `settings.json`, not a preference. Claude cannot run these; the harness does. Say so and stop.

The repo is public. Nothing employer-specific goes in the file: no employer or client names, no internal hostnames or URLs, no ticket keys, no private paths, no names of unreleased products. If the user's wording carries any of it, rewrite the preference so it holds without them, and say what you dropped.

Write it in the file's existing voice: first person about the user, imperative to the agent, the reason in one clause or none, and follow [STYLE.md](../../STYLE.md). Put it under the heading that fits; add a heading only if none does. Keep the whole file short.

Then commit from a worktree off `origin/master`, per the worktree preference the file itself states:

```sh
git -C <repo> worktree add --detach <scratchpad>/wt-prefs origin/master
git -C <scratchpad>/wt-prefs switch -c global-preference-<slug>
```

Edit there, commit with a plain summary line (no Conventional Commits prefix, no `Co-authored-by` trailer), and push. Ask before opening a pull request: for a one-line preference, pushing the branch and merging it is the whole job, and the review skills add nothing. Remove the worktree when the branch is merged.

The other machines get the change on their next `git pull` of this repo, with no further setup, as long as the import from step 2 is in place.

## 4. Report

One block:

- What changed: the preference added, or the machine wired up.
- Where: repo file, machine file, or both.
- Anything skipped, and why, including content dropped as employer-specific.
- What the user has to do: start a new session for it to load, and `git pull` on the other machines.
