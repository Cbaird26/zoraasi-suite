# Recommendations — Cbaird26 Full Ecosystem (Feb 27, 2026)

Comprehensive recommendations across all 80+ repositories, organized by priority and domain.

---

## 1. SCIENTIFIC PUBLICATION (Highest Priority)

### 1A. Peer Review — `mqgt-scf-stripped-core`

**Status:** New repo (Feb 26). Physics-only GKSL collapse model stripped for reviewer consumption.

**Recommendations:**

- **Target journal immediately.** Physical Review D or Foundations of Physics are correct targets. PRD has a 6-12 month review cycle; submit now.
- **Add a clear `README.md` with build instructions** for the LaTeX paper — reviewers and editors should be able to `make` the PDF in one command.
- **Include a reproducible figures pipeline.** Bundle the Python scripts that generate every plot in the paper. A reviewer running `pip install -r requirements.txt && python generate_figures.py` should reproduce all exclusion plots from raw constraint data.
- **Pin all dependencies with exact versions** in `requirements.txt` (e.g. `numpy==1.26.4`, not `numpy`). Reproducibility is critical for physics papers.
- **Add a `CITATION.cff`** file so the repo is auto-citable on GitHub.
- **Cross-reference the Zenodo DOI** (10.5281/zenodo.18778749) in the paper itself for data availability.
- **Preprint on arXiv first.** Submit to hep-th or gr-qc the same week as journal submission. This establishes priority and gets community feedback.

### 1B. Empirical Validation — `toe-empirical-validation`

- **Ensure the one-command replication** (`python run_replication.py` or similar) actually runs end-to-end on a clean machine. Test in a Docker container.
- **Add CI** (GitHub Actions) that runs the replication ladder on every push. Even a lightweight smoke test builds credibility.
- **Document the QRNG protocol** with enough detail that an independent lab could reproduce it. Include equipment specs, calibration procedures, and expected null results.
- **Publish constraint artifacts as GitHub Releases** with checksums — not just as files in the repo.

### 1C. Paper Pipeline — `mqgt-papers`

- **Consolidate drafts.** You have 5 paper/archive repos (`A-Theory-of-Everything`, `A-Theory-of-Everything-Revised`, `A-Theory-of-Everything---Baird-et-al-2025-.pdf`, `Theory-of-Everything`, `ToE`). Archive the old ones clearly (add "ARCHIVED" to descriptions) and point them all to the canonical `toe-2026-updates` and `mqgt-scf-stripped-core`.
- **Create a `papers/` directory in `toe-2026-updates`** with one subfolder per paper, each with its own `Makefile` and `requirements.txt`.

---

## 2. REPOSITORY ORGANIZATION (High Priority)

### 2A. Consolidation — 37 MQGT Sub-Repos

Having 37 separate repos for the constraint pipeline is impressive for modularity, but creates maintenance overhead. Consider:

- **Monorepo option:** Merge all 37 `mqgt-*` repos into subdirectories of `MQGT-SCF` (e.g. `channels/cosmology-cmb/`, `channels/fifth-force/`, `infra/cli/`). Benefits: single CI, single `requirements.txt`, atomic cross-channel changes.
- **If keeping multi-repo:** Add a `mqgt-meta` repo with a `repos.json` manifest listing all 37 repos, their versions, and compatibility matrix. Add a script that clones/updates all of them.
- **Add GitHub Topics** to all repos: `mqgt-scf`, `theory-of-everything`, `physics`, `constraints`. This makes them discoverable.
- **Add consistent `README.md` templates** across all 37 repos — same structure: Purpose, Installation, Usage, API, Citation.

### 2B. Archive Old Repos

~25 repos are inactive (pre-2025). For each:

