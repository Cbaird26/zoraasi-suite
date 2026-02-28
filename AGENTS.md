# AGENTS.md

## Cursor Cloud specific instructions

### Overview

The **ZoraASI Suite** is the deployment hub for Zora — the AI identity from the Baird-ZoraASI collaboration. It includes the Zor-El multi-model API (v0.4.0), a chat UI with markdown rendering, identity documents, Ollama modelfiles, and deployment configs.

### Repository contents

| Directory/File | Purpose |
|---|---|
| `api/main.py` | Zor-El API v0.4.0 — 7 models via OpenRouter, 3 modes, rate limiting, auth, metrics |
| `api/requirements.txt` | Python deps: fastapi, uvicorn, httpx, pydantic, slowapi |
| `site/index.html` | Chat UI with XSS protection, role selector, markdown rendering, mobile responsive |
| `identity/` | Outer (public) and inner (reference) Zora identity docs |
| `deploy/` | Ollama modelfile and deployment config YAML |
| `tests/test_api.py` | 17 pytest tests covering all endpoints and validation |
| `scripts/run_outer.sh` | Launcher that delegates to `mqgt_scf_reissue` |
| `scripts/deploy.sh` | Unified deploy script (fly/railway/render/local/ollama) |
| `scripts/apply_recommendations.sh` | Cross-repo maintenance (archive, topics, citation, license) |
| `Dockerfile` | Container-ready build |
| `fly.toml` / `railway.json` / `render.yaml` | Platform deployment configs |
| `.github/workflows/ci.yml` | GitHub Actions CI: pytest + shellcheck + syntax |
| `.cursor/rules/zora-outer.mdc` | Cursor rule for Zora outer identity |
| `CITATION.cff` | Auto-citation metadata |

### Running the Zor-El API

```bash
pip install -r api/requirements.txt

# OpenRouter (recommended — access to all 7 models)
OPENROUTER_API_KEY=sk-or-... uvicorn api.main:app --port 8000

# Anthropic fallback
ANTHROPIC_API_KEY=sk-ant-... uvicorn api.main:app --port 8000

# Ollama (local, private, needs GPU)
OLLAMA_MODEL=zora-outer uvicorn api.main:app --port 8000
```

Endpoints: `/` (root), `/health`, `/identity`, `/invariants`, `/models`, `/metrics`, `POST /query`, `/chat` (UI), `/docs` (Swagger).

### Environment variables

| Variable | Purpose | Default |
|---|---|---|
| `OPENROUTER_API_KEY` | OpenRouter API key (primary) | — |
| `ANTHROPIC_API_KEY` | Anthropic API key (fallback) | — |
| `OLLAMA_HOST` | Ollama server URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | Ollama model name | `zora-outer` |
| `ZORA_DEFAULT_ROLE` | Default model role | `soul` |
| `ZORA_MODE` | Default query mode | `single` |
| `ZORA_API_KEY` | Optional API key for `/query` auth | — (open) |
| `ZORA_CORS_ORIGINS` | Comma-separated allowed origins | GitHub Pages + Render |
| `ZORA_CORS_ALLOW_ALL` | Set to `true` for `*` CORS | — |

### Running tests

```bash
pip install pytest pytest-asyncio
python -m pytest tests/ -v
```

17 tests cover: root, health, models, identity, invariants, metrics, query validation, chat UI, system prompt, and API key auth.

### Live deployment

Zora API is deployed on Render at `https://zoraasi-suite.onrender.com`. The `gh-pages` branch serves the landing page at `cbaird26.github.io/zoraasi-suite`.

### Linting

- **Shell**: `shellcheck scripts/run_outer.sh scripts/deploy.sh`
- **Markdown**: `markdownlint '**/*.md'` (expect line-length warnings)
- **YAML**: `yamllint deploy/config.yaml` (expect line-length warnings)
- **Python**: `python -m py_compile api/main.py`

### Key caveats

- The Ollama `gpt-oss:20b` model requires ~14GB RAM. On CPU-only VMs, inference takes 2+ minutes per response; use OpenRouter or Anthropic instead.
- Ollama's `/api/generate` endpoint may hang on CPU. Use `/api/chat` instead (the API code already does this).
- The Render free tier has cold starts (~30-60s after 15min idle).
- Rate limiting is 30 requests/minute per IP on `/query`.
- If `ZORA_API_KEY` is set, all `/query` requests require `X-API-Key` header.
- The Zora outer identity system prompt is in `api/main.py` (SYSTEM_PROMPT constant) and mirrors `identity/ZORA_OUTER_IDENTITY.md`.
- `scripts/run_outer.sh` requires the external `mqgt_scf_reissue` repo (not public). The API (`api/main.py`) is self-contained and does not need it.
