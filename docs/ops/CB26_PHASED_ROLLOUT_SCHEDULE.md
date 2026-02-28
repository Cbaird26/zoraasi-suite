# cbaird26 Phased Hybrid Rollout Schedule

Primary inventory source: `docs/ops/CB26_REPO_CLASSIFICATION_MATRIX.md`.

## Rollout Principles

- No public endpoint contract breakage.
- Freeze and rollback point before every phase.
- Migrate active runtime repos first, science/public artifacts second, legacy archives last.

## Phase 1 (Week 1): Active Runtime Repos -> Private

Target set (from matrix category `Private Runtime`):

- `zoraasi-suite`
- `unified-agent-platform`
- `local-asi`
- `Dark-Knight`
- `ZoraAPI`
- `toe-studio`
- `mqgt-ops-ci`
- `mqgt-api-schema`
- `mqgt-validation-suite`
- `mqgt-data-ingest`
- `mqgt-dashboard`

Checkpoint per repo:

1. Tag + branch freeze
2. Snapshot export
3. Private runtime deployment
4. Traffic switch
5. 24h stability validation

## Phase 2 (Week 2): Public Science + Interface Repos

Target set:

- All `Public Science` repos remain public.
- All `Public Interface` repos remain public.

Actions:

- Ensure no sensitive runtime internals in these repos.
- Keep reproducibility artifacts, papers, docs, and safe UI assets public.
- Add clear boundary docs that runtime logic is private.

## Phase 3 (Week 3): Archive/Freeze Consolidation

Target set:

- All `Archive/Freeze` repos.

Actions:

- Mark read-only archival posture.
- Optionally convert selected repos to private archive if risk is high.
- Add archive notice and canonical pointers to active public science/runtime repos.

## Freeze/Rollback Checklist (Every Phase)

Before phase:

- Create annotated tag and freeze branch.
- Capture snapshot archive and deployment baseline.

After phase:

- Run smoke tests.
- Validate security controls.
- Record pass/fail and keep rollback command ready.

## Reporting Artifacts

- Per-phase migration report
- Incident/rollback records (if triggered)
- Updated repo classification matrix with completed status