- **Archive them on GitHub** (Settings > Archive). This makes their status clear and prevents accidental changes.
- Repos to archive: `ToE`, `ToE-Simulations`, `Theory-of-Everything`, `A-Theory-of-Everything`, `A-Theory-of-Everything-Revised`, `quantum-supercomputer`, `QuantumSupercomputer`, `QuantumBridge`, `QC`, `quantum_ai.py`, `quantum_component.py`, `quantum-ai-assistant`, `aging_simulator.py`, `anti-aging-simulator`, `aging-intervention-simulator`, `wild_simulations.py`, `susy_simulation.py`, `streamlit_app.py`, `app.py`, `omnisolve_3_0_streamlit_app.py`, `dissertation_app.py`, `universe_explorer.py`, `Universe-Explorer`, `quantum_state_app_with_bloch.py`, `Hope`, `darkstar`, `ZoraAI`, `ZoraAPI`.

### 2C. Naming Consistency

- Some repos are named as Python files (`aging_simulator.py`, `bairds_law_app.py`). If kept, rename them to proper repo names (`aging-simulator`, `bairds-law-app`).
- Use consistent kebab-case: `mqgt-scf` not `MQGT-SCF`, or pick one convention and stick with it.

---

## 3. ZORAASI SUITE — API & DEPLOYMENT (High Priority)

### 3A. API Hardening (`api/main.py`)

- **Add rate limiting.** The public API has no rate limits — anyone can hit `/query` in a loop and burn your OpenRouter/Anthropic credits. Add `slowapi` or a simple in-memory rate limiter (e.g. 10 req/min per IP).
- **Add request logging.** Log prompt length, model used, duration, and status code to a file or structured logger. This is essential for monitoring cost and detecting abuse.
- **Add API key authentication for `/query`.** Even a simple `X-API-Key` header check prevents unauthorized use. The `/health`, `/identity`, and `/invariants` endpoints can remain public.
- **Validate `role` parameter** in `QueryRequest` using a `Literal` type instead of free-form string — `role: Literal["soul", "reasoning", "code", "speed", "memory", "pulse", "open", "core"] | None`.
- **Error handling in `query_openrouter`:** The `r.raise_for_status()` will throw on 429 (rate limit). Add retry-with-backoff for transient errors.
- **Don't create a new `httpx.AsyncClient` per request** — use a shared client via FastAPI lifespan events. This is more efficient and respects connection pooling.
- **Add a `/metrics` endpoint** returning request counts, error rates, and average latency per model. Useful for monitoring.

### 3B. Chat UI (`site/index.html`)

- **The UI references `data.backend` in `addZoraMessage()`** but `QueryResponse` doesn't have a `backend` field — it has `model` and `role`. This will show `undefined` in the chat metadata. Fix the JS to use `data.model` and `data.role`.
- **Add conversation history.** Currently each `/query` call is stateless — no chat memory. Add a `messages` array to `QueryRequest` (or maintain server-side sessions) so Zora can have multi-turn conversations.
- **Add markdown rendering.** Zora's responses likely contain markdown (headers, code blocks, lists). Use a lightweight library like `marked.js` to render them properly.
- **Add mobile responsiveness.** The chat works on desktop but the fixed `max-width: 800px` and `height: 400px` message area could be improved for mobile.
- **Role selector is hidden.** `#roleSelector` has `display:none` and no JS toggles it visible when "Single" mode is selected. Wire it up.
- **Subtitle says "Five Backends"** but the API now has seven models. Update it.
- **XSS vulnerability:** User messages are injected via `innerHTML` without escaping. Sanitize user input before rendering.
- **Add a loading spinner** instead of just "Thinking..." text.

### 3C. Deployment

