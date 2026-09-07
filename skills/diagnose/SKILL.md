---
name: diagnose
description: A step-by-step method for hard bugs and performance regressions - reproduce the bug with an automated check, shrink the reproduction, list possible causes, test them one at a time, fix, and add a regression test. Use when user says "diagnose this" / "debug this", reports a bug, says something is broken/throwing/failing, or describes a performance regression.
---

# Diagnose

A method for hard bugs. Work through the phases in order, and skip one only when you can say why it does not apply.

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

## Before you start

When exploring the codebase, read `CONTEXT.md` if it exists to learn the project's vocabulary and how the relevant modules fit together, and check the ADRs for the area you are touching.

## Tracked issues

If this diagnosis belongs to an issue in the tracker, either because the user names one or because it carries the `needs-diagnosis` label described in the `labels` skill, read the issue and its comments first. Reproduction reports and earlier attempts live there. When you find the root cause, post it back as an issue comment with the reproduction command, the cause, and the evidence. Then change the label: `ready-for-agent` if the fix is now clear enough to implement directly, or `needs-grilling` if it opens a design discussion. If the session ends without a cause, post what you tried and what evidence is missing, and change the label to `needs-input` if a specific question for the maintainer came up.

## Redact secrets

This skill has you show commands, outputs, and captured files. Remove every secret before showing anything and write `<REDACTED>` in its place. Build your checks so they read credentials from environment variables, so that the credential stays in the environment rather than in what you show. Captured requests carry auth headers, so quote only the lines that matter.

If the redacted output is not enough to diagnose the bug, say so and ask the user.

## Phase 1: Build a feedback loop

A feedback loop here means an automated check that fails on this specific bug and passes once the bug is fixed.

This phase matters most. With such a check you will find the cause, because bisection, testing hypotheses, and adding instrumentation all rely on it. Without one, reading code will not get you there.

Spend more effort here than feels proportionate. Try many approaches before concluding that a check cannot be built.

### Ways to build one, roughly in order of preference

1. A failing test at whichever level reaches the bug: unit, integration, or end to end.
2. A curl or HTTP script against a running dev server.
3. A CLI invocation with a fixture input, diffing stdout against a known-good snapshot.
4. A headless browser script (Playwright or Puppeteer) that drives the UI and asserts on the DOM, console, or network.
5. Replaying a captured trace. Save a real network request, payload, or event log to disk and replay it through the code path in isolation.
6. A throwaway harness. Spin up a minimal subset of the system, one service with mocked dependencies, that exercises the buggy code path with a single function call.
7. A property or fuzz loop. If the bug is "sometimes wrong output", run 1000 random inputs and look for the failure.
8. A bisection harness. If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so you can run `git bisect run` over it.
9. A differential check. Run the same input through the old version and the new version (or two configs) and diff the outputs.
10. A script that walks a person through the steps. Use this last. If a human has to click, drive them with `scripts/hitl-loop.template.sh` so that the steps and their results are still captured for you.

Once the check exists, the rest of the work is mostly routine.

### Make the check better

Once you have a check that works, improve it:

- Make it faster. Cache setup, skip unrelated initialization, narrow the test scope.
- Make the signal sharper. Assert on the specific symptom rather than on "did not crash".
- Make it deterministic. Pin the time, seed the random number generator, isolate the filesystem, stub the network.

A 30-second check that fails only sometimes is barely better than none. A 2-second check that fails every time is what you want.

### Bugs that do not reproduce every time

Aim for a higher reproduction rate rather than a perfectly clean reproduction. Run the trigger 100 times, run it in parallel, add load, narrow timing windows, inject sleeps. A bug that shows up 50% of the time can be debugged; one that shows up 1% of the time cannot. Keep raising the rate until you can work with it.

### When you cannot build a check at all

Stop and say so. List what you tried. Ask the user for one of: (a) access to an environment where the bug reproduces, (b) a redacted capture (a HAR file, log dump, core dump, or screen recording with timestamps), or (c) permission to add temporary instrumentation in production. Do not move on to hypotheses without a check.

### When Phase 1 is done

Phase 1 is done when you can name one command (a script path, a test invocation, a curl) that you have already run at least once, showing the invocation and its redacted output, and that is:

