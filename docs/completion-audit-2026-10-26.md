# GenomeGuard completion audit — 26 October 2026

## Executive result

**Release classification: hosted public-genotype research prototype; NOT production-ready for private, controlled-access, or clinical genomic data.**

This is an evidence-based completion audit, not a claim that all production gates are closed. The product has a deployed research workflow, real public genotype input, automated tests, API authorization tests, and explicit product-boundary copy. Production readiness is blocked by missing operational controls that cannot be safely simulated or inferred from CI.

## Verified repository and deployment state

- Repository: https://github.com/kaustubhdua/GenomeGuard
- Live URL: https://genomeguard.onrender.com
- Main commit audited: `a9aed73c4c0ffad632b892eb98eee294a4e9d751` (PR #36 merge)
- Render service: `srv-dbev1ka9lscs738813t0`
- Render deployment: `dep-dbfiug0u01pc73beus5g`, status `live` when checked on 26 October 2026; deployed source commit `a9aed73c4c0ffad632b892eb98eee294a4e9d751`.
- Render plan: Free; region Singapore; one instance; auto-deploy from `main`.
- Render reports no GenomeGuard PostgreSQL instance. `GG_DATABASE_URL` is not configured.
- The Render service configuration currently reports an empty health-check path, even though `render.yaml` declares `/health`. The deployed provider configuration must be corrected and re-verified.
- The live URL and health endpoints could not be independently fetched by the available web verification client during this audit. Render's deployment state is not a substitute for end-to-end runtime acceptance.
- PR #34 corrected hosted capability/provenance claims. PR #36 added route-driven authorization tests and mobile drawer keyboard improvements. PR #34 CI completed successfully; PR #36's description records local test, lint, and browser smoke success. The deployment provider reports the merged main commit live.

## Data authenticity and scope

The hosted research image is built from public 1000 Genomes / IGSR chromosome 22 genotype calls (600 samples × 3,000 variants) with source and policy provenance hashes. This is real public dataset content, not fabricated private participant data.

Important boundaries:
- The dataset policy is a documented, dataset-level mapping of public-release terms. It is **not** participant-specific consent, a legal authorization, or proof of suitability for a particular research purpose.
- Local demo and test workflows intentionally use synthetic fixtures. They must remain clearly labelled and must never be described as real people or actual consent.
- The hosted mode disables demo/synthetic participant workflows.
- Risk scores are heuristics, not independently validated privacy guarantees.
- The privacy ledger is not a formally audited differential-privacy implementation.
- Built-in explanation templates are used; no live LLM is configured.
- The audit log is a local hash chain, not an independent immutable anchor.
- The Beacon/FHIR artifacts demonstrate selected schema checks, not full interoperability certification or legally valid consent.
- This product must not be used for clinical decisions or private/controlled-access participant data.

## Evidence-backed status matrix

| Area | Status | Evidence / next requirement |
|---|---|---|
| Public-genotype research mode | Implemented; deployment marked live | Public 1000 Genomes/IGSR source; source/policy provenance is described in product docs. Repeat live end-to-end smoke against the current deployment when network access is available. |
| Product capability claims | Improved | Hosted mode distinguishes dataset-level policy from participant-specific consent, heuristic risk, templates, and local audit chain. |
| CI and browser checks | Automated checks exist and have passed on tested changes | CI includes lint, tests, real PostgreSQL integration tests in an ephemeral CI database, evaluations, demo checks, Python/JS syntax, Playwright routes, responsive checks, and axe-core checks. CI does not prove hosted persistence or operational readiness. |
| Authorization regression coverage | Improved | PR #36 added a route-driven authorization matrix for admin, requester, and donor routes plus journey tests. Independent security testing remains outstanding. |
| UI and responsive behavior | Automated coverage exists | UI smoke checks cover themes, mobile widths, keyboard paths and automated accessibility. Manual screen-reader/assistive-tech review is still required. |
| Durable request/audit persistence | **BLOCKED** | No hosted PostgreSQL instance or `GG_DATABASE_URL`; SQLite resides on Render's ephemeral filesystem. Provision a dedicated managed database, configure secrets, run migrations, and prove persistence across restart/redeploy. |
| Backups and disaster recovery | **BLOCKED** | No production backup policy or isolated restore drill. Configure managed backups/PITR or equivalent, retention, access controls, and prove a restore with recorded evidence. |
| Institutional identity | **BLOCKED** | No institutional OIDC/SSO, verified organizational membership, or MFA policy. Integrate with the intended institution's identity provider and test login, lifecycle, authorization, and revocation. API keys are not verified institutional identity. |
| Participant consent / withdrawal | **BLOCKED for participant data** | No authoritative participant-level consent and withdrawal source. Define an institution-approved consent model, map allowed uses to DUO using GA4GH guidance, and validate legal/ethics requirements before accepting any participant data. |
| Independent audit anchoring | **BLOCKED** | Local hash chain alone is not immutable against an actor able to rewrite the database and recompute hashes. Send signed, append-only events or checkpoints to a separately controlled audit service with trusted timestamps and access separation. |
| Production health/readiness | **BLOCKED** | Readiness must remain fail-closed until controls are configured and verified. Align Render's actual health-check setting with the repo blueprint; prove liveness and readiness behavior against the deployed service. |
| Security/privacy/ethics review | **BLOCKED** | No independent penetration test, privacy impact assessment, legal/ethics approval, or cryptographic review. Complete scoped reviews and remediate findings before sensitive-data use. |
| Monitoring and incident response | **BLOCKED / unverified** | Define actionable alerting, incident ownership, secret rotation, retention/deletion, vulnerability handling, and recovery objectives; test a runbook. |
| Production multi-tenant consistency | **BLOCKED / unverified** | Prove tenant isolation, concurrency behavior, and persistence under the actual production topology before scaling beyond one instance. |

## Required production release gates

Do not mark the service production-ready until all applicable gates have evidence attached to a specific release:

1. **Durable data layer**
   - Provision a dedicated managed PostgreSQL database for GenomeGuard only.
   - Store the connection string and encryption keys in the hosting secret manager; never commit them or expose them in browser-visible configuration.
   - Apply the versioned migration and verify schema/version state.
   - Prove create/read/update behavior, concurrent audit ordering, and request ownership against the deployed service.
   - Prove data survives application restart and redeploy.

2. **Backup and restore**
   - Document RPO/RTO, retention, backup encryption, restore access, and deletion policy.
   - Take a backup and restore it into an isolated database.
   - Run integrity checks and a documented application-level acceptance test against the restored copy.
   - Record evidence and schedule recurring restore drills.

3. **Identity and authorization**
   - Integrate the actual institution's OIDC/SAML identity provider and MFA requirements.
   - Use server-validated claims and explicit role/tenant membership; do not treat an API key as a human identity.
   - Test denial by default, account revocation, session expiry, cross-tenant access, and secret rotation.

4. **Consent and governance**
   - Do not invent participant consents. Integrate only an authoritative consent/withdrawal system approved by the data controller.
   - Map real consent language and permitted purposes to a governed vocabulary such as DUO using GA4GH Machine Readable Consent Guidance.
   - Require institution/legal/ethics approval for each intended dataset and jurisdiction.
   - Keep public-dataset research mode distinct from any future controlled-access cohort.

5. **Independent audit evidence**
   - Use a separately administered append-only destination for signed events/checkpoints.
   - Define key custody, trusted timestamping, verification, retention, access review, and incident procedures.
   - Test tampering, replay, missing sequence, restore, and key rotation.

6. **Live acceptance and independent review**
   - Run read-only health/provenance/UI smoke tests on the exact production commit.
   - In an isolated staging environment, run authenticated API workflows, persistence, restart/redeploy, backup/restore, tenant isolation, rate-limit and error-path tests.
   - Complete independent security testing using OWASP ASVS 5.0.0 as a verification baseline; complete privacy impact, institutional ethics/legal review, and manual screen-reader testing.
   - Do not submit real participant data until approvals and controls are complete.

7. **Operational release**
   - Configure provider health checks and verify readiness cannot return ready when mandatory controls are absent.
   - Define monitoring/alerts, incident contacts, dependency/security updates, data retention/deletion, service limits, and a rollback plan.
   - Publish a versioned release note with exact commit, data source/provenance, test evidence, limitations, and any remaining known issues.

## Hosting constraint

Render's official documentation says free web services have ephemeral filesystems and should not be used for production; free PostgreSQL expires after 30 days and does not include managed backups. Therefore a free service/database cannot be presented as the durable production solution. Select a supported paid database/hosting tier or a different managed provider only after the project owner approves the recurring budget and operational owner. Do not create a fragile free database merely to make readiness green.

## Research references

- Render free-plan limitations: https://render.com/docs/free
- Render PostgreSQL backups and recovery: https://render.com/docs/postgresql-backups
- GA4GH Machine Readable Consent Guidance: https://www.ga4gh.org/product/machine-readable-consent-guidance/
- GA4GH Framework for responsible sharing of genomic and health-related data: https://www.ga4gh.org/framework/
- OWASP Application Security Verification Standard 5.0.0: https://asvs.owasp.org/
- WHO, Guidance for human genome data collection, access, use and sharing (20 November 2024): https://www.who.int/publications/i/item/9789240102149

## Final decision

**Do not certify as complete production software yet.** The audited release is a public-genotype research prototype with tested code paths and explicit limitations. The remaining blockers require real infrastructure, institution-owned identity and consent systems, independent review, and live operational evidence; these cannot honestly be replaced by synthetic data, mocked integrations, or green CI alone.
