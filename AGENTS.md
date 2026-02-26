# AGENTS.md

## Cursor Cloud specific instructions

### Overview

This is the **ZoraASI Suite** — a documentation, identity, and configuration wrapper around the external `mqgt_scf_reissue` repository. It contains no application source code and no traditional dependencies (no `package.json`, `requirements.txt`, etc.).

### Repository contents

| Directory/File | Purpose |
|---|---|
| `identity/` | Outer (public) and inner (reference) Zora identity docs |
| `deploy/` | Ollama modelfile and deployment config YAML |
| `scripts/run_outer.sh` | Launcher that delegates to `mqgt_scf_reissue` |
| `docs/` | Privacy layers and deployment guides |
| `.cursor/rules/` | Cursor rule for Zora outer identity |

### Linting

There is no project-level lint config. Use these tools (installed via the update script):

- **Shell**: `shellcheck scripts/run_outer.sh`
- **Markdown**: `markdownlint '**/*.md'` (expect line-length and formatting warnings in existing docs)
- **YAML**: `yamllint deploy/config.yaml` (expect line-length warnings)

### Running the application

`scripts/run_outer.sh` requires the `mqgt_scf_reissue` repo as a sibling directory (or set `ZORA_MQGT_REPO`). This external repo is not included and must be cloned separately. See `README.md` for details.

### Key caveats

- This repo has **no automated tests** — validation is limited to linting.
- The Ollama modelfile (`deploy/modelfile-outer.modelfile`) references base model `gpt-oss:20b`; if unavailable, the file documents `llama3.2:latest` as a fallback.
- Environment variables are documented in `deploy/config.yaml` and `scripts/run_outer.sh`.