- [ ] Specific to this bug. It drives the actual buggy code path and asserts on the user's exact symptom, so it fails on this bug and passes once the bug is fixed. "Runs without erroring" does not count.
- [ ] Deterministic. It gives the same verdict every run, or for intermittent bugs, a high and stable reproduction rate as described above.
- [ ] Fast. It runs in seconds.
- [ ] Runnable by you without a human, except through `scripts/hitl-loop.template.sh`.

If you catch yourself reading code to build a theory before this command exists, stop. Jumping straight to a hypothesis is the mistake this skill exists to prevent. Without a failing check there is no Phase 2.

## Phase 2: Reproduce and shrink

Run the check and watch it fail.

Confirm:

- [ ] The check produces the failure the user described, and not a different failure nearby. If it catches a different bug, you will fix the wrong bug.
- [ ] The failure reproduces across several runs, or for intermittent bugs, at a rate you can work with.
- [ ] You have captured the exact symptom (error message, wrong output, timing) so that later phases can verify the fix addresses it.

### Shrink the reproduction

Once the check fails, shrink the scenario to the smallest one that still fails. Remove inputs, callers, config, data, and steps one at a time, re-running the check after each removal, and keep only what is needed for the failure to occur.

This is worth doing because a minimal reproduction leaves fewer things to suspect in Phase 3 and becomes a clean regression test in Phase 5.

You are done when removing any remaining element makes the check pass.

Do not move on until you have both reproduced and shrunk the scenario.

## Phase 3: List possible causes

Write down 3 to 5 ranked hypotheses before testing any of them, one line each. If you only generate one, you will anchor on the first plausible idea.

Each hypothesis must make a prediction you can test:

> "If <X> is the cause, then <changing Y> will make the bug disappear, or <changing Z> will make it worse."

If you cannot state the prediction, the hypothesis is a guess. Discard it or sharpen it.

Show the ranked list to the user before testing. They often know something that reorders it at once ("we just deployed a change to #3"), or have already ruled some out. Do not block on their reply. If the user is not responding, proceed with your own ranking.

## Phase 4: Add instrumentation

Each probe must test a specific prediction from Phase 3. Change one variable at a time.

Preferred tools, in order:

1. A debugger or REPL if the environment supports it. One breakpoint beats ten logs.
2. Targeted logs at the boundaries that tell the hypotheses apart.
3. Never "log everything and grep".

Tag every debug log with a unique prefix, for example `[DEBUG-a4f2]`. Cleanup at the end is then a single grep. Tagged logs are easy to find and remove; untagged ones get left behind.

For performance regressions, logs are usually the wrong tool. Establish a baseline measurement first (a timing harness, `performance.now()`, a profiler, a query plan), then bisect. Measure before you fix.

## Phase 5: Fix and add a regression test

Write the regression test before the fix, but only if there is a right place to put it.

The right place is one where the test exercises the real bug pattern the way it occurs at the call site. If the only available place is too shallow (a single-caller test when the bug needs several callers, or a unit test that cannot reproduce the chain of calls that triggered the bug), a regression test there gives false confidence.

If no right place exists, that is a finding in itself. Note it: the structure of the codebase is preventing the bug from being locked down by a test. Bring it up in the last phase.

If a right place exists:

1. Turn the shrunk reproduction into a failing test there.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 check against the original, unshrunk scenario.

## Phase 6: Clean up and write up

Required before declaring done:

- [ ] The original reproduction no longer reproduces (re-run the Phase 1 check)
- [ ] The regression test passes, or the lack of a place for one is documented
- [ ] All `[DEBUG-...]` instrumentation is removed (grep for the prefix)
- [ ] Throwaway prototypes are deleted, or moved to a clearly marked debug location
- [ ] The hypothesis that turned out to be correct is stated in the commit or PR message, so that the next person learns from it

Report in the terminal, under eight lines: the cause in one sentence, the fix commit, the name of the regression test, and the result of re-running the Phase 1 check. Do not retell the investigation; the issue comment and the commit message hold that.

Then ask: what would have prevented this bug? If the answer involves a structural change (no good place for a test, tangled callers, hidden coupling), hand off to the `/improve-codebase-architecture` skill with the specifics. Make that recommendation after the fix is in rather than before, since you know more now than when you started.
