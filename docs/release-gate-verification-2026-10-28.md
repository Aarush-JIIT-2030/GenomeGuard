# GenomeGuard release-gate verification — 28 October 2026

## Decision

**Release status: research prototype only. Not approved for private, controlled-access, or clinical genomic data.**

This update records direct repository and Supabase observations made on 28 October 2026. It is intentionally not a claim of production completion. A passing CI workflow, successful frontend build, or healthy provider deployment does not prove durable persistence, participant-level consent, or production security.

## Work completed in this pass

- Reviewed the current `main` repository, existing completion audit, deployment configuration, and the field-first UI pull request.
- Inspected the linked Supabase project `common 1` read-only. Its current schema includes both `genomeguard` and `bharatsim`; it is therefore shared infrastructure, not an isolated GenomeGuard production database.
- Checked the deployment status record: `api_migration_complete=false`, `genomic_dataset_loaded=false`, `render_dependency_present=true`, and `release_gate_passed=false`. Its notes say the API, cohort data, and endpoint parity have not been migrated.
- Checked the `genomeguard` schema: 13 tables exist; row-level security is disabled on those tables. All 12 application/data tables inspected were empty; `schema_migrations` had one row. The separate public deployment-status table has RLS enabled.
- Checked Supabase security/performance advisors. The security advisor reported seven tables in the separate `bharatsim` schema with RLS enabled but no policies. This is a shared-project finding and must be handled with the BharatSim owner/workflow, not silently changed as part of GenomeGuard.
- Found an accessibility regression in the UI PR: dark-theme primary buttons rendered white text on a light-green background (contrast ratio 2.14); the donor consent action had the same issue. Patched the theme tokens to use a dark foreground in dark mode and re-triggered CI.

## Release blockers — must be resolved with evidence

### P0 — Isolate the database and establish least privilege

- Provision or designate a **GenomeGuard-only** managed PostgreSQL project/database. Do not treat `common 1` as an isolated production store; it currently contains both GenomeGuard and BharatSim schemas.
- Do not blindly enable RLS on the existing GenomeGuard tables until the intended API connection roles and ownership model are reviewed. The current backend has not been proven to use this database, and blanket policy changes could either break access or create a false sense of security.
- Define the access model for every table: application service role, institutional researcher, steward, and any participant-facing access. Keep privileged service credentials server-side; deny direct public access by default.
- Apply reviewed, versioned migrations to the isolated database and verify the migration history against the repository.
- Prove that unauthorized roles cannot read or mutate donor, genotype, request, decision, epsilon-ledger, or audit data. Add cross-tenant/role regression tests and run Supabase security advisors after policies are in place.

### P0 — Connect the real backend and durable storage

- Configure the hosting secret `GG_DATABASE_URL` only after the isolated database is ready; never commit it or expose it to browser JavaScript.
- Migrate the API's actual persistence path from ephemeral local storage to the managed database, or explicitly document and maintain the local-only mode. Verify endpoint parity rather than assuming that schema creation connects the app.
- Run create/read/update and concurrent-request tests against the deployed service.
- Prove data survives process restart and redeploy. Record sanitized test evidence and the deployed commit.

### P0 — Correct health/readiness and prove live operation

- The prior audit found the Render service's provider-side health-check path empty even though `render.yaml` specifies `/health`. Correct the provider setting and verify it from the provider configuration.
- Keep readiness fail-closed while required database/API/data dependencies are missing. Do not set `release_gate_passed=true` until the real acceptance criteria pass.
- Execute a read-only deployed smoke test for health, readiness, API authorization, request creation, persistence, and restart survival. Record HTTP status and deployment commit. A Vercel frontend build alone is not enough.

### P0 — Governance and privacy boundaries

- Keep the hosted instance restricted to the public 1000 Genomes / IGSR research dataset until an institution-approved data governance process exists.
- Do not invent participant consents or imply that dataset-level release policy equals individual consent or legal authorization.
- Add institutional identity (OIDC/SAML as appropriate), MFA where required, server-validated membership/roles, session revocation, and cross-tenant authorization tests before private cohorts.
- Establish backup retention, encryption, recovery objectives, and a successful isolated restore drill.
- Anchor signed audit checkpoints in a separately administered append-only system; a local hash chain is not independently immutable.
- Obtain independent security, privacy, legal/ethics, and cryptographic review before accepting sensitive participant data.
- Document monitoring, incident ownership, secret rotation, retention/deletion, vulnerability response, and recovery procedures.

## UI / accessibility gate

The field-first theme is a CSS-only enhancement to the existing vanilla-JavaScript app. Avoid introducing React/Magic UI/React Bits solely for decoration: the repository does not currently use a React runtime, and a migration would increase risk without improving the product's core research workflow.

The first CI run caught dark-mode action contrast failures. The fix changes the theme's foreground token to dark text on light green in dark mode while preserving white text on the darker light-theme primary action. Do not merge the UI PR until the new full CI run is green, including the browser/axe checks.

## Honest scope statement

GenomeGuard is a privacy-aware research prototype for evaluating access to public genomic research data. Its risk scores are heuristics, fixed explanation templates are not a live LLM, synthetic records are confined to clearly labelled local test/demo workflows, and the local hash chain is not an independent immutable audit anchor. It is not a clinical decision system, a guarantee of anonymity, or an approved environment for private/controlled-access genomic data.

## Acceptance checklist

- [ ] Dedicated GenomeGuard database and reviewed least-privilege policies
- [ ] Migrations applied and migration history reconciled
- [ ] Real backend connected to durable storage
- [ ] Authorization/tenant-isolation tests pass against the deployed service
- [ ] Persistence survives restart and redeploy
- [ ] Provider health-check configuration corrected and verified
- [ ] Live readiness and end-to-end smoke checks pass for a named deployment commit
- [ ] Backup/restore drill completed and evidence recorded
- [ ] Institutional identity, consent/withdrawal governance, and independent audit anchoring implemented before private data
- [ ] Independent security/privacy/ethics review completed before sensitive-data use
- [ ] Full CI, responsive, keyboard, and accessibility checks pass after UI changes

**No production gate should be marked complete based solely on this document.** Attach deployment-specific evidence for every checked item.
