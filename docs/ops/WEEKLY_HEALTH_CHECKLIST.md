# Weekly 5-Minute Health Checklist

Run once per week to keep local/GitHub/Render aligned.

## 1) Git baseline checks

```bash
git fetch origin --tags
git status --short --branch
git log --oneline -1
```

Verify local `main` and `origin/main` are aligned (or intentionally diverged).

## 2) Render health checks

```bash
curl -sS https://zoraasi-suite.onrender.com/health
curl -s -o /dev/null -w "%{http_code}\n" https://zoraasi-suite.onrender.com/chat
```

Expect status `ok` and HTTP `200`.

## 3) Local health checks

```bash
./scripts/run_api.sh
```

In another shell:

```bash
curl -sS http://localhost:8000/health
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/chat
```

## 4) Functional smoke (single/router/consensus)

```bash
curl -sS -X POST https://zoraasi-suite.onrender.com/query \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Reply with READY","mode":"single","role":"soul"}'
```

```bash
curl -sS -X POST https://zoraasi-suite.onrender.com/query \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Summarize in one line.","mode":"router"}'
```

```bash
curl -sS -X POST https://zoraasi-suite.onrender.com/query \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Give three bullets on stability priorities.","mode":"consensus"}'
```

## 5) Rollback readiness

- Confirm freeze tag exists:
  - `git tag | rg zorel-polish-freeze`
- Confirm rollback doc exists:
  - `docs/ops/ROLLBACK.md`

