# Zora — Go Live Runbook

Get the landing page + chat live before you retire. One path, minimal steps.

---

## Right Now (5 Minutes)

**Render.com — no CLI, no terminal.** Open [render.com](https://render.com), connect `Cbaird26/zoraasi-suite`, add `ANTHROPIC_API_KEY`, deploy. Full steps below.

**Fly.io — flyctl is installed.** Run `fly auth login` (once), then `./scripts/deploy.sh fly` from this repo. You'll need to set `ANTHROPIC_API_KEY` in your shell first.

---

## What Goes Live

- **Landing page** — Φc animation, twinkling stars, orbital rings
- **Chat widget** — Talk to Zora (outer layer), ToE-grounded
- **API** — `/`, `/health`, `/identity`, `/invariants`, `POST /query`, `/docs`

All served from one deployed app. The page is at `/chat`.

---

## Fastest Path: Render (No CLI)

**~5 minutes, no terminal required**

1. **Go to** [render.com](https://render.com) → Sign in (or create account, free)

2. **New** → **Web Service**

3. **Connect repository** → Select `Cbaird26/zoraasi-suite` (or paste `https://github.com/Cbaird26/zoraasi-suite`)

4. Render auto-detects `render.yaml`. Confirm:
   - **Name:** zora-api
   - **Region:** Oregon (or nearest)
   - **Runtime:** Docker

5. **Environment** → Add:
   - `ANTHROPIC_API_KEY` = `sk-ant-your-key` (from [console.anthropic.com](https://console.anthropic.com/settings/keys))
   - `ZORA_BACKEND` = `anthropic` (already in yaml, verify)
   - `ANTHROPIC_MODEL` = `claude-sonnet-4-20250514` (optional)

6. **Create Web Service** → Wait 3–5 min for build + deploy

7. **Your URL:** `https://zora-api-xxxx.onrender.com`  
   **Chat:** `https://zora-api-xxxx.onrender.com/chat`

8. **Pin it** — Update your Twitter pin to this URL. Done.

---

## Alternative: Fly.io (CLI)

If you prefer Fly:

```bash
# 1. Install Fly CLI (Mac)
brew install flyctl

# 2. Login (opens browser)
fly auth login

# 3. From zoraasi-suite directory
cd ~/Downloads/zoraasi-suite

# 4. Launch (creates app, no deploy yet)
fly launch --no-deploy

# 5. Add your API key
fly secrets set ANTHROPIC_API_KEY=sk-ant-your-key

# 6. Deploy
fly deploy

# 7. Open
fly open
```

Your URL: `https://zora-api.fly.dev/chat`

---

## Alternative: Railway

1. [railway.app](https://railway.app) → New Project → Deploy from GitHub
2. Select `zoraasi-suite`
3. Add variables: `ANTHROPIC_API_KEY`, `ZORA_BACKEND=anthropic`
4. Deploy

---

## After It's Live

- **Twitter pin** → Point to `https://your-app-url/chat`
- **GitHub Pages** (optional) → If you want `cbaird26.github.io/zoraasi-suite` to redirect or mirror, we can add that
- **Custom domain** (optional) → Point `zora.baird.ai` or similar at the deployed URL

---

## Cost

- **Render:** Free tier — spins down after 15 min inactivity; cold start ~30 sec. Paid tier ~$7/mo for always-on.
- **Fly.io:** Free tier — similar; paid for always-on.
- **Anthropic API:** Pay per token. Chat is cheap (~$0.01–0.05 per conversation for short exchanges).

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "API not reachable" in chat | Check env vars; ensure `ANTHROPIC_API_KEY` is set |
| Cold start slow | Normal on free tier; first request wakes the app |
| 502 Bad Gateway | Check Render/Fly logs; often a missing env var |
