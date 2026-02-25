# ZoraASI Suite — Deployment Guide

How to deploy Zora for "access almost anywhere" — web, local, Moltbook, agents.

---

## Option 1: Web API (Vercel / Railway / Fly.io)

1. Clone zoraasi-suite and mqgt_scf (or use zora-brain-backend as submodule).
2. Set env: `ZORA_IDENTITY_LAYER=outer`, `ZORA_CANON_DIR=/path/to/zora-canon-v1`.
3. Do **not** mount `memory/` — outer layer loads from `identity/ZORA_OUTER_IDENTITY.md`.
4. Deploy Zora Brain API (FastAPI) with uvicorn.
5. Expose `/`, `/health`, `POST /query`, `/chat` (if chat UI included).

**Example (Fly.io):**
```bash
fly launch
fly secrets set ZORA_IDENTITY_LAYER=outer
fly deploy
```

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

## Option 5: iCloud / Cursor Agents (Future)

Document how to point agents at:
- Outer API URL (if deployed)
- Modelfile path for local Ollama
- Cursor rule for Zora-outer

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
