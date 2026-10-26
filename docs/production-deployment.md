# Hosted deployment record

Last audited: 26 October 2026.

## Current public research instance

- Public URL: https://genomeguard.onrender.com
- Hosting: Render web service, free plan, Singapore region
- Service ID: `srv-dbev1ka9lscs738813t0`
- Latest deployment checked: `dep-dbfiug0u01pc73beus5g`, status `live`
- Deployed source commit: `a9aed73c4c0ffad632b892eb98eee294a4e9d751` (PR #36 merge)
- Runtime: Docker, Python 3.12 image, Uvicorn
- Dataset: public 1000 Genomes / IGSR chromosome 22 genotype calls, 600 samples × 3,000 variants
- Policy provenance: versioned mapping of published dataset-level public-release terms; not participant-specific consent and not independent legal review
- Demo mode and destructive audit-tampering mode: disabled
- Explanations: built-in templates; no live LLM configured

Render reports the deployment as live and tied to the audited main commit. The available web verification client could not fetch the public URL or health endpoints during this audit, so a successful current end-to-end runtime smoke is **not established by this document**. Re-run the documented live checks from a network-enabled runner before relying on the runtime.

## Health and readiness configuration

The repository's `render.yaml` declares `healthCheckPath: /health`. However, Render's current service configuration reported an empty `healthCheckPath` on 26 October 2026. This is configuration drift. Correct the actual Render service setting through the provider dashboard/API, then verify:
- `GET /health` reflects liveness and source provenance only;
- `GET /health/ready` remains not-ready (HTTP 503) while required production controls are absent;
- deployment and post-deploy acceptance tests run against the exact deployed commit.

Do not treat a liveness response, deployment status, or green CI as production readiness.

## PostgreSQL implementation status

The opt-in PostgreSQL adapter and migration/recovery tooling were merged through [PR #33](https://github.com/kaustubhdua/GenomeGuard/pull/33), merge commit `eab308f27113e207b995e5c310f339abbd91d3a3`. Subsequent UI, authorization, and documentation work is present on main.

The Render account currently has **no GenomeGuard PostgreSQL instance** and `GG_DATABASE_URL` is not configured. The deployed service therefore has no verified durable request/audit persistence. SQLite is stored at `/data/genomeguard.sqlite3` on an ephemeral filesystem. The adapter includes versioned migrations, an offline SQLite migration tool, PostgreSQL audit sequence locking, transactional mutation handling, integration tests, and backup/restore tooling; none of these provisions a database or proves production durability by itself.

Required before production:
1. Provision a dedicated managed PostgreSQL database for GenomeGuard only, with an explicitly approved recurring budget and owner.
2. Set `GG_DATABASE_URL` and encryption/master secrets using the provider's secret manager; never commit them or expose them to browser code.
3. Apply and verify migrations, then test request ownership, concurrent writes, and audit ordering against the deployed service.
4. Prove records survive application restart and redeploy.
5. Configure backup retention and recovery objectives; restore a backup into an isolated database and run integrity and application acceptance checks.

Do not use a temporary free database as a production fix. Render's free PostgreSQL databases expire after 30 days and do not provide managed backups. See [Render free-plan limitations](https://render.com/docs/free) and [Postgres recovery and backups](https://render.com/docs/postgresql-backups).

## Explicit production blockers

1. **Durable persistence and recovery:** No managed database configured; no production backup/restore drill.
2. **Institutional identity:** No institutional OIDC/SSO, verified organization membership, or institution-controlled MFA lifecycle. Provisioned API keys are not verified human identity.
3. **Participant consent and withdrawal:** Hosted public-data policy is dataset-level only. There is no authoritative participant-specific consent/withdrawal source.
4. **External audit anchoring:** The local hash chain is tamper-evident but not immutable against an actor able to rewrite the database and recompute hashes. No independently controlled external anchor or trusted timestamp is configured.
5. **Independent assurance:** No independent penetration test, privacy impact assessment, institutional ethics/legal review, clinical validation, or cryptographic review has been completed.
6. **Manual accessibility:** Automated axe/browser checks do not replace manual screen-reader and assistive-technology review.
7. **Operational controls:** Monitoring/alerting, incident response, retention/deletion, recurring recovery drills, and multi-instance consistency are not verified.
8. **Live acceptance:** Re-run read-only research-mode, route/UI, authorization, and accessibility smoke tests on the exact current deployment; the current audit could not fetch the live endpoints through its web verifier.

## Data and policy boundary

The deployed genotype calls come from the public 1000 Genomes / IGSR release. Source and policy file hashes are recorded during cohort build. The versioned policy maps published dataset-level terms to a DUO-inspired rule set; it is not participant-specific consent, legal advice, or independent approval for any specific use.

Local demo and test workflows intentionally use synthetic fixtures. Hosted research mode disables demo/synthetic participant workflows. Keep those paths explicitly labelled and never describe synthetic fixtures as real people or consent.

The privacy-risk output is heuristic, not an independently validated guarantee. The privacy-budget ledger is not a formally audited differential-privacy implementation. The Beacon-style endpoint is not full Beacon certification. FHIR Consent fixtures are synthetic validation artifacts, not real consent records. No live LLM is configured. The local audit chain has no external immutable anchor.

## Reproduce checks

From a local clone with Python 3.11+, dependencies, and Playwright Chromium installed:

```bash
python scripts/live_research_mode_smoke.py --base https://genomeguard.onrender.com
python scripts/live_ui_smoke.py --base https://genomeguard.onrender.com
npm install --prefix /tmp/gg-axe --no-save --package-lock=false axe-core@4.14.0
AXE_CORE_PATH=/tmp/gg-axe/node_modules/axe-core/axe.min.js python scripts/live_accessibility_smoke.py --base https://genomeguard.onrender.com
```

Research-mode smoke checks should be read-only. Run write-enabled acceptance only against an isolated staging service with synthetic fixtures. Never run destructive persistence probes against production data.

## Release decision

The service is a working **public-genotype research prototype**, not a production genomic-data-governance service. Do not submit private participant data, identifiable genomic data, controlled-access cohorts, or clinical records. Keep readiness fail-closed until the relevant controls exist and their live behavior is verified.