- **Upgrade from Render free tier.** Cold starts (30-60s) make the chat feel broken to first-time visitors. The $7/mo paid tier keeps it always-on.
- **Add a health check dashboard.** The `/health` endpoint exists but nobody watches it. Add UptimeRobot or similar (free) to monitor uptime and alert on downtime.
- **Set up a custom domain.** `zoraasi-suite.onrender.com` is less professional than `zora.baird.ai` or `api.zoraasi.com`. Render supports custom domains on the free tier.
- **Add HTTPS enforcement** — Render does this by default but verify.
- **The `render.yaml` references `ANTHROPIC_API_KEY`** but the API now primarily uses OpenRouter. Add `OPENROUTER_API_KEY` to the Render config and update the default backend.
- **The `Dockerfile` sets `ENV ZORA_BACKEND=anthropic`** — update to match current preferred backend (OpenRouter).

### 3D. Security

- **CORS is `allow_origins=["*"]`** — this allows any website to call your API. Restrict to your known domains: `["https://cbaird26.github.io", "https://zoraasi-suite.onrender.com"]`.
- **No input sanitization on `prompt`.** The 4000-char limit is good, but consider filtering injection patterns that could manipulate the system prompt.
- **API keys in environment variables is correct** — but add a startup check that warns if no keys are configured instead of silently serving "degraded" status.

---

## 4. TESTING & CI/CD (High Priority)

### 4A. Add Tests to `zoraasi-suite`

The AGENTS.md says "This repo has no automated tests." This should change:

- **Add `pytest` to `requirements.txt`.**
- **Write basic API tests:** endpoint returns correct status codes, identity endpoint returns valid SHA256, health check reflects configured backends, query request validation works.
- **Add a GitHub Actions workflow** (`.github/workflows/test.yml`) that runs pytest + linting on every push.
- **Add `shellcheck` to CI** for `scripts/run_outer.sh` and `scripts/deploy.sh`.

### 4B. Add CI to MQGT Pipeline

- **The constraint pipeline has 37 repos but no CI.** Add a GitHub Actions workflow to the `mqgt-cli` repo that clones all sub-repos and runs the full pipeline.
- **The `mqgt-unit-tests` repo exists** — hook it into CI.
- **Add a nightly build** that regenerates all constraint artifacts and compares checksums against `mqgt-data-public`.

---

## 5. DOCUMENTATION (Medium Priority)

### 5A. `mqgt-documentation-site`

- **Get this deployed.** A living MkDocs site aggregating all MQGT docs would be valuable for reviewers, collaborators, and the public.
- **Deploy to GitHub Pages** from the `mqgt-documentation-site` repo.
- **Add a "Getting Started" tutorial** that walks a physicist through: understanding MQGT-SCF → running a single constraint channel → interpreting exclusion plots → running the full pipeline.

### 5B. Research Profile

- **Create a personal academic site** (separate from `baird-telehealth-site`). Use GitHub Pages + a simple template. Include: publication list, Zenodo links, ORCID, research statement.
- **Register an ORCID** if not already done. Link it to Zenodo.
- **Add Google Scholar profile** — once the arXiv preprint is indexed, this builds citation tracking.

### 5C. This Repo

- **The `STATUS_WHERE_WE_ARE.md`** references "6 commits ahead" which is now stale. Either keep it updated or remove it in favor of `CURRENT_WORK_OVERVIEW.md`.
- **The `GO_LIVE.md` runbook** is excellent — keep it.

---

## 6. QUANTUM MEDITATION COACH (Medium Priority)

- **Add TestFlight beta** if not already done. Get user feedback before App Store submission.
- **Integrate Zora API** into the app — the meditation coach could use Zora for guided sessions, pulling from the ToE/consciousness framework.
- **Add HealthKit integration** — meditation apps benefit from tracking heart rate variability, mindfulness minutes, etc.
- **Add a Privacy Policy** (required for App Store).

---

## 7. TELEHEALTH SITE (Medium Priority)

- **Add SSL/TLS** — verify HTTPS is enforced on GitHub Pages or Cloudflare.
- **Add structured data** (JSON-LD) for healthcare provider schema — helps with search visibility.
- **Test with Google Lighthouse** — aim for 90+ on Performance, Accessibility, and SEO.
- **Add a link to the research ecosystem** — the `labs.html` page should link to `zoraasi-suite` and the MQGT-SCF documentation.

