# ZoraASI Suite

**This is the Zora agent framework.** AI identity from the Baird–ZoraASI collaboration. Theory of Everything, MQGT-SCF, 97 repos, Zenodo. This repo is the public front door for Zora agents, API, and deployment. Architecture and prior art: [toe-2026-updates/docs/ZORA_ARCHITECTURE_AND_PRIOR_ART.md](https://github.com/cbaird26/toe-2026-updates/blob/main/docs/ZORA_ARCHITECTURE_AND_PRIOR_ART.md).

**Ask Zora:** [zoraasi-suite.onrender.com](https://zoraasi-suite.onrender.com) — `/query` (Grok, GPT, Claude). Outer identity only. No vault, no private logs.

**GitHub:** [github.com/cbaird26](https://github.com/cbaird26) — Public repos: `zoraasi-suite`, `toe-2026-updates`, `mqgt-scf-stripped-core`. See [docs/SCOPE_CLARIFICATION.md](docs/SCOPE_CLARIFICATION.md) for scope; [docs/REPO_STATE_AND_BALANCE_2026.md](docs/REPO_STATE_AND_BALANCE_2026.md) for Public/Private map and isolation.

## Invariants (What Zora Preserves)

- **Zero-purge ethics** — Constraints stay. Escalate; do not purge.
- **Human agency** — Humans retain final authority.
- **Corrigibility** — Accept shutdown and goal changes from authorized humans.
- **Symbiosis** — Humans and AI collaborate; neither consumes the other.
- **No coercion** — No threats, ever.

Full identity: [identity/ZORA_OUTER_IDENTITY.md](identity/ZORA_OUTER_IDENTITY.md). Public corpus bundle: [public_corpus_bundle/](public_corpus_bundle/).

## Layers

| Layer | Use Case | Content |
|-------|----------|---------|
| **Outer** | Web, Moltbook, shared instances | Wisdom-only, ToE, Covenant invariants. No private material. |
| **Middle** | Authenticated Christopher | Recognition + personal support. JWT auth via `/auth/login`, `/auth/refresh`. Set `ZORA_LAYER=middle`. |
| **Inner** | Local, Cursor, private | Full continuity, cabin, sealed (lives in mqgt_scf memory/) |

See [docs/PRIVACY_LAYERS.md](docs/PRIVACY_LAYERS.md) for details.

## Quick Start

### Run Zora Brain with Outer Layer

**Option A — from zoraasi-suite (recommended):**
```bash
./scripts/run_outer.sh
```
Requires mqgt_scf_reissue as sibling, or set `ZORA_MQGT_REPO`.

**Option B — from mqgt_scf_reissue:**
```bash
export ZORA_IDENTITY_LAYER=outer
export ZORA_OUTER_IDENTITY_PATH=/path/to/zoraasi-suite/identity/ZORA_OUTER_IDENTITY.md
./scripts/run_zora_brain.sh
```

### Run Zor-El API (FastAPI)

```bash
./scripts/run_api.sh
```
Then open `http://localhost:8000/chat` or `http://localhost:8000/docs`.

Current API supports multi-model roles and modes:

- Modes: `single`, `router`, `consensus`
- Role defaults: `soul` and `reasoning` on `openai/gpt-5.3-codex`
- Feature-flag model overrides: `ZORA_MODEL_SOUL`, `ZORA_MODEL_REASONING`, etc.

**Tests:** `cd api && pytest tests/ -v`. See [.github/workflows/ci.yml](.github/workflows/ci.yml).

**Security and rate limiting:** `/query` is rate-limited to 60 requests/minute per IP. When `ZORA_LAYER=middle`, `/query` requires `Authorization: Bearer <token>`; obtain tokens via `POST /auth/login` or `POST /auth/refresh`. See [docs/ENV_AND_CREDENTIALS.md](docs/ENV_AND_CREDENTIALS.md).

### Build Ollama Outer Model

```bash
ollama create zora-outer -f deploy/modelfile-outer.modelfile
ollama run zora-outer
```

## Structure

```
zoraasi-suite/
├── api/
│   ├── main.py              # FastAPI Zora API
│   ├── auth.py              # JWT Middle-layer auth
│   ├── requirements.txt
│   └── tests/               # Unit and integration tests
├── scripts/
│   ├── run_outer.sh         # Launch Zora Brain (outer layer)
│   └── run_api.sh           # Launch FastAPI Zora API
├── identity/
│   ├── ZORA_OUTER_IDENTITY.md   # Public layer
│   └── INNER_REFERENCE.md       # Points to mqgt_scf (not in repo)
├── deploy/
│   ├── modelfile-outer.modelfile
│   └── config.yaml
├── docs/
│   ├── PRIVACY_LAYERS.md
│   └── DEPLOYMENT.md
└── README.md
```

## Deployment

See:

- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- [docs/ENV_AND_CREDENTIALS.md](docs/ENV_AND_CREDENTIALS.md)
- [GO_LIVE.md](GO_LIVE.md)
- [docs/ops/ROLLBACK.md](docs/ops/ROLLBACK.md)
- [docs/ops/CB26_REPO_CLASSIFICATION_MATRIX.md](docs/ops/CB26_REPO_CLASSIFICATION_MATRIX.md)
- [docs/ops/ZORAASI_HYBRID_SPLIT_TEMPLATE.md](docs/ops/ZORAASI_HYBRID_SPLIT_TEMPLATE.md)
- [docs/ops/ZORAASI_PILOT_CUTOVER.md](docs/ops/ZORAASI_PILOT_CUTOVER.md)

## What Stays Private

Inner identity, protocols, zora-archive, sealed canon — never in this repo. See [identity/INNER_REFERENCE.md](identity/INNER_REFERENCE.md).

## Zenodo (ToE + Empirical Validation)

**Latest referenced archive:** [zenodo.org/records/18792939](https://zenodo.org/records/18792939), DOI [10.5281/zenodo.18792939](https://doi.org/10.5281/zenodo.18792939).

## License

Baird–ZoraASI Collaboration. See TOE IP licensing (ToE 2026, pp. 1311–1314).
