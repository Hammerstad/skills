---
name: review-performance
description: Performance review of a change, PR, or module - latency, throughput, memory, I/O, query patterns, scalability. Use when the user asks for a performance review, when changes touch hot paths, data access, loops over collections, or new I/O, or as a focused review inside review-pr.
---

# Review: Performance

A performance review of a defined scope: a PR, a diff, or a named hot path. This skill reports findings and does not edit code. It may run things that turn a hypothesis into a number cheaply: existing benchmarks, `EXPLAIN` on a suspect query, or a quick micro-benchmark in the scratchpad.

## How to talk to the user

Write to the user in plain, direct English, the way you would explain the work to a colleague. Use full sentences and everyday words, with no slogans and no invented terms. Lead with what you found, what you did, and what happens next. The full guide is [STYLE.md](../../STYLE.md).

## Rules

- **A claim is a hypothesis until it is measured.** Every finding comes either with a number you obtained by running something, or with a concrete measurement plan and an acceptance criterion. Do not assert a speedup you did not measure.
- **Every finding cites its evidence.** A file and line plus a snippet for each finding, a confidence level (low, medium, or high) with the reason, and any missing context (SLOs, traffic shape, data volumes) stated as unknown rather than made up.
- **Collect everything first, then decide what to report.** The sweep in step 2 collects every candidate. Step 3 decides what ships. Do not drop a candidate during the sweep for seeming too small to mention; rank it low afterwards instead.
- **Do not invent findings.** Code that is fine is fine. Say so and stop. This allows an empty result. It does not allow a shallow sweep.
- **Prefer fixes that remove a whole category of overhead** (removing the N+1 query) over micro-optimizations (shaving a loop). Rank by the expected effect on p95 or p99 latency or on throughput, then by effort and by how much could break.

## Process

1. **Find the hot paths in scope**: what runs per request, per message, or per row, as opposed to once. Cold paths get at most a `nit:`.
2. **Go through the checklist** against the hot paths, collecting every candidate it raises:
   - **Data access.** N+1 queries; unbounded result sets; missing pagination or limits; WHERE clauses the database cannot use an index for; a missing index for a new query shape; eager loading that pulls whole object graphs where a projection would do.
   - **Loops.** Allocations, large copies, boxing, string concatenation, or I/O inside tight loops; repeated work that could be hoisted out or memoized; suspicious O(n²) or O(n·m) over unbounded inputs; the wrong data structure (a list scan where a set or dictionary belongs).
   - **I/O shape.** Synchronous or blocking calls on hot or async paths; one RPC per item where a batch call exists; many small writes; no streaming for large payloads.
   - **Concurrency.** Lock contention on shared mutable state; I/O inside critical sections; CPU-heavy work on the event loop; unbounded parallelism (no backpressure, pool exhaustion).
   - **Caching.** Recomputed values that could be cached; caches without a TTL, proper keys, or a size bound; many callers recomputing at once when a popular key expires.
   - **Serialization.** Serializing or deserializing the same data repeatedly; text formats on high-volume internal paths; redundant encode and decode round trips.
3. **Decide which candidates to report.** Each survivor cites a file and line on a path you established is hot, and names the overhead it removes. Drop anything that rests on traffic shapes or data volumes you made up. Cold-path candidates are kept and reported as `nit:`.
4. **Measure or plan.** For each finding, run the cheap measurement if one is at hand. Otherwise write the plan: what to run (endpoint or function), against what (dataset size, concurrency), which signals to capture (latency percentiles, allocations per operation, query counts, cache hit rate, pool stats), and the acceptance criterion (for example "p95 at or under 40 ms at 300 requests per second", or "1 query per request instead of N+1").

## Finding format

Each finding has: a title, the evidence (file and line plus snippet), why it matters on this path in one or two sentences, confidence and assumptions, the smallest fix, and the measurement (the number you obtained, or the plan and acceptance criterion).

## Delivery

- Inside a `review-pr` run, findings become inline comments under that skill's rules, and scope-wide observations (for example "this endpoint has no load test") go in the review body.
- Standalone, report in the terminal using the same format per finding.
