# Open Repo Policy — What Is Private Stays Private

**Policy:** Push and open all appropriate or forward-progressing repos as public. What is private stays private.

---

## Repos Under cbaird26

Repos are **open by default** for Public Science, Public Interface, and forward-progressing work. Private Runtime repos (orchestration, sensitive ops) may remain private per classification.

---

## What Stays Private (Never Committed)

| Category | Protection |
|----------|------------|
| **Inner layer** — vault, cabin, sealed corpus, continuity pack | Lives in mqgt_scf_reissue `memory/`; not in public repos. See [PRIVACY_LAYERS.md](PRIVACY_LAYERS.md), [identity/INNER_REFERENCE.md](../identity/INNER_REFERENCE.md) |
| **Credentials** — API keys, .env, *.credentials.json | `.gitignore`; see [ENV_AND_CREDENTIALS.md](ENV_AND_CREDENTIALS.md) |
| **Personal data** — conversations, zoraasi_export, merged corpus | `**/vault/`, `**/zoraasi_export/`, `**/conversations.json`, `**/merged_corpus.jsonl` in `.gitignore` |

---

## References

- [PRIVACY_LAYERS.md](PRIVACY_LAYERS.md) — Outer, Middle, Inner layer definitions
- [ENV_AND_CREDENTIALS.md](ENV_AND_CREDENTIALS.md) — Env vars and secret handling
- [identity/INNER_REFERENCE.md](../identity/INNER_REFERENCE.md) — Where inner identity lives (outside this repo)
- [docs/ops/CB26_REPO_CLASSIFICATION_MATRIX.md](ops/CB26_REPO_CLASSIFICATION_MATRIX.md) — Repo visibility targets

---

C.M. Baird, ZoraASI. March 2026.
