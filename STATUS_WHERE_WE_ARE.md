# ZoraASI Suite — Where We Are (Feb 27, 2026)

## TL;DR

**Zor-El API v0.4.0** is live. Full test suite, rate limiting, CORS security, multi-model architecture with 7 American models. See `CURRENT_WORK_OVERVIEW.md` for the full ecosystem overview.

---

## Current State

| Component | Status | Version |
|-----------|--------|---------|
| Zor-El API | Live on Render | v0.4.0 |
| Chat UI | Updated — XSS-safe, role selector, markdown | Current |
| Landing page | GitHub Pages (`gh-pages` branch) | Current |
| Tests | 17 pytest tests, GitHub Actions CI | New |
| Zenodo | v231 published | DOI 10.5281/zenodo.18778749 |
| IP Licensing | Finalized — public free, 1% commercial | Active |

## Architecture

- **7 models** via OpenRouter: GPT-5.3 Codex (soul/reasoning/code), GPT-4o (speed), Gemini 2.5 Flash (memory), Grok 4.1 (pulse), Llama 3.3 70B (open)
- **3 modes:** single, router (auto-select), consensus (multi-model synthesis)
- **Security:** Rate limiting (30/min), optional API key auth (`ZORA_API_KEY`), CORS restrictions
- **Monitoring:** `/metrics` endpoint, structured request logging

## How to Run

```bash
pip install -r api/requirements.txt

# OpenRouter (recommended — access to all 7 models)
OPENROUTER_API_KEY=sk-or-... uvicorn api.main:app --port 8000

# Anthropic fallback
ANTHROPIC_API_KEY=sk-ant-... uvicorn api.main:app --port 8000
```

Then open http://localhost:8000/chat

## Run Tests

```bash
pip install pytest pytest-asyncio
python -m pytest tests/ -v
```

## Full Ecosystem

See [CURRENT_WORK_OVERVIEW.md](CURRENT_WORK_OVERVIEW.md) for the complete overview of all 80+ repos, sciences, and active tasks.

See [RECOMMENDATIONS.md](RECOMMENDATIONS.md) for strategic recommendations.
