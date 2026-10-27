# Security verification register

**Status: baseline created; independent verification not yet completed.** This register is an evidence tracker, not a claim of OWASP compliance or certification. The project owner or an independent reviewer must record commit-specific evidence and approve any exception.

Reference: OWASP Application Security Verification Standard (ASVS), version 5.0.0, at https://asvs.owasp.org/. Use the official versioned requirements when assigning exact ASVS identifiers; do not infer an identifier from a topic heading.

## Result definitions

- **Verified** — a reviewer inspected the implementation and repeatable evidence for the stated release.
- **Partial** — a control exists but coverage, deployment evidence, or independent review is incomplete.
- **Blocked** — a required external control or owner decision is missing.
- **Not applicable** — documented rationale approved by the reviewer.
- **Not assessed** — no adequate evidence yet.

Do not mark a control verified because a dependency is installed or a CI job is green.

## Verification register

| Domain | Required verification | Current status | Evidence required to close |
|---|---|---|---|
| Authentication | Institutional OIDC integration, issuer/audience/nonce validation, secure callback, session expiry and revocation | Blocked | Institution-selected IdP configuration, negative tests, reviewer and exact commit |
| Authorization | Server-side least privilege, request ownership, role checks, tenant isolation, direct API access | Partial | Full route matrix, cross-tenant tests against target deployment, independent review |
| Session and credentials | Secure cookies where applicable, rotation, revocation, no secrets in client bundles/logs | Not assessed | Configuration evidence, secret scan, session lifecycle tests |
| Input handling | Schema validation, size limits, safe parsing of uploaded genomic files, error-path coverage | Partial | Boundary/fuzz tests, malformed-file corpus, reviewed limits |
| Cryptography | Approved algorithms, key custody, rotation, authenticated encryption, failure handling | Blocked | Threat-model review and independent cryptographic review |
| Data protection | Minimize genomic data in logs, exports, traces and errors; retention/deletion controls | Partial | Log inspection, retention tests, documented data-flow review |
| Audit | Canonical event encoding, durable ordering, tamper detection, external independent anchoring | Blocked | Tamper/replay/gap tests plus independently administered anchor and key-custody evidence |
| Policy and consent | Versioned policy provenance, ambiguous-use hold, no synthetic consent in hosted authorization | Partial | Policy-change/withdrawal tests and institution-approved authoritative source before participant data |
| API security | Authentication and authorization on protected routes, rate limits, safe errors, no debug routes in hosted mode | Partial | Exact-deployment negative/abuse tests and reviewed API inventory |
| File processing | File size and decompression limits, corruption handling, checksum and format validation | Partial | Malformed/truncated/oversized input tests and ingestion provenance report |
| Dependencies | Dependency updates, vulnerability audit, lockfile strategy and remediation SLA | Partial | Successful scheduled audits, reviewed exceptions and tested update PRs |
| Build and deployment | Least-privilege workflow permissions, action pinning policy, reproducible release and rollback | Partial | Workflow review, action SHA pinning decision, artifact/release evidence |
| Container | Minimal image, non-root runtime where feasible, image vulnerability scan, secret-free layers | Not assessed | Container scan and deployment configuration evidence |
| Monitoring | Error/latency/dependency signals, authentication abuse and audit-integrity alerting | Blocked | Live alerts, owners, tested alert delivery and incident drill |
| Recovery | Durable database, encrypted backups, isolated restore drill, defined RPO/RTO | Blocked | Actual database/backup configuration and successful restore evidence |
| Privacy assurance | Threat model and empirical evaluation of every published privacy claim | Blocked | Reproducible evaluation, limitations, independent privacy review |
| Accessibility | Automated checks plus keyboard and assistive-technology manual testing | Partial | Dated manual test report and remediation evidence |
| Governance | Institutional ethics/legal approval for each controlled dataset and use | Blocked for controlled data | Written approval from the responsible institution/data controller |

## Release sign-off

Complete this table for every candidate release:

- Release tag and full commit SHA:
- Environment and hosting service:
- Data source/release and provenance hash:
- CI workflow run URLs:
- Live smoke-test report:
- Database migration and persistence evidence:
- Backup/restore evidence:
- Authentication and authorization review:
- Consent/policy review:
- Audit-anchor verification:
- Dependency and secret-scan results:
- Independent security/privacy reviewer:
- Manual accessibility review:
- Open findings and accepted risk owner:
- Release decision and date:

**Release rule:** Until the blocked infrastructure and governance items are verified, classify the hosted service as a public-genotype research prototype. Do not enable private/controlled-access or clinical genomic data.
