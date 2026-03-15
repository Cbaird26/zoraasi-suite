# API Error Responses

**Zor-El API v0.3.0+** — Structured error format for clients.

---

## Format

All error responses use a consistent JSON structure:

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "detail": null | object | array
  }
}
```

---

## Error Codes by Endpoint

### POST /query

| HTTP | code | message | When |
|------|------|---------|------|
| 422 | `validation_error` | Request validation failed | Invalid body (e.g. empty prompt, prompt > 4000 chars) |
| 400 | `Unknown role` | ... | Invalid `role` parameter |
| 502 | `http_error` | Backend returned {status} | OpenRouter/Anthropic returned error |
| 503 | `No API keys configured` | ... | OPENROUTER_API_KEY and ANTHROPIC_API_KEY missing |
| 503 | `Backend not reachable` | ... | Network/connection failure |
| 504 | `Inference timed out` | ... | Request took > 120s |
| 429 | (SlowAPI) | Rate limit exceeded | > 60 requests/minute on /query |

### POST /auth/login, /auth/refresh

| HTTP | code | message |
|------|------|---------|
| 422 | `validation_error` | Missing or invalid username/password |
| 401 | `Invalid credentials` | Wrong login |
| 401 | `Invalid or expired refresh token` | Bad refresh token |

### GET /chat

| HTTP | code | message |
|------|------|---------|
| 404 | `Chat UI not found.` | site/index.html missing |

---

## Example: Validation Error (422)

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed",
    "detail": [
      {
        "loc": ["body", "prompt"],
        "msg": "field required",
        "type": "value_error.missing"
      }
    ]
  }
}
```

---

## Example: Backend Unavailable (503)

```json
{
  "error": {
    "code": "Backend not reachable",
    "message": "Backend not reachable",
    "detail": null
  }
}
```

---

## Client Handling

1. Check `response.status_code`.
2. Parse `response.json()` and read `error.code` for programmatic handling.
3. Use `error.message` for user-facing text.
4. Use `error.detail` for validation details (422) or debug info.
