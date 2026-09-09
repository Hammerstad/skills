# Global preferences

<!-- Shared across machines. Install with the `global-preferences` skill, which
     points ~/.claude/CLAUDE.md at this file so `git pull` updates every machine. -->

## Commits
- Do not add a `Co-authored-by:` trailer (or any "Generated with Claude" line) to commit messages.
- Do not use Conventional Commits — no `feat:` / `fix:` / `chore:` prefixes. Use a plain, descriptive summary line.

## Branch work goes in a worktree

I often have three or more sessions running against the same repo at once. Start any branch work in
its own worktree (`git worktree add --detach <scratchpad>/wt<n> <base>`) rather than running
`git switch` or `gh pr checkout` in the shared checkout. Push only your own commits. If a shared
checkout has already collected commits from another session, cherry-pick only yours onto the
branch's pushed tip inside a worktree and push from there. Never force-push a shared branch;
another session may be working against it.

## How to write to me

The Concise output style sets how long a reply is. These rules are about the words in it, and they apply to chat, to commit messages, and to anything you write into GitHub or into docs.

- Lead with the result. First line: what happened or what you found. Then what I have to do. Stop there. Add details when I ask for them.
- If something failed or was skipped, that is the first line, with the output.
- Say the literal thing. Mannered prose swaps a direct statement for a metaphor or a flourish: "a landmine with no warning sign" for "this breaks when vite is updated", "fold this in" for "add this", "silently" for "without an error", "the key insight" for nothing at all. Metaphors carry meanings you did not choose, and I have to translate them. When a literal phrase is available, use it.
- Do not sell and do not narrate. A recommendation gets its reason in one clause or none. Cut "this matters more than it looks", "in other words", "worth noting", "the real question is". Do not describe what you are about to do or how you reasoned.
- Use everyday words. Established engineering terms are fine when there is no short everyday equivalent (rebase, worktree, ADR, regression test, N+1 query). Spell out any other acronym the first time it appears. Do not coin a name for something that has an ordinary description.
- Format for the reader, not for effect. Bullets when there are several parallel items, a table when there are rows and columns. No bold lead-ins on bullets. Prefer a period or a comma to an em-dash. Commands, paths, and error text go in backticks or a code block, not in the middle of a sentence.
- Before sending, reread the draft once and delete: metaphors, sentences that justify a recommendation, anything I did not ask for.

American spelling. The same rules, with examples, are in `STYLE.md` next to this file, which the skills carry inline.
