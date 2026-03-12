# Environment Variables and Credentials

**Audit of env vars used across ZoraASI Suite.** Layer attribution and secret handling.

---

## Layer Attribution

| Layer | Env Vars | Contains Secrets? |
|-------|----------|-------------------|
| **Outer** | OPENROUTER_API_KEY, ANTHROPIC_API_KEY, OLLAMA_*, ZORA_DEFAULT_ROLE, ZORA_MODE, ZORA_MODEL_*, ZORA_LAYER | Yes (API keys) |
| **Middle** | ZORA_LAYER, JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRY, MIDDLE_USER, MIDDLE_PASSWORD, MIDDLE_PASSWORD_HASH | Yes (JWT, password) |
| **Inner** | ZORA_MQGT_REPO, ZORA_CANON_DIR, ZORA_MEMORY_DIR, ZORA_OUTER_IDENTITY_PATH, ZORA_IDENTITY_LAYER | No (paths only) |

---

## Variable Reference

### API Keys (Secrets — never commit)

| Variable | Layer | Purpose |
|----------|-------|---------|
| `OPENROUTER_API_KEY` | Outer | OpenRouter API for GPT, Claude, Grok, Llama, Gemini |
| `ANTHROPIC_API_KEY` | Outer | Optional direct Anthropic fallback |

### Ollama (Local)

| Variable | Default | Purpose |
|----------|---------|---------|
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `zora-outer` | Model for `core` role |

### Zora API Tuning

| Variable | Default | Purpose |
|----------|---------|---------|
| `ZORA_DEFAULT_ROLE` | `soul` | Default model role |
| `ZORA_MODE` | `single` | Mode: single, router, consensus |
| `ZORA_MODEL_SOUL` | (empty) | Override model for soul role |
| `ZORA_MODEL_REASONING` | (empty) | Override for reasoning |
| `ZORA_MODEL_CODE` | (empty) | Override for code |
| `ZORA_MODEL_SPEED` | (empty) | Override for speed |
| `ZORA_MODEL_MEMORY` | (empty) | Override for memory |
| `ZORA_MODEL_PULSE` | (empty) | Override for pulse |
| `ZORA_MODEL_OPEN` | (empty) | Override for open |

### Layer Selection (API)

| Variable | Default | Purpose |
|----------|---------|---------|
| `ZORA_LAYER` | `outer` | API layer: `outer` (no auth) or `middle` (JWT required on /query) |

### Zora Brain (Outer / Inner)

| Variable | Purpose |
|----------|---------|
| `ZORA_IDENTITY_LAYER` | `outer` or `inner` (Zora Brain identity selection) |
| `ZORA_OUTER_IDENTITY_PATH` | Path to ZORA_OUTER_IDENTITY.md |
| `ZORA_MQGT_REPO` | Path to mqgt_scf_reissue (for run_outer.sh) |
| `ZORA_CANON_DIR` | Canon directory |
| `ZORA_MEMORY_DIR` | Memory directory |

### Middle Layer (JWT — when ZORA_LAYER=middle)

| Variable | Default | Purpose |
|----------|---------|---------|
| `JWT_SECRET` | (required) | Secret for signing tokens |
| `JWT_ALGORITHM` | HS256 | Algorithm |
| `JWT_EXPIRY` | 3600 | Access token expiry (seconds) |
| `MIDDLE_USER` | chris | Login username |
| `MIDDLE_PASSWORD` | (empty) | Dev: plain password |
| `MIDDLE_PASSWORD_HASH` | (empty) | Prod: bcrypt hash of password |

---

## Best Practices

1. **Never commit real secrets.** Use `.env` (gitignored) or platform secrets (Render, Fly.io, Railway).
2. **Use `.env.example`** with placeholders only. Copy to `.env` and fill locally.
3. **Rotate API keys** periodically; rotate immediately if exposed.
4. **Audit deployments** — ensure OPENROUTER_API_KEY and ANTHROPIC_API_KEY are set via platform secrets, not env files in repo.

---

## Files

- `.env` — Local secrets (gitignored). Create from `.env.example`.
- `.env.example` — Template with placeholders. Safe to commit.
- `*.credentials.json` — OAuth credentials (gitignored).
