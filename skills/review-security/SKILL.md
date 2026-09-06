---
name: review-security
description: Security review of a change, PR, or module - authentication, authorization, input handling, secrets, crypto, data isolation, supply chain. Use when the user asks for a security review, when reviewing changes that touch auth/input/secrets/storage/pipelines, or as a focused review inside review-pr.
---

# Review: Security

A thorough security review of a defined scope: a PR, a diff, or a named module. This skill reports findings and does not edit code. It may run read-only commands that sharpen the evidence: grepping for secrets, `npm audit` or `dotnet list package --vulnerable`, or reading CI workflow permissions.

## How to talk to the user

Write to the user in plain, direct English, the way you would explain the work to a colleague. Use full sentences and everyday words, with no slogans and no invented terms. Lead with what you found, what you did, and what happens next. The full guide is [STYLE.md](../../STYLE.md).

## Rules

- **Every finding cites its evidence.** A file and line, or a config excerpt, from the actual scope. No findings from a hunch, no invented paths, no assumed infrastructure.
- **A claim is potential until it is corroborated.** Give each finding a confidence level (low, medium, or high) with a one-line reason. State the unknowns that limit the review (no threat model, an unclear trust boundary) rather than guessing around them.
- **Collect everything first, then decide what to report.** The checklist sweep collects every candidate. The filter step decides what ships. Do not suppress a candidate during the sweep because it seems minor or probably intentional; make that judgment one step later, with all the candidates in front of you.
- **Do not invent findings.** A clean scope gets "no security findings in this scope". That is a successful review. This allows an empty result. It does not allow a shallow sweep.
- **The smallest fix, and how to prove it.** Each finding proposes the smallest fix and a test that verifies it, usually a negative test: the request that should be rejected.

## Process

1. **Map the scope**: entry points, assets touched, data flowing in and out, and trust boundaries crossed. One short paragraph, with the unknowns listed explicitly.
2. **Go through the checklist** against the code, collecting every candidate it raises:
   - **Authentication and authorization.** Is every sensitive operation in scope guarded? Check the callers: an authorized endpoint that calls an unguarded internal path is the classic hole. Is object ownership checked, or only identity? An identity-only check lets a user reach other users' objects by changing an ID.
   - **Input handling.** Validation at trust boundaries, output encoding, injection surfaces (SQL, command, path, template, XSS), and deserialization of untrusted data.
   - **Secrets.** In code, config, logs, error messages, test fixtures, or git history introduced by this change. Secrets belong in the environment or a vault.
   - **Crypto.** Home-made primitives, weak algorithms, randomness that is not cryptographically secure used for tokens, and keys or IVs handled as ordinary strings.
   - **Errors and logging.** Stack traces or sensitive data leaking to clients or logs, and security-relevant actions that leave no audit trail.
   - **Config and egress.** Permissive CORS, disabled TLS verification, debug endpoints, and network or file permissions that are broader than needed.
   - **Isolation.** Multi-tenant data paths: can tenant A's identifier reach tenant B's rows? Queries missing the tenant or owner condition.
   - **Supply chain.** New dependencies (typosquats, maintenance state), unpinned versions where the ecosystem pins them, CI workflow permissions that were widened (`pull_request_target`, secrets exposure), and install scripts.
3. **Decide which candidates to report.** Each survivor cites a file and line or a config excerpt from the actual scope and describes a concrete abuse case. Drop anything that rests on assumed infrastructure or on paths you never read. A real finding you are only medium-confident about survives; say so in its confidence line rather than dropping it.
4. **Rank** by how exploitable it is and how much damage it does: High, Medium, or Low.

## Finding format

Each finding has: a title, the evidence (file and line plus snippet), the abuse case in one or two sentences (who does what, and what they get), confidence and assumptions, the smallest fix, and the verification test.

## Delivery

- Inside a `review-pr` run, findings become inline comments under that skill's rules, and scope-wide observations go in the review body. Security findings are never marked `nit:`.
- Standalone, report in the terminal using the same format per finding.
