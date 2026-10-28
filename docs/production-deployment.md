# Hosted deployment record

Last audited: 28 October 2026.

## Current public research instance

- Public URL: https://genomeguard.onrender.com
- Hosting: Render web service, free plan, Singapore region
- Service ID: `srv-dbev1ka9lscs738813t0`
- Current Render deployment: `dep-dbg42osipgvc73eesutg`, status `live`
- Deployed source commit: `a100921c98dbb194e365f76d32f9340700b2c196` (merge of PR #43)
- Runtime: Docker, Python 3.12 image, Uvicorn
- Dataset: public 1000 Genomes / IGSR chromosome 22 genotype calls, 600 samples × 3,000 variants
- Policy provenance: versioned mapping of published dataset-level public-release terms; not participant-specific consent and not independent legal review
- Hosted demo mode and destructive audit-tampering mode: disabled
- Explanations: built-in templates; no live LLM configured

Render reports the current main commit as live. This confirms deployment status, not end-to-end runtime health. The available web verifier could not fetch the public URL or health endpoints, and the connected Vercel account could not independently inspect the current deployment content. Do not claim a live UI/API acceptance pass until the documented checks pass from a network-enabled runner.

## Health and readiness configuration

The repository's `render.yaml` declares `healthCheckPath: /health`, but Render's live service configuration reported an empty `healthCheckPath` during the 26 October audit. The setting could not be corrected with the available provider actions. This configuration drift remains open.

Required verification:
- Configure Render's health check path as `/health` in the service dashboard.
- Confirm `GET /health` reports liveness and source provenance only.
- Confirm `GET /health/ready` remains not-ready (HTTP 503) while production controls are absent.
- Run read-only research-mode, API, route/UI, authorization, and accessibility smoke tests against the exact deployed commit.

Do not treat a liveness response, deployment status, or green CI as production readiness.

## PostgreSQL and Supabase status

The opt-in PostgreSQL adapter and migration/recovery tooling were merged through [PR #33](https://github.com/kaustubhdua/GenomeGuard/pull/33). The Render service still has no verified GenomeGuard PostgreSQL connection: `GG_DATABASE_URL` is not configured. The deployed service therefore has no verified durable request/audit persistence. SQLite is stored at `/data/genomeguard.sqlite3` on an ephemeral filesystem. The adapter and its tests do not provision a database or prove production durability by themselves.

The intended Supabase project is `common 1`, ID `hkyieaovolkethovyenb`, with GenomeGuard isolated in the `genomeguard` schema. This Supabase project is shared with a separate `bharatsim` schema and has BharatSim migration records too; keep project-specific schemas, grants, migrations, and data isolated and never run a GenomeGuard migration against another schema. The live database contains 13 GenomeGuard application tables, but the cohort, donor, genotype, request, decision, and audit tables have zero rows; no production cohort was fabricated or imported. The backend is not connected to this database.

**Live security finding and follow-up:** the initial 27 October query found RLS disabled on all 13 GenomeGuard tables. On 28 October, the reviewed private-schema migration was applied and direct SQL verified RLS enabled on all 13 tables and no schema `USAGE` privilege for `anon`, `authenticated`, or `service_role`. The latest Supabase security advisor now reports `rls_enabled_no_policy` informational findings for GenomeGuard and BharatSim. GenomeGuard's no-policy state is intentional for this private schema: browser roles have no schema `USAGE` privilege and no Data API exposure is intended. This is defense in depth, not a complete authorization design. A dedicated database and reviewed server-side role/access model remain required. The reviewed defense-in-depth migration `supabase/migrations/20261027010000_private_schema_rls.sql` was applied to the live database on 28 October 2026 as migration `20261028180028` (`genomeguard_private_schema_rls`). Direct SQL verification confirmed RLS enabled on all 13 `genomeguard` tables and no `USAGE` privilege on the schema for `anon`, `authenticated`, or `service_role`. The migration is scoped to `genomeguard` and does not change the separate `bharatsim` schema. It intentionally creates no client-facing policies; the intended access model is a separately reviewed trusted server-side PostgreSQL connection. Do not expose private genomic tables through the Supabase Data API. This is defense in depth only: the Render backend is still not connected to this database, and production persistence is not verified.

Required before production:
1. Configure the actual dedicated PostgreSQL connection string as Render secret `GG_DATABASE_URL` using the provider dashboards. Never paste it into chat, commit it, or expose it to browser code. Prefer a dedicated GenomeGuard-only database rather than a shared application project for production.
2. Verify migrations, least-privilege server connection, request ownership, concurrent writes, audit ordering, and failure behavior against the deployed service.
3. Prove records survive restart and redeploy.
4. Configure backup retention and recovery objectives; restore into an isolated database and run integrity/application acceptance checks.
5. Correct and verify Render's provider-side health-check path (`/health`) and run a live smoke test against the exact deployed commit.

Do not use a temporary free database as a production fix. Render's free PostgreSQL databases expire after 30 days and do not provide managed backups. See [Render free-plan limitations](https://render.com/docs/free) and [Postgres recovery and backups](https://render.com/docs/postgresql-backups). Supabase's [production checklist](https://supabase.com/docs/guides/deployment/going-into-prod) recommends RLS with appropriate policies, reviewing security findings, load testing, and a verified backup strategy.

## Vercel frontend status

- Project: `genome-guard` — [Vercel project](https://vercel.com/jyc-website/genome-guard)
- Project ID: `prj_Q2uhnuLdzXTo4JoZUXqzhW6YuICT`
- Settings updated: root directory `frontend`, static/Other framework, output directory `.`, preview SSO protection.
- GitHub-triggered preview for PR #43 was reported `READY`.
- A production deployment and public route-by-route acceptance test are **not independently verified**. Direct production deployment creation was denied by the connected Vercel API, and current deployment-list access is denied.

The frontend rewrites API requests to the Render service. Vercel is not a replacement for durable backend storage. Promote a production deployment only after the UI and API acceptance tests pass and the private-data security controls are in place.

## Explicit production blockers

1. **Durable persistence and recovery:** no configured/verified database connection; no production backup/restore drill.
2. **Database security:** RLS is disabled on all 13 live application tables; the merged migration remains unapplied.
3. **Institutional identity:** no institutional OIDC/SSO, verified organization membership, or institution-controlled MFA lifecycle. Provisioned API keys are not verified human identity.
4. **Participant consent and withdrawal:** hosted public-data policy is dataset-level only. There is no authoritative participant-specific consent/withdrawal source.
5. **External audit anchoring:** the local hash chain is tamper-evident but not immutable against an actor able to rewrite the database and recompute hashes. No independently controlled external anchor or trusted timestamp is configured.
6. **Independent assurance:** no independent penetration test, privacy impact assessment, institutional ethics/legal review, clinical validation, or cryptographic review has been completed.
7. **Manual accessibility:** automated axe/browser checks do not replace manual screen-reader and assistive-technology review.
8. **Operational controls:** monitoring/alerting, incident response, retention/deletion, recurring recovery drills, and multi-instance consistency are not verified.
9. **Live acceptance:** run read-only research-mode, route/UI, authorization, and accessibility smoke tests on the exact current deployment; the available verifier could not fetch the live endpoints.

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
