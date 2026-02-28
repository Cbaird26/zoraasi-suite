# cbaird26 Wave Execution Packs

This file standardizes controls for each migration wave in the all-105 rollout.

## Wave 1: Private Runtime Controls

Use with: `CB26_WAVE1_RUNTIME_TRACKER.md`

Per-repo required controls:

1. Freeze references created (tag + branch + snapshot checksum).
2. Runtime private boundary confirmed (no sensitive internals in public surface).
3. Rollback proof documented (command and successful smoke verification).
4. Guardrails active (`main` protection + secret/path policy checks).

Evidence fields per repo:

- Freeze tag:
- Freeze branch:
- Snapshot checksum:
- Rollback command:
- Smoke status:

## Wave 2: Public Science + Interface Hardening

Use with: `CB26_WAVE2_PUBLIC_TRACKER.md`

Per-repo required controls:

1. Public scope statement present (science/interface only).
2. Runtime internals/prompt internals absent.
3. Secrets denylist checks pass.
4. Front-door links and docs verified.

Evidence fields per repo:

- Scope statement file:
- Secret scan result:
- Boundary check result:
- UX/link check result:

## Wave 3: Archive/Freeze Posture

Use with: `CB26_WAVE3_ARCHIVE_TRACKER.md`

Per-repo required controls:

1. Archive/read-only posture declared.
2. Canonical pointer to active repos/docs present.
3. Historical tags/snapshots retained.
4. Optional private archive conversion decision recorded.

Evidence fields per repo:

- Archive notice:
- Canonical pointer:
- Snapshot/tag reference:
- Conversion decision:

## Exit Rule

A wave is marked complete only when all repos in its tracker have evidence fields populated and status moved from `planned` to `completed`.
