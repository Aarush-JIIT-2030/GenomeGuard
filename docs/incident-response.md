# Incident response and recovery runbooks

**Scope:** GenomeGuard public-genotype research instance. This document is an operational template; it does not claim monitoring, alert delivery, backups, or recovery drills are already configured.

## Roles and communication

Before production use, name a primary incident owner, backup owner, hosting/database operators, institutional privacy/security contact, and decision-maker for suspending research access. Keep contact details in an approved private operational system, not in this public repository.

For any suspected exposure of participant data, assume the public research prototype is not an approved environment: stop data processing, preserve relevant metadata without copying genomic payloads, notify the responsible organization through its approved incident process, and obtain legal/privacy advice before further handling.

## First response checklist

1. Record UTC detection time, reporter, affected service/environment, deployed commit, and a short symptom summary.
2. Assign an incident ID and owner; classify severity using the organization's incident policy.
3. Preserve relevant application, provider, identity, and audit metadata. Do not put secrets, raw genotypes, participant identifiers, or tokens in the ticket.
4. Decide whether to disable submissions or restrict traffic. Prefer a safe service interruption over uncontrolled data release.
5. Rotate affected credentials using the hosting provider and identity provider; do not paste new secrets into GitHub issues or chat.
6. Record actions, timestamps, decisions, and evidence references in an access-controlled incident record.
7. Validate recovery with negative authorization tests and a source/commit check before reopening traffic.
8. Complete a post-incident review with root cause, impact, remediation owner, due date, and regression test.

## Database unavailable

- Confirm provider status and connectivity from the service environment without printing the connection string.
- Confirm /health reflects process liveness and /health/ready remains not-ready when required storage is unavailable.
- Do not silently switch to SQLite or an in-memory store for hosted writes.
- Pause write operations if transactional persistence cannot be guaranteed.
- Restore connectivity or fail over only using the approved provider procedure.
- After recovery, verify migration state, request ownership, decision/audit consistency, and a controlled read/write workflow.
- Record the outage window and whether any acknowledged writes were lost.

## Failed migration

- Stop deployment promotion; preserve the failing migration log with secrets redacted.
- Do not edit the production schema manually without a reviewed recovery plan.
- Confirm the last successful migration version and take/verify a backup before any corrective action.
- Reproduce against an isolated database copy, prepare a forward-fix or reviewed restore plan, and obtain operator approval.
- Re-run migration and application acceptance checks against the restored/fixed database.
- Document the schema version and exact commit before resuming deploys.

## Suspected unauthorized access or credential compromise

- Restrict or disable the affected account/key/session; preserve audit metadata.
- Rotate credentials and invalidate sessions through the authoritative identity/secret provider.
- Review affected request IDs, role/tenant checks, exports, and relevant audit events. Avoid copying genomic payloads into incident records.
- Test cross-user and cross-tenant denial on the exact affected release.
- Notify the responsible security/privacy owner and follow applicable notification obligations.
- Reopen access only after the root cause is mitigated and a regression test exists.

## Audit verification failure

- Treat a failed chain verification, unexpected sequence gap, or failed external checkpoint as a security-relevant event.
- Suspend privileged decisions and data release if trustworthy decision history is required but cannot be established.
- Preserve the current database snapshot and verification output under controlled access.
- Compare against independently anchored checkpoints if such an anchor is configured. A local hash chain alone cannot prove that a privileged database operator did not rewrite and recompute history.
- Do not repair or rebuild the chain in place before preserving evidence and obtaining review.
- Resume only after the authorized owner documents the cause, recovery method, and residual uncertainty.

## Corrupt or untrusted dataset ingestion

- Stop publication of the affected dataset release and mark it unavailable.
- Preserve source URL, release identifier, retrieval time, checksums, validation output, and software versions.
- Re-fetch only from the authoritative source and verify checksums/integrity where the source publishes them.
- Validate format, reference assembly, sample/variant counts, and metadata before making the release visible.
- Re-run provenance and policy review. A checksum is not proof of legal permission or consent.
- Record a new immutable release identifier rather than silently overwriting provenance.

## Failed backup restoration

- Keep the failed restore isolated; never point production at an unverified copy.
- Record backup timestamp, encryption/key version, restore target, error, and database schema version.
- Verify backup integrity, key access, extension compatibility, migration state, and row-level/application invariants.
- Repeat only after the failure cause and data-loss risk are understood.
- Reopen service only after application-level acceptance and authorization tests pass.

## Bad deployment and rollback

- Identify the exact current and last-known-good commit and provider deployment IDs.
- Roll back using the provider's supported mechanism; do not assume code rollback reverses schema changes.
- Verify health, readiness, public dataset provenance, demo-route disablement, and unauthenticated denial.
- Run a read-only smoke suite first, then an approved controlled write/read test if persistent storage is configured.
- Document any migration compatibility issue and block further deploys until a reviewed fix is available.

## Required operational exercises

Before claiming operational readiness, run each scenario in an isolated staging environment, capture timestamps and evidence links, record detection and recovery times, and assign follow-up owners. Define the service's RPO/RTO and backup retention with the actual service owner. No recovery objective is considered met until demonstrated by a successful drill.
