# cbaird26 Guardrail Execution

This runbook applies account-wide governance controls referenced in `PRIVACY_GOVERNANCE_GUARDRAILS.md`.

## Script

- `scripts/ops/apply_guardrails_all_repos.sh`

## What it enforces

- Branch protection on `main` for each repo.
- Required status checks (`secret-scan`, `path-policy`) on protected branches.
- Secret scanning and push protection enablement.
- Public-repo reminder for denylist CI policy enforcement.

## Usage

Dry-run first:

```bash
./scripts/ops/apply_guardrails_all_repos.sh
```

Apply to account:

```bash
./scripts/ops/apply_guardrails_all_repos.sh --apply
```

## Notes

- Requires `gh` authentication with permissions to edit repository settings.
- Some repos may need manual follow-up for workflow files that publish `secret-scan` and `path-policy` checks.
- Use wave trackers to confirm guardrails are effective before changing repository visibility.
