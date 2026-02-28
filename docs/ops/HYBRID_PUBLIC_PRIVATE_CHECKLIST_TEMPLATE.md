# Hybrid Public/Private Migration Checklist Template

Use this checklist per repository during hybrid migration.

## Repository

- Name:
- URL:
- Owner:
- Target classification: `Public Science` / `Public Interface` / `Private Runtime` / `Archive/Freeze`

## A) Freeze and Baseline

- [ ] Freeze tag created
- [ ] Freeze branch created
- [ ] Snapshot archive created
- [ ] Deployment baseline captured
- [ ] Rollback command verified

## B) Boundary Enforcement

- [ ] Public-safe folders identified and preserved
- [ ] Private runtime folders identified and moved/isolated
- [ ] API/interface contract documented
- [ ] No sensitive internals remain in public repo

## C) Secrets and Access

- [ ] Secrets removed from code/config
- [ ] Secrets stored only in deployment secret manager
- [ ] Keys rotated after cutover
- [ ] Branch protection enabled
- [ ] CODEOWNERS applied

## D) Validation

- [ ] Health endpoint check passes
- [ ] Core query flow passes
- [ ] Front-end interaction passes
- [ ] Auth/rate-limit checks pass
- [ ] Regression issues triaged or resolved

## E) Post-Cutover

- [ ] Stability window completed
- [ ] Incident log updated (if needed)
- [ ] Migration report finalized
- [ ] Repo matrix updated with final status
