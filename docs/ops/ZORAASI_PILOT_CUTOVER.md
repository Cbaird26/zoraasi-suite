# Zoraasi-Suite Pilot Cutover (No Downtime)

Goal: migrate runtime internals to private infrastructure while preserving public suite continuity.

## Preflight

- Confirm current production health:
  - `GET /health`
  - `GET /models`
  - `POST /query` in `single`, `router`, `consensus`
- Confirm freeze references exist:
  - `docs/ops/FREEZE_BASELINE.md`
  - `docs/ops/ROLLBACK.md`

## Cutover Sequence

1. **Freeze + Snapshot**
   - Create tag/branch from current `main`.
   - Export snapshot archive.
   - Record SHA and deployment baseline.

2. **Deploy private runtime**
   - Stand up private API service with identical endpoint contract.
   - Configure secrets in deployment provider only.
   - Apply auth/rate limiting before exposing traffic.

3. **Shadow verification**
   - Run smoke prompts against private runtime URL.
   - Compare response structure with current public runtime.
   - Confirm latency and error budget are acceptable.

4. **Traffic switch**
   - Point front-facing suite runtime URL to private backend.
   - Keep old runtime as hot standby for rollback window.
   - Perform immediate health and mode checks.

5. **Post-switch hardening**
   - Rotate model-provider keys.
   - Confirm logs and alerts are green.
   - Mark old runtime read-only or decommission after stability window.

## Stability Window

- Recommended: 24-48 hours with scheduled checks:
  - hourly for first 4 hours,
  - every 4 hours until window ends.

## Rollback Trigger Conditions

Rollback immediately if any of the following persists for more than 5 minutes:

- `POST /query` availability drops below 99%.
- Repeated 5xx responses in any mode.
- Auth bypass or security policy failure.
- Front-end chat flow breaks for standard prompts.

## Rollback Path

1. Re-point public suite to previous runtime URL.
2. Redeploy frozen tag from `docs/ops/FREEZE_BASELINE.md`.
3. Re-run smoke tests to confirm recovery.
4. Open incident log with cause and fix actions.
