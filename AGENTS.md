# AGENTS.md

## Cursor Cloud specific instructions

### Overview

This is a **configuration and identity repository** (no application code). It contains Zora's outer (public) identity definition, an Ollama modelfile, a deployment config, and a launcher script. The actual backend ("Zora Brain") lives in the external `mqgt_scf_reissue` repository.

### Key services

| Service | How to run | Notes |
|---------|-----------|-------|
| **Ollama** (local LLM) | `ollama serve` (background), then `ollama create zora-outer -f deploy/modelfile-outer.modelfile` | The repo's modelfile uses `gpt-oss:20b` as base. If unavailable, substitute a smaller model (e.g. `qwen2:0.5b`) in a temp modelfile for testing. |
| **Zora Brain API** | `./scripts/run_outer.sh` | Requires sibling `mqgt_scf_reissue` repo or `ZORA_MQGT_REPO` env var. Not runnable from this repo alone. |

### Validation commands

- **Shell script lint:** `shellcheck scripts/run_outer.sh` — SC1091 (info about `.venv/bin/activate` not found) is expected; the venv lives in the external repo.
- **YAML lint:** `yamllint deploy/config.yaml` — line-length and missing `---` warnings are cosmetic; the YAML parses correctly.
- **Ollama model test:** `curl -s http://localhost:11434/api/generate -d '{"model":"zora-outer","prompt":"What is MQGT-SCF?","stream":false,"options":{"num_predict":100}}'`

### Gotchas

- The base model `gpt-oss:20b` referenced in `deploy/modelfile-outer.modelfile` is not publicly available on Ollama hub. For local testing, create a temp modelfile pointing to an available model (e.g. `qwen2:0.5b`) with the same SYSTEM prompt.
- `scripts/run_outer.sh` expects the `mqgt_scf_reissue` repo as a sibling directory. Set `ZORA_MQGT_REPO` to override.
- No automated test suite, build system, or package manager exists in this repo — it is purely configuration and documentation.