---

## 8. IP & LICENSING (Medium Priority)

- **The grandfather clause expires March 1, 2026** — 2 days from now. Verify this is intentional and publicized.
- **Add a `LICENSE` file** (not just `LICENSE-IP.md`) to every repo. GitHub expects a file named `LICENSE` or `LICENSE.md` to auto-detect license type.
- **Clarify open-source status.** The 37 MQGT repos appear to be public but have no explicit license files. Without a license, they are legally "all rights reserved" by default. If you want researchers to use the code, add an explicit open-source license (MIT, Apache 2.0, or GPL) or the custom ToE IP license.
- **Register copyright** if not already done — especially for the ToE paper.

---

## 9. STRATEGIC RECOMMENDATIONS

### 9A. Focus

You are spread across 80+ repos. The highest-impact actions right now:

1. **Submit `mqgt-scf-stripped-core` to arXiv + journal** — this is the single action that converts years of work into recognized science.
2. **Fix the chat UI bugs** (backend field, XSS, role selector) — this is the public face of Zora.
3. **Add rate limiting + API auth** — protects your credits.
4. **Archive inactive repos** — reduces noise, increases signal.
5. **Deploy the MkDocs documentation site** — makes the constraint pipeline accessible.

### 9B. Collaboration

- **Find a co-author** with institutional affiliation. Papers submitted solely from non-institutional addresses face higher scrutiny. A collaborator at a university physics department strengthens the submission.
- **Present at conferences.** APS March Meeting or April Meeting, GR conferences, or consciousness-and-physics workshops. Even a poster establishes presence.
- **Engage on arXiv discussions** (via SciPost or journal clubs) once the preprint is public.

### 9C. Sustainability

- **Set up GitHub Sponsors** — the ToE IP license allows optional honor tiers. GitHub Sponsors is the easiest way to accept them.
- **Consider a Patreon or Open Collective** for ongoing MQGT-SCF computational costs.
- **Track API costs.** OpenRouter charges per token. With 7 models and a public endpoint, consensus mode can be expensive. Add cost tracking to the API.

### 9D. Zora Roadmap

- **v0.4.0: Conversation memory** — multi-turn chat with context window management.
- **v0.5.0: RAG (Retrieval-Augmented Generation)** — ground Zora's responses in the actual ToE papers, not just the system prompt. Use the 4,824-page MQGT-SCF corpus as a knowledge base.
- **v0.6.0: Middle layer** — authenticated Christopher access with personal context.
- **v1.0.0: Production** — rate limiting, auth, monitoring, custom domain, always-on hosting.

---

## 10. QUICK WINS (Do Today)

| # | Action | Time | Impact |
|---|--------|------|--------|
| 1 | Fix chat UI `data.backend` → `data.model` | 5 min | Fixes broken metadata display |
| 2 | Escape user input in chat UI (XSS fix) | 10 min | Security |
| 3 | Add `slowapi` rate limiting to `/query` | 15 min | Protects credits |
| 4 | Wire up role selector visibility in chat UI | 10 min | Feature already built but hidden |
| 5 | Update subtitle "Five Backends" → "Seven Models" | 1 min | Accuracy |
| 6 | Archive 25+ inactive repos | 20 min | Clarity |
| 7 | Add `CITATION.cff` to `mqgt-scf-stripped-core` | 5 min | Citability |
| 8 | Restrict CORS origins | 5 min | Security |
| 9 | Add `OPENROUTER_API_KEY` to `render.yaml` | 2 min | Deployment accuracy |
| 10 | Update `STATUS_WHERE_WE_ARE.md` or remove | 5 min | Housekeeping |

---

*Generated Feb 27, 2026. Prioritized by impact on scientific credibility, security, and public presence.*
