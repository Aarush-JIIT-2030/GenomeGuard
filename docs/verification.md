# Verification evidence

Read every result with its exact commit and workflow run. A passing workflow proves only the checks it ran; it does not establish production genomic-data governance readiness.

Last audit: 26 October 2026.

## Current deployed research instance

- Public URL: https://genomeguard.onrender.com
- Render service: `srv-dbev1ka9lscs738813t0`
- Deployed application commit: `a9aed73c4c0ffad632b892eb98eee294a4e9d751`
- Render deployment: `dep-dbfiug0u01pc73beus5g`, reported `live` on 26 October 2026
- Mode: non-demo research mode, built from public 1000 Genomes / IGSR chromosome 22 genotype calls (600 samples × 3,000 variants)
- Source and policy provenance: hashed public source and versioned dataset-level public-release policy mapping; not participant-specific consent
- Current production caveat: no GenomeGuard PostgreSQL instance and no `GG_DATABASE_URL`; Render service is on the free plan with an ephemeral filesystem.

The Render provider reports the deployed commit as live. The web verification client used for this audit could not fetch the public site or health endpoints, so current end-to-end live runtime behavior is **not independently verified in this audit**. Repeat the live scripts from a network-enabled runner against the exact deployed commit before relying on runtime claims.

## Repository CI and automated tests

The GitHub Actions CI workflow includes:
- Python lint and backend test suite;
- PostgreSQL integration tests against an ephemeral PostgreSQL 16 service in CI;
- evaluation smoke tests and full evaluation;
- local demo checks;
- JavaScript syntax checks and Python compile checks;
- Playwright browser smoke checks across all UI routes;
- light/dark theme and narrow viewport checks;
- axe-core automated accessibility checks, keyboard paths, mobile navigation, reduced-motion behavior, and guided tour checks;
- screenshot artifacts for visual review.

The CI job completed successfully for PR #34's tested commit `c9c7eac6ea1e019f66f6142ca5896878b785c467` in run [#40263212372](https://github.com/kaustubhdua/GenomeGuard/actions/runs/40263212372). PR #36 added route-driven authorization matrix tests and mobile drawer keyboard access; its PR description records test, lint, and browser smoke success. The merge commit is `a9aed73c4c0ffad632b892eb98eee294a4e9d751`.

These checks are valuable regression evidence but do not prove the live service has durable storage, institutional identity, external audit anchoring, or an approved consent authority. PostgreSQL integration in CI uses a temporary test database; it does not provision production infrastructure.

## Authorization and API boundary

PR #36 added an authorization matrix driven by the route catalog. Tests exercise admin, requester, and donor route refusal behavior for missing, invalid, or wrong-owner credentials, plus cross-requester action boundaries. This is regression coverage, not an independent penetration test or proof of institutional identity. The hosted service uses provisioned API keys, not institutional OIDC/SSO or verified organization identity.

## Data and policy provenance

The hosted cohort uses real public 1000 Genomes / IGSR genotype calls. Its policy is a documented dataset-level mapping of published public-release terms. It does **not** fabricate participant-specific consent records. It does not establish permission for private or controlled-access cohorts or legal approval for a specific downstream use.

Local demo and test paths use synthetic fixtures intentionally. Synthetic FHIR R4 Consent resources and synthetic evaluation cohorts are validation artifacts, not real consent or real participant data. Hosted mode disables synthetic demo workflows.

## Persistence, recovery, and readiness

The Render service runs on the free plan and has no configured persistent disk. SQLite is stored at `/data/genomeguard.sqlite3` on an ephemeral filesystem. Request and audit history must not be assumed to survive a restart, redeploy, spin-down, or instance replacement.

The PostgreSQL adapter foundation is merged, but the Render account has no GenomeGuard Postgres instance and `GG_DATABASE_URL` is not configured. Durable persistence is therefore not established. No production backup/restore drill has passed.

The `/health/ready` endpoint is intended to remain HTTP 503 / `ready: false` while mandatory production controls are absent. Render's actual service configuration reported an empty health-check path even though `render.yaml` declares `/health`; resolve this provider/configuration mismatch and verify behavior on the deployed service.

## Remaining production assurance

- Dedicated durable database and verified migrations/ownership/concurrency on the live service.
- Backup retention, isolated restore drill, and tested RPO/RTO.
- Institutional OIDC/SSO, verified organization membership, MFA, and revocation lifecycle.
- An authoritative participant consent/withdrawal source before any participant-level governance claim.
- Independently controlled append-only audit anchor and trusted timestamps.
- Independent security penetration test, privacy impact assessment, legal/ethics review, and cryptographic review.
- Manual screen-reader/assistive-technology testing.
- Operational monitoring, incident response, retention/deletion, secret rotation, and recurring recovery drills.
- Live end-to-end acceptance against the current deployment.

See [the completion audit](completion-audit-2026-10-26.md), [hosted deployment record](production-deployment.md), [threat model](threat-model.md), [real-data provenance](real-data.md), and [real cohort consent requirements](real-cohort-consent.md).

## Final verification statement

Current evidence supports describing GenomeGuard as a hosted **public-genotype research prototype** with automated regression coverage. It does not support describing the service as production-ready for private participant data, controlled-access genomic data, or clinical decisions. Keep readiness fail-closed until the controls above are implemented and verified.
