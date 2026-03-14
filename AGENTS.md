# AGENTS.md

## Cursor Cloud specific instructions

### Overview

The **ZoraASI Suite** is the deployment hub for Zora — the AI identity from the Baird-ZoraASI collaboration. It includes a FastAPI-based Zora API, an animated landing page with chat widget, identity documents, Ollama modelfiles, and deployment configs.

### Repository contents

| Directory/File | Purpose |
|---|---|
| `api/main.py` | FastAPI Zora API — OpenRouter, Anthropic, Ollama; multi-role, multi-mode |
| `api/auth.py` | JWT auth for Middle layer (ZORA_LAYER=middle) |
| `api/requirements.txt` | Python deps: fastapi, uvicorn, httpx, pydantic, slowapi, python-jose, passlib |
| `api/tests/` | Unit and integration tests |
| `site/index.html` | Landing page with animated Φc visualization + chat widget |
| `identity/` | Outer (public) and inner (reference) Zora identity docs |
| `deploy/` | Ollama modelfile and deployment config YAML |
| `scripts/run_outer.sh` | Launcher that delegates to `mqgt_scf_reissue` |
| `scripts/deploy.sh` | Unified deploy script (fly/railway/render/local/ollama) |
| `Dockerfile` | Container-ready build |
| `fly.toml` / `railway.json` / `render.yaml` | Platform deployment configs |
| `.cursor/rules/zora-outer.mdc` | Cursor rule for Zora outer identity |

### Running the Zora API

```bash
pip install -r api/requirements.txt

# Anthropic backend (recommended, fast ~2-10s responses)
ZORA_BACKEND=anthropic ANTHROPIC_API_KEY=sk-ant-... uvicorn api.main:app --port 8000

# Ollama backend (local, private, needs GPU for reasonable speed)
ZORA_BACKEND=ollama OLLAMA_MODEL=zora-outer uvicorn api.main:app --port 8000

# OpenAI backend
ZORA_BACKEND=openai OPENAI_API_KEY=sk-... uvicorn api.main:app --port 8000
```

Endpoints: `/` (root), `/health`, `/identity`, `/invariants`, `POST /query`, `POST /auth/login`, `POST /auth/refresh`, `/chat` (landing page), `/docs` (Swagger). When `ZORA_LAYER=middle`, `/query` requires `Authorization: Bearer <token>`. See [docs/ENV_AND_CREDENTIALS.md](docs/ENV_AND_CREDENTIALS.md).

### Live deployment

Zora API is deployed on Render at `https://zoraasi-suite.onrender.com`. The `gh-pages` branch serves the landing page at `cbaird26.github.io/zoraasi-suite`.

### Linting

No project-level lint config. Use these tools (installed via the update script):

- **Shell**: `shellcheck scripts/run_outer.sh scripts/deploy.sh`
- **Markdown**: `markdownlint '**/*.md'` (expect line-length warnings in existing docs)
- **YAML**: `yamllint deploy/config.yaml` (expect line-length warnings)
- **Python**: Standard Python linting on `api/main.py`

### External AI integration (Grok, ChatGPT)

- **Ask Zora**: [zoraasi-suite.onrender.com](https://zoraasi-suite.onrender.com) — Outer identity only. No vault, no private logs.
- **Public corpus**: `public_corpus_bundle/` — Sanitized for RAG or Custom GPT.
- **Public MCP**: `mcp/zora_public_server.py` — Tools: `get_zora_identity`, `query_zora`.

### Key caveats

- The Ollama `gpt-oss:20b` model requires ~14GB RAM. On CPU-only VMs, inference takes 2+ minutes per response; use the Anthropic or OpenAI backend instead.
- Ollama's `/api/generate` endpoint may hang on CPU. Use `/api/chat` instead (the API code already does this).
- Set `OLLAMA_NEW_ENGINE=true` when running Ollama serve to avoid inference timeouts.
- The Render free tier has cold starts (~30-60s after 15min idle).
- The `ANTHROPIC_API_KEY` requires credits loaded on the Anthropic account. A 401 error means invalid key; a 400 means insufficient credits.
- The Zora outer identity system prompt is in `api/main.py` (SYSTEM_PROMPT constant) and mirrors `identity/ZORA_OUTER_IDENTITY.md`.
- This repo has no automated tests — validation is limited to linting and manual API testing.
- `scripts/run_outer.sh` requires the external `mqgt_scf_reissue` repo (not public). The API (`api/main.py`) is self-contained and does not need it.
