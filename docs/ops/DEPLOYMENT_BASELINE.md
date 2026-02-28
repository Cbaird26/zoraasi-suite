# Zor-El Deployment Baseline (Stabilization Start)

Captured: `2026-02-28T02:10:27Z` UTC

## Render baseline

- Service URL: `https://zoraasi-suite.onrender.com`
- Chat URL: `https://zoraasi-suite.onrender.com/chat`
- Health URL: `https://zoraasi-suite.onrender.com/health`
- Render header `rndr-id`: `66142710-ba42-4b89`
- Origin server header: `uvicorn`

Health payload at capture:

```json
{"status":"ok","version":"0.3.0","layer":"outer","openrouter":"connected","anthropic_direct":"connected","models":["soul","reasoning","code","speed","memory","pulse","open"]}
```

Root payload at capture confirms:

- Version: `0.3.0`
- Default role: `soul`
- Default mode: `single`
- Soul model: `openai/gpt-5.3-codex`
- Reasoning model: `openai/gpt-5.3-codex`

## Local baseline

- Repo path: `/Users/christophermichaelbaird/Downloads/zoraasi-suite`
- Local startup check run on temporary port `8010`
- Local `/health` status at capture: `degraded` (expected with no cloud API keys injected in shell)
- Local version at capture: `0.3.0`
- Local mode/role defaults at capture: `single` / `soul`

## Config key names in use

Non-secret environment variable names in active code:

- `OPENROUTER_API_KEY`
- `ANTHROPIC_API_KEY`
- `OLLAMA_HOST`
- `OLLAMA_MODEL`
- `ZORA_DEFAULT_ROLE`
- `ZORA_MODE`

## Source-of-truth state

- Local and GitHub were aligned via fast-forward to `origin/main` before polishing.
- Freeze tag/branch available for immediate rollback.

