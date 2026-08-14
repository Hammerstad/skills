---
name: review-security
description: Security review lens for a change, PR, or module - authentication, authorization, input handling, secrets, crypto, data isolation, supply chain. Use when the user asks for a security review, when reviewing changes that touch auth/input/secrets/storage/pipelines, or as a deep lens inside review-pr.
---

# Review: Security

A deep security lens over a defined scope — a PR, a diff, or a named module. Findings only: this skill never edits code. It **may** run read-only commands that sharpen evidence (grep for secrets, `npm audit` / `dotnet list package --vulnerable`, reading CI workflow permissions).

## Discipline

- **Evidence or it doesn't exist.** Every finding cites file:line or a config excerpt from the actual scope. No finding from vibes, no invented paths, no assumed infrastructure.
- **Every claim is potential until corroborated.** Mark confidence (low/medium/high) with a one-line rationale. Unknowns that limit the review (no threat model, unclear trust boundary) get stated, not guessed around.
- **No forced findings.** A clean scope gets "no security findings in this scope" — that is a successful review, not a failed one.
- **Smallest fix, and how to prove it.** Each finding proposes the minimal remediation and a verification test (usually a negative test: the request that should be rejected).

## Process

1. **Map the scope**: entry points, assets touched, data flows in/out, trust boundaries crossed. One short paragraph — unknowns listed explicitly.
2. **Sweep the checklist** against the code, keeping only evidence-backed findings:
   - **AuthN/AuthZ** — is every sensitive operation in scope guarded? Check the *callers*: an authorized endpoint calling an unguarded internal path is the classic hole. IDOR: is object ownership checked, or only identity?
   - **Input handling** — validation at trust boundaries, output encoding, injection surfaces (SQL, command, path, template, XSS), deserialization of untrusted data.
   - **Secrets** — in code, config, logs, error messages, test fixtures, or git history introduced by this change. Secrets belong in the environment/vault.
   - **Crypto** — home-rolled primitives, weak algorithms, non-CSPRNG randomness for tokens, keys/IVs handled as ordinary strings.
   - **Errors & logging** — stack traces or sensitive data leaking to clients or logs; security-relevant actions that leave no audit trace.
   - **Config & egress** — permissive CORS, disabled TLS verification, debug endpoints, overly broad network/file permissions.
   - **Isolation** — multi-tenant data paths: can tenant A's identifier reach tenant B's rows? Queries missing the tenant/owner predicate.
   - **Supply chain** — new dependencies (typosquats, maintenance state), unpinned versions where the ecosystem pins, CI workflow permissions widened (`pull_request_target`, secrets exposure), install scripts.
3. **Rank** by exploitability × impact, High/Medium/Low.

## Finding format

Title · Evidence (file:line + snippet) · Abuse case (1-2 sentences: who does what, and what they get) · Confidence + assumptions · Smallest remediation · Verification test.

## Delivery

- Inside a `review-pr` run: findings become inline comments under that skill's contract (they are findings, never `nit:`), with scope-wide observations going to the review body.
- Standalone: report in the terminal, same per-finding format.
