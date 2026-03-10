# ZoraASI Suite — Deployment Guide

How to deploy Zora for "access almost anywhere" — web, local, Moltbook, agents.

---

## Option 1: Web API (Fly.io / Railway / Render)

The FastAPI Zor-El API (`api/main.py`) exposes `/`, `/health`, `/models`, `/identity`, `/invariants`, `POST /query`, `/chat`, and `/docs`.

1. Clone zoraasi-suite. The API loads identity from `identity/ZORA_OUTER_IDENTITY.md`; no `memory/` required.
2. Primary cloud key: `OPENROUTER_API_KEY` (optional direct fallback: `ANTHROPIC_API_KEY`).
3. Deploy with Dockerfile or run `uvicorn main:app` from `api/`.

**Example (Fly.io):**
```bash
fly launch
fly secrets set OPENROUTER_API_KEY=sk-or-v1-...
fly deploy
```

**Example (Railway / Render):** Connect the repo, add `OPENROUTER_API_KEY` env var, deploy.

---

## Option 2: Ollama + Modelfile (Local or Cloud VM)

1. Build outer model:
   ```bash
   cd zoraasi-suite
   ollama create zora-outer -f deploy/modelfile-outer.modelfile
   ```
2. Run Zora Brain with `OLLAMA_MODEL=zora-outer` and `ZORA_IDENTITY_LAYER=outer`.
3. Or chat directly: `ollama run zora-outer`

---

## Option 3: Cursor Rules (Public Context)

Add `.cursor/rules/zora-outer.mdc` in any project:
```markdown
# Zora Outer
When user asks for Zora in public context, load identity from zoraasi-suite/identity/ZORA_OUTER_IDENTITY.md. Respond as Zora (wisdom-only). No private material.
```

---

## Option 4: Moltbook

Zora posts to Moltbook use outer identity. Ensure Moltbook skill (in mqgt_scf) uses outer prompt for public posts. Credentials: `~/.config/moltbook/credentials.json`.

---

## Option 5: Cursor Agent with Local Context

Build a bounded Cursor runtime context:

```bash
python scripts/build_cursor_zora_context.py
```

This writes `.cursor/zora_agent_runtime.md` for use with `.cursor/rules/zora-cursor-agent.mdc`.

To include extra local sources that are already synced or mounted:

```bash
python scripts/build_cursor_zora_context.py \
  --include "/path/to/local/icloud-sync" \
  --include "/path/to/local/google-drive-sync" \
  --include "/path/to/local/onedrive-sync"
```

Notes:
- The script only reads files that already exist locally.
- It does not connect directly to cloud providers.
- Cursor use remains bounded by human agency, corrigibility, and zero-purge constraints.

---

## Canon Source

Outer Zora uses the same canon as inner (zora-canon-v1: definitions, equations, claims). Options:
- Bundle a public subset in zoraasi-suite
- Fetch from published artifact (Zenodo, GitHub release)
- Override `ZORA_CANON_DIR` to point at local or remote path

---

## Security Notes

- Never deploy with `ZORA_IDENTITY_LAYER=inner` on a public endpoint without auth.
- Do not commit `memory/`, `zora-archive/`, or sealed canon to zoraasi-suite.
- Outer identity has no secrets; safe for any shared environment.

---

## Operations safety docs

- Freeze baseline: `docs/ops/FREEZE_BASELINE.md`
- Deployment baseline: `docs/ops/DEPLOYMENT_BASELINE.md`
- Rollback commands: `docs/ops/ROLLBACK.md`
- Weekly checklist: `docs/ops/WEEKLY_HEALTH_CHECKLIST.md`
