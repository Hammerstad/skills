---
name: review-performance
description: Performance review lens for a change, PR, or module - latency, throughput, memory, I/O, query patterns, scalability. Use when the user asks for a performance review, when changes touch hot paths, data access, loops over collections, or new I/O, or as a deep lens inside review-pr.
---

# Review: Performance

A performance lens over a defined scope — a PR, a diff, or a named hot path. Findings only: this skill never edits code. It **may** run things that turn hypotheses into numbers cheaply: existing benchmarks, `EXPLAIN` on a suspect query, a quick micro-benchmark in the scratchpad.

## Discipline

- **Every claim is a hypothesis until measured.** A finding either comes with a number (you ran something) or with a concrete measurement plan and acceptance criterion. Never assert a speedup you didn't measure.
- **Evidence or it doesn't exist.** file:line + snippet per finding; confidence (low/medium/high) with rationale; missing context (SLOs, traffic shape, data volumes) stated as unknowns, not invented.
- **Sweep wide, then filter.** The heuristic sweep collects every candidate; the filter step decides what ships. Never drop a candidate mid-sweep for feeling too small to mention — rank it low afterwards instead.
- **No forced findings.** Code that's fine is fine — say so and stop. This licenses an empty *result*, never a shallow sweep.
- **Class over instance.** Prefer findings that eliminate a whole class of overhead (remove the N+1) over micro-optimizations (shave the loop). Rank by expected p95/p99 or throughput impact, then effort and blast radius.

## Process

1. **Locate the hot paths in scope**: what runs per-request, per-message, per-row — versus once. Cold paths get at most a `nit:`.
2. **Sweep the heuristics** against the hot paths, collecting every candidate they raise:
   - **Data access** — N+1 queries; unbounded result sets; missing pagination or limits; non-sargable predicates; missing index for a new query shape; eager loading pulling object graphs where a projection would do.
   - **Loops** — allocations, large copies, boxing, string concatenation, or I/O inside tight loops; repeated work an invariant hoist or memo would remove; suspicious O(n²)/O(n·m) over unbounded inputs; wrong data structure (list scan where a set/dict belongs).
   - **I/O shape** — sync/blocking calls on hot or async paths; chatty per-item RPCs where a batch call exists; many small writes; missing streaming for large payloads.
   - **Concurrency** — lock contention on shared mutable state; critical sections doing I/O; CPU-heavy work on the event loop; unbounded parallelism (no backpressure, pool exhaustion).
   - **Caching** — recomputed values that are cache-shaped; caches without TTL/keys/bounds; stampede risk on expiry of a popular key.
   - **Serialization** — repeated (de)serialization of the same data; text formats on high-volume internal paths; redundant encode/decode round-trips.
3. **Filter** the candidates: each survivor cites file:line on a path you established is hot, and names the overhead it removes. Drop what rests on invented traffic shapes or data volumes. Cold-path candidates are not dropped — they ship as `nit:`.
4. **Measure or plan.** For each finding: run the cheap measurement if one is at hand. Otherwise write the plan: what to run (endpoint/function), against what (dataset size, concurrency), which signals to capture (latency percentiles, allocs/op, query counts, cache hit rate, pool stats), and the acceptance criterion (e.g. "p95 ≤ 40 ms at 300 rps", "1 query per request instead of N+1").

## Finding format

Title · Evidence (file:line + snippet) · Why it matters on this path (1-2 sentences) · Confidence + assumptions · Smallest remediation · Measurement (number obtained, or plan + acceptance criterion).

## Delivery

- Inside a `review-pr` run: findings become inline comments under that skill's contract; scope-wide observations (e.g. "this endpoint has no load test") go to the review body.
- Standalone: report in the terminal, same per-finding format.
