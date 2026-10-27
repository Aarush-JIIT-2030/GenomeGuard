# Production assurance implementation status — 26 October 2026

## Summary

This change set implements repository-side assurance controls that can be delivered without inventing infrastructure, identity, consent, audit, or review evidence. It does **not** convert GenomeGuard into production-ready software. The current release remains a public-genotype research prototype.

The supplied completion audit is the acceptance checklist. Statuses below separate repository work from controls that require an infrastructure owner, institutional authority, or independent reviewer.

## Implemented in this change set

| Area from completion audit | Change in this branch | What this does not prove |
|---|---|---|
| Supply-chain security | Adds a scheduled/on-push/pull-request CodeQL workflow for Python and JavaScript; adds a strict Python dependency audit; adds Gitleaks secret scanning | No scan has passed until GitHub Actions runs against this branch; no scan can guarantee absence of all vulnerabilities or leaked credentials |
| Dependency hygiene | Adds weekly Dependabot updates for Python and GitHub Actions | Updates still require review, CI, compatibility checks, and remediation ownership |
| OWASP ASVS baseline | Adds a verification register with explicit evidence criteria and truthful current statuses | Not a compliance attestation or certification; exact requirements need independent review |
| Incident response | Adds database outage, migration, credential compromise, audit failure, dataset corruption, restore failure, and rollback runbooks | Monitoring, alerting, backups, named incident owners, and drills are not automatically configured |
| Evidence and release discipline | Documents release sign-off fields for exact commit, source provenance, CI, live acceptance, recovery, identity, consent, audit, security, and accessibility evidence | No release gate should be marked complete without actual evidence from its target environment |

## Still blocked — do not mark complete

### Infrastructure and persistence
- No dedicated GenomeGuard managed PostgreSQL database is configured in the audited Render workspace.
- GG_DATABASE_URL is not configured on the hosted service.
- Request/audit durability across restart and redeploy is unverified.
- Backup policy, isolated restore drill, RPO/RTO, and operational ownership remain unverified.
- The repository blueprint declares /health, but the audited Render service setting reported an empty health-check path. This provider-side setting must be corrected and checked on Render itself.

### Identity and governance
- Institutional OIDC/SSO, verified organizational membership, lifecycle revocation, and institution-specific MFA are absent.
- The public 1000 Genomes/IGSR dataset has a dataset-level public-release policy mapping, not participant-specific consent.
- No authoritative participant consent/withdrawal integration is configured. Synthetic consent must never be used to authorize a real dataset.
- Legal, ethics, and data-controller approval are required before any controlled-access or participant-level data is used.

### Audit, scientific assurance, and interoperability
- Local hash chaining is not an independent audit anchor.
- Risk scores are heuristics; the privacy ledger is not a formally audited differential-privacy implementation.
- Beacon-style and FHIR validation workflows do not establish full interoperability certification or legal consent.
- Independent security/penetration, privacy, and cryptographic reviews have not been completed.
- Manual screen-reader/assistive-technology review is outstanding.

### Live product acceptance and operations
- The new security workflow must run and its findings must be triaged; this branch's CI/security outcome is not known before GitHub executes it.
- The exact deployed commit and live application must be re-tested after changes are merged and deployed.
- Monitoring/alert delivery, secret rotation exercises, data-retention/deletion, incident drills, and rollback exercises remain unverified.
- User testing must demonstrate that researcher and steward workflows are understandable without developer assistance.

## Why these blockers cannot be completed in source code alone

A source commit cannot provision and verify a paid managed database without selecting a budget and accountable operator. It cannot invent an institution's identity provider, real consent source, or ethics approval. Nor can it substitute mocked data for a restore drill, external audit checkpoint, independent penetration test, or manual accessibility review. Doing so would create a false completion claim and weaken the product's trustworthiness.

## Release classification

**Current release classification: public-genotype research prototype; not production-ready for private, controlled-access, participant-level, or clinical genomic data.**

Keep the readiness endpoint fail-closed until the real controls exist and have been verified against the intended deployment. Do not change the readiness response merely to make deployment indicators green.
