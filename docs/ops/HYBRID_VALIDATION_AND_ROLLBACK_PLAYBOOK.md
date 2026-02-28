# Hybrid Validation and Rollback Playbook

Use this for each migrated repository/service after hybrid privacy cutover.

## 1) Validation Scope

Validate three layers:

1. Interface continuity (public UI and docs)
2. Runtime continuity (private backend functionality)
3. Security continuity (auth, secret hygiene, policy gates)

## 2) Smoke Test Checklist

### API Surface

- `GET /health` returns healthy status.
- `GET /models` returns expected role map.
- `POST /query` succeeds for:
  - `single`
  - `router`
  - `consensus`

### Response Contract

- Required keys present in response payload:
  - `response`
  - `mode`
  - `role`
  - `model`
  - `model_id`
  - `model_name`

### Front-End Continuity

- Public suite loads and sends prompts successfully.
- Mode switches work and return visible responses.
- Metadata display does not regress.

### Security and Access

- Private runtime rejects unauthorized access paths.
- Rate limiting and abuse controls are active.
- No secrets detected in public repo diff before/after cutover.

## 3) Acceptance Gates

Cutover is accepted only if all are true:

- No critical endpoint failures for 24h.
- No schema/contract regression in core endpoints.
- No auth bypass and no secret leakage findings.
- Rollback procedure tested once and documented.

## 4) Rollback Drill (Per Repo)

1. Identify rollback reference:
   - freeze tag
   - freeze branch
   - deployment baseline
2. Re-point traffic to prior stable deployment.
3. Redeploy freeze commit.
4. Re-run smoke checklist and confirm recovery.
5. Record elapsed recovery time and root cause.

## 5) Reporting Template

For each repo migration, capture:

- Repo name
- Migration date/time (UTC)
- Freeze tag/branch/SHA
- Smoke test results (pass/fail)
- Rollback drill result (pass/fail, recovery time)
- Incidents and corrective actions
