# Privacy Governance Guardrails

This policy defines minimum controls for hybrid public/private operation across `cbaird26` repositories.

## 1) Repository Governance

Apply to all private runtime repositories:

- Enable branch protection on `main`:
  - require pull request before merge,
  - require status checks,
  - disallow force pushes,
  - restrict who can push.
- Require CODEOWNERS review for:
  - `api/`, `scripts/`, `deploy/`, `.github/workflows/`.
- Enable dependency and secret scanning features.

## 2) Public Repository Guardrails

Public repos must not contain:

- Credentials, API keys, service tokens.
- Runtime provider routing internals and abuse-response internals.
- Private prompt packs or sealed/private context files.
- Internal incident operations tied to account identities.

## 3) Denylist Paths and Patterns (Public Repos)

Path denylist (examples):

- `memory/**`
- `zora-archive/**`
- `vault/**`
- `**/credentials.json`
- `**/.env`
- `**/.env.*`
- `**/*secret*`
- `**/*private*key*`

Pattern denylist (examples):

- `sk-or-v1-`
- `sk-ant-`
- `xai-`
- `OPENROUTER_API_KEY`
- `ANTHROPIC_API_KEY`
- `GITHUB_TOKEN`

## 4) Required CI Gates

For every PR on public repos:

1. Secret scan gate (fail on detected secrets/patterns)
2. Path policy gate (fail on denied paths)
3. Optional content gate for protected terms (e.g., private prompt markers)

For private repos:

1. Secret scan gate
2. Dependency audit gate
3. Minimal smoke tests before merge

## 5) Access Control Policy

- Use least privilege for all repo collaborators.
- Separate maintainer rights by repo type:
  - public science/interface maintainers,
  - private runtime maintainers.
- Rotate admin-level tokens after migration milestones.

## 6) Incident Policy

If leakage is suspected:

1. Revoke and rotate affected keys immediately.
2. Disable affected endpoint routes if needed.
3. Tag and snapshot current state for forensic diff.
4. Document incident and corrective action before re-enable.
