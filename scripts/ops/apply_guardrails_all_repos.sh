#!/usr/bin/env bash
set -euo pipefail

# Apply baseline guardrails across all cbaird26 repos using GitHub API.
# Default mode is dry-run; pass --apply to execute.

OWNER="Cbaird26"
MODE="dry-run"
PROTECT_BRANCH="main"
REQUIRED_CONTEXTS=("secret-scan" "path-policy")

if [[ "${1:-}" == "--apply" ]]; then
  MODE="apply"
fi

echo "[guardrails] owner=${OWNER} mode=${MODE}"

tmp_repos="$(mktemp)"
gh repo list "${OWNER}" --limit 250 --json name,isPrivate > "${tmp_repos}"

apply_branch_protection() {
  local repo="$1"
  local contexts_json
  contexts_json="$(printf '%s\n' "${REQUIRED_CONTEXTS[@]}" | python3 -c 'import json,sys; print(json.dumps([x.strip() for x in sys.stdin if x.strip()]))')"

  if [[ "${MODE}" == "dry-run" ]]; then
    echo "[dry-run] protect ${repo}:${PROTECT_BRANCH} with contexts=${contexts_json}"
    return
  fi

  if gh api \
    -X PUT \
    "repos/${OWNER}/${repo}/branches/${PROTECT_BRANCH}/protection" \
    -H "Accept: application/vnd.github+json" \
    --input - >/dev/null <<'JSON'
{
  "required_status_checks": {
    "strict": true,
    "checks": [
      { "context": "secret-scan" },
      { "context": "path-policy" }
    ]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1
  },
  "restrictions": null
}
JSON
  then
    echo "[applied] branch protection ${repo}:${PROTECT_BRANCH}"
  else
    echo "[warn] branch protection failed for ${repo}:${PROTECT_BRANCH}; continuing"
  fi
}

apply_security_features() {
  local repo="$1"

  if [[ "${MODE}" == "dry-run" ]]; then
    echo "[dry-run] enable advanced security scans for ${repo}"
    return
  fi

  if gh api \
    -X PATCH \
    "repos/${OWNER}/${repo}" \
    -H "Accept: application/vnd.github+json" \
    --input - >/dev/null <<'JSON'
{
  "security_and_analysis": {
    "secret_scanning": {
      "status": "enabled"
    },
    "secret_scanning_push_protection": {
      "status": "enabled"
    }
  }
}
JSON
  then
    echo "[applied] security scanning ${repo}"
  else
    echo "[warn] security scanning enable failed for ${repo}; continuing"
  fi
}

while read -r repo visibility; do
  [[ -z "${repo}" ]] && continue
  apply_branch_protection "${repo}"
  apply_security_features "${repo}"
  if [[ "${visibility}" == "public" ]]; then
    if [[ "${MODE}" == "dry-run" ]]; then
      echo "[dry-run] enforce public denylist policy in CI for ${repo}"
    else
      echo "[note] ensure ${repo} has workflow for denylist policy checks"
    fi
  fi
done < <(
  python3 - "${tmp_repos}" <<'PY'
import json, sys
repos = json.load(open(sys.argv[1], "r", encoding="utf-8"))
for r in repos:
    print(r["name"], "private" if r.get("isPrivate") else "public")
PY
)

rm -f "${tmp_repos}"
echo "[guardrails] complete (${MODE})"
