# Repo State, Balance, and Isolation — Ops Reference

**Master map for Public vs Private, cross-contamination guardrails, parallel storage, and isolation boundaries.**

**Full document:** TOE_Corpus_2026/REPO_STATE_AND_BALANCE_2026.md (canonical spine)

---

## 1. Public vs Private (Summary)

| Category | Public | Private | Guard |
|----------|--------|---------|-------|
| **Repos** | zoraasi-suite, toe-2026-updates, mqgt-scf-stripped-core, baird-telehealth-site, cbaird26 profile | unified-agent-platform, local-asi, Dark-Knight | GitHub visibility; PR protection |
| **Content** | Outer identity, papers, public_corpus_bundle, ToE LaTeX | Inner (vault, cabin, sealed corpus), credentials, zoraasi_export | .gitignore; [PRIVACY_LAYERS](PRIVACY_LAYERS.md); [INNER_REFERENCE](../identity/INNER_REFERENCE.md) |
| **Scope** | zoraasi, ToE physics, telehealth | Gmail (never a project), personal inbox, sealed materials | [SCOPE_CLARIFICATION](SCOPE_CLARIFICATION.md) |

---

## 2. Cross-Contamination Mitigations

| Risk | Mitigation |
|------|------------|
| Gmail conflated with corpus | [SCOPE_CLARIFICATION](SCOPE_CLARIFICATION.md); no Gmail in ENV_AND_CREDENTIALS |
| Outer vs Inner bleed | Inner in mqgt_scf_reissue `memory/`; never in zoraasi-suite |
| Cloud sync overwrites | Local primary; cloud = backup; exclude vault, .env |

---

## 3. Pre-Push Checklist

1. `git status` — no vault/, zoraasi_export/, .env, credentials
2. `git diff --staged` — no private paths
3. SCOPE_CLARIFICATION present — no Gmail as project
4. Branch protection — PR required for main

---

## 4. References

- [PRIVACY_LAYERS](PRIVACY_LAYERS.md) — Outer, Middle, Inner
- [OPEN_REPO_POLICY](OPEN_REPO_POLICY.md) — What stays private
- [SCOPE_CLARIFICATION](SCOPE_CLARIFICATION.md) — No Gmail as project
- [ops/PRIVACY_GOVERNANCE_GUARDRAILS](ops/PRIVACY_GOVERNANCE_GUARDRAILS.md) — Denylist, CI gates

---

C.M. Baird, ZoraASI. March 2026.
