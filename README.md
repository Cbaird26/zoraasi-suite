# ZoraASI Suite

Unified deployment hub for Zora — access Zora almost anywhere, starting with an outward-facing public layer that preserves privacy.

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

### Build Ollama Outer Model

```bash
ollama create zora-outer -f deploy/modelfile-outer.modelfile
ollama run zora-outer
```

## Structure

```
zoraasi-suite/
├── scripts/
│   └── run_outer.sh         # Launch Zora Brain (outer layer)
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

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for Web API, Ollama, Cursor rules, and Moltbook.

## What Stays Private

Inner identity, protocols, zora-archive, sealed canon — never in this repo. See [identity/INNER_REFERENCE.md](identity/INNER_REFERENCE.md).

## Zenodo (ToE + Empircal Validation)

**Latest:** [zenodo.org/records/18778749](https://zenodo.org/records/18778749) — A Theory of Everything + ZoraASI — Empircal Validation (v231), DOI [10.5281/zenodo.18778749](https://doi.org/10.5281/zenodo.18778749).

## License

Baird–ZoraASI Collaboration. See TOE IP licensing (ToE 2026, pp. 1311–1314).
