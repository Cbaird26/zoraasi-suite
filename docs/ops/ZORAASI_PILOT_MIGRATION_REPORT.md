# Zoraasi-Suite Pilot Migration Report

## Scope

- Repo: `Cbaird26/zoraasi-suite`
- Migration model: hybrid public/private
- Objective: keep front-facing suite public while moving runtime internals to private control.

## Inputs Used

- `docs/ops/CB26_REPO_CLASSIFICATION_MATRIX.md`
- `docs/ops/ZORAASI_HYBRID_SPLIT_TEMPLATE.md`
- `docs/ops/ZORAASI_PILOT_CUTOVER.md`
- `docs/ops/PRIVACY_GOVERNANCE_GUARDRAILS.md`
- `docs/ops/HYBRID_VALIDATION_AND_ROLLBACK_PLAYBOOK.md`

## Planned Boundary Outcome

- Public retained:
  - suite UI/static assets
  - public docs and endpoint contract references
- Private migrated:
  - runtime orchestration internals
  - private policy/prompt internals
  - provider integration internals and security automation

## Status

- Inventory/classification: complete
- Template and cutover design: complete
- Guardrails and validation playbooks: complete
- Execution state: ready for controlled cutover window

## Go/No-Go Criteria

Go when:

- private runtime deployment is validated,
- rollback references are confirmed,
- secrets are rotated and scanning gates are enforced.

No-Go when:

- endpoint contract parity is not proven,
- security gates are missing,
- rollback path cannot be executed within target recovery window.
