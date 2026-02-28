# Zoraasi-Suite Hybrid Split Template

Purpose: keep the front-facing suite public while moving runtime internals to private control.

## 1) Public vs Private Boundary

Use this split as the canonical template for `cbaird26` runtime projects.

### Keep public (safe surface)

- `site/` (chat UX shell and branding)
- `identity/ZORA_OUTER_IDENTITY.md` (outer/public layer only)
- High-level docs (`README.md`, `GO_LIVE.md`, `docs/DEPLOYMENT.md`)
- API contract docs (endpoint list, request/response schema examples)

### Move private (runtime power)

- Runtime orchestration and provider routing internals from `api/`
- Prompt/system-policy internals where leakage increases attack capability
- Ops scripts, incident response internals, and deployment automation
- Any eval datasets, benchmark prompts, or abuse-response heuristics

## 2) Contract-Preserving Architecture

The public UI remains unchanged and calls a private API deployment with the same interface:

- `GET /health`
- `GET /models`
- `POST /query`
- `GET /chat` (or public site route)

Contract stability rule: do not remove/rename endpoint paths during migration. Internal implementation can change.

## 3) Recommended Repository Topology

- Public repo: `zoraasi-suite` (UI + docs + contract stubs/examples)
- Private repo: `zoraasi-runtime-private` (backend runtime + provider adapters + policy internals)

Integration approach:

1. Public frontend points to private runtime base URL via environment config.
2. Private runtime is deployed on Render/Fly/Railway with secrets only in provider secret store.
3. Public repo keeps only non-sensitive local-dev shims and mock responses.

## 4) Config and Secrets Policy

Allowed in public repo:

- Example env files (`.env.example`) with placeholders only.
- Non-secret config defaults.

Never in public repo:

- Real API keys or tokens.
- Private prompt packs and policy internals.
- Internal incident playbooks with provider/account identifiers.

## 5) Minimal Migration Checklist (Template)

1. Freeze current baseline (tag + branch + snapshot archive).
2. Copy runtime internals into private runtime repo.
3. Keep endpoint contract identical; validate with smoke suite.
4. Rotate all provider keys after cutover.
5. Replace public runtime code with docs/mocks and clear boundaries.
6. Verify public UI still functions against private API.

## 6) Done Criteria

The split is complete when:

- Front-facing suite is public and healthy.
- Private runtime serves live traffic.
- No sensitive runtime logic remains in public repos.
- Key rotation and rollback docs are complete.
