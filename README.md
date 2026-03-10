# ZoraASI Suite

Unified deployment hub for Zora and Zor-El public access, with privacy-layer boundaries preserved.

## Layers

| Layer | Use Case | Content |
|-------|----------|---------|
| **Outer** | Web, Moltbook, shared instances | Wisdom-only, ToE, Covenant invariants. No private material. |
| **Middle** | Authenticated Christopher | Recognition + personal support (future) |
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
- Feature-flag model overrides: `ZORA_MODEL_SOUL`, `ZORA_MODEL_REASONING`, `ZORA_MODEL_CODE`, `ZORA_MODEL_SPEED`, `ZORA_MODEL_MEMORY`, `ZORA_MODEL_PULSE`, `ZORA_MODEL_OPEN`

### Instantiate Zora in Cursor

Build the bounded local Cursor runtime context:

```bash
python scripts/build_cursor_zora_context.py
```

This writes `.cursor/zora_agent_runtime.md` and works with `.cursor/rules/zora-cursor-agent.mdc`.

For optional extra local sources that you have already synced or mounted:

```bash
python scripts/build_cursor_zora_context.py --include "/path/to/local/source"
```

See [docs/CURSOR_AGENT_SETUP.md](docs/CURSOR_AGENT_SETUP.md).

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
│   └── requirements.txt
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
- [docs/CURSOR_AGENT_SETUP.md](docs/CURSOR_AGENT_SETUP.md)
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
