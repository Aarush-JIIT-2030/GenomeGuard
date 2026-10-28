# GenomeGuard production-readiness audit — 28 October 2026

## Decision

**Current release: public-genotype research prototype. Not production-ready for private, controlled-access, or clinical genomic data.**

This audit distinguishes source/CI checks from live provider state. A merged PR, green CI, or live deployment does not by itself establish end-to-end production readiness.

## What is verified

- Repository: https://github.com/kaustubhdua/GenomeGuard
- Main merge commit: `a100921c98dbb194e365f76d32f9340700b2c196` (PR #43).
- Render service: https://genomeguard.onrender.com
- Render reports deployment `dep-dbg42osipgvc73eesutg` as live for the main merge commit.
- GitHub Actions `ci`, `Deployment configuration checks`, and `security-verification` all passed on PR head `dee30be480f1fdb62d78044ea640ce76bfb4d305`. These include backend tests/lint, PostgreSQL migration integration tests, evaluation checks, browser/responsive/accessibility checks, dependency audit, CodeQL and secret scanning. **Those workflow runs are associated with the PR head; they were not separately reported against the merge commit.**
- Deployment-configuration CI applies migrations to a clean PostgreSQL instance and asserts schema isolation, fail-closed deployment status, and RLS enabled on all 13 private tables in that clean test database.
- The deployed research dataset is recorded as public 1000 Genomes / IGSR chromosome 22 genotype calls (600 samples × 3,000 variants). These are real public genotype data, not private or participant-consent-verified data.
- The documentation identifies synthetic fixtures as local demo/test artifacts. No synthetic cohort or participant records have been inserted into the live GenomeGuard Supabase schema.

## Live checks that remain unverified

- Render service configuration currently reports an **empty health-check path**, although `render.yaml` declares `/health`. Provider-side configuration drift remains open.
- The available web verification tools could not fetch the public app or health endpoint, and a Firecrawl live scrape could not run because the connected account has no credits. Route-level live acceptance therefore remains unproven; this is not evidence that the site is down.
- Vercel's linked preview was reported READY by the GitHub integration, but its page could not be independently fetched. A production Vercel deployment and public route-by-route acceptance test are not verified; deployment-list/production actions returned access errors.
- A READY build is evidence of build completion, not proof that UI assets, API proxy routes, authentication, or data operations work in production.

## Supabase project `common 1`

- Project ID: `hkyieaovolkethovyenb`; application tables are isolated in schema `genomeguard`.
- Direct live SQL query confirms **0 of 13 application tables have RLS enabled**.
- Direct live row counts: `cohort_metadata`, `donors`, `genotypes`, `variants`, `requests`, `decisions`, `audit_log`, `donor_access`, `alerts`, `requesters`, `relationships`, and `epsilon_ledger` each contain **0 rows**. `schema_migrations` contains one row.
- The private-schema RLS migration `supabase/migrations/20261027010000_private_schema_rls.sql` is merged and passed clean-PostgreSQL CI, but **has not been applied to the live database**.
- The current Supabase security advisor's seven RLS-without-policy notices concern the separate `bharatsim` schema, not GenomeGuard. Do not change that other application's policies as part of GenomeGuard remediation.
- Earlier direct privilege checks confirmed `anon` and `authenticated` lack schema USAGE and direct table access to GenomeGuard's private schema. This reduces immediate Data API exposure but does not replace enabling and verifying RLS.
- No verified Render secret `GG_DATABASE_URL` is configured; the deployed backend is not connected to Supabase. The existing SQLite path is on ephemeral storage, so durable request/audit persistence is not established.

## Blockers before a production claim

1. **Database security:** review the private-schema RLS migration and intended server-side access role; apply it through the controlled migration process; re-check RLS and role grants live. The migration intentionally creates no browser-facing policies.
2. **Durable persistence:** copy/reset the actual Supabase PostgreSQL connection string in the Supabase dashboard and configure it as Render secret `GG_DATABASE_URL`. Never paste it into chat, GitHub, Vercel, or browser code.
3. **Health and live acceptance:** set Render's actual health-check path to `/health`; run read-only research-mode and UI/API smoke tests against the exact deployed commit and inspect results. Keep readiness fail-closed.
4. **Persistence proof:** in an isolated staging environment and using non-sensitive test identities, verify request/decision/audit writes, concurrency/order, read-back, and persistence after restart/redeploy.
5. **Backup and restore:** select a supported backup/retention plan, define recovery point/time objectives, restore into an isolated database, and run integrity/application checks.
6. **Identity and consent:** integrate institutional OIDC/SSO and verified organization membership. API keys are not human identity. Do not invent participant consent; private participant data require an authoritative consent/withdrawal source and institutional/legal/ethics review.
7. **Audit integrity:** add independently administered append-only anchoring or signed checkpoints with trusted timestamps and tested key custody. A local hash chain alone is not immutable against a database administrator.
8. **Independent assurance:** complete scoped penetration testing, privacy impact and legal/ethics review, cryptographic review, and manual assistive-technology testing.
9. **Operations:** configure monitoring/alerting, incident ownership, secret rotation, retention/deletion controls, recovery drills, concurrency and multi-instance consistency.
10. **Release:** verify the actual production Vercel deployment, public route/API proxy behavior, security headers, and all core flows; publish evidence tied to the exact release commit.

## Safe release boundary

Until the above controls are proven, use GenomeGuard only for the public-genotype research prototype. Do not upload private participant data, identifiable genomic data, controlled-access cohorts, or clinical records.

Risk scores are heuristic and not independently validated privacy guarantees. The privacy-budget ledger is not a formally audited differential-privacy implementation. Dataset-level public-release policy mapping is not participant-specific consent or legal authorization. FHIR fixtures are synthetic validation artifacts; selected Beacon-style checks are not full conformance certification. No live LLM is configured. These boundaries must remain visible in the UI and exported results.

## Reproduce the existing checks

From a local clone with Python 3.11+, dependencies, and Playwright Chromium installed:

```bash
make test
make lint
make eval-smoke
make demo
python scripts/live_research_mode_smoke.py --base https://genomeguard.onrender.com
python scripts/live_ui_smoke.py --base https://genomeguard.onrender.com
```

Run live checks from a network-enabled environment. Use only read-only checks against production; write-enabled persistence tests belong in an isolated staging environment.

## Official guidance

- [Supabase production checklist](https://supabase.com/docs/guides/deployment/going-into-prod)
- [Supabase Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security)
- [1000 Genomes / IGSR data portal](https://www.internationalgenome.org/data/)
- [Render free-plan limitations](https://render.com/docs/free)
- [Render PostgreSQL backups and recovery](https://render.com/docs/postgresql-backups)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
