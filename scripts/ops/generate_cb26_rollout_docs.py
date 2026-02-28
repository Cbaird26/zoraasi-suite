#!/usr/bin/env python3
"""Generate cbaird26 all-repo rollout docs from live GitHub inventory."""

from __future__ import annotations

import datetime as dt
import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OPS_DIR = ROOT / "docs" / "ops"


def run_json(cmd: list[str]) -> list[dict]:
    out = subprocess.check_output(cmd, text=True)
    return json.loads(out)


def classify(repo: dict) -> tuple[str, str, str]:
    """Return (category, target_visibility, wave)."""
    name = (repo.get("name") or "").lower()
    desc = (repo.get("description") or "").lower()
    text = f"{name} {desc}"

    runtime_overrides = {
        "zoraasi-suite",
        "unified-agent-platform",
        "local-asi",
        "dark-knight",
        "zoraapi",
        "toe-studio",
        "studio-hub",
    }
    science_overrides = {
        "mqgt-scf-stripped-core",
        "toe-empirical-validation",
        "toe-2026-updates",
        "mqgt-papers",
        "mqgt-scf-thesis",
        "a-theory-of-everything",
        "a-theory-of-everything-revised",
        "theory-of-everything",
        "toe",
        "a-theory-of-everything---baird-et-al-2025-.pdf",
    }
    interface_overrides = {
        "zora-toe-public-kit",
        "holocron-public-export",
        "baird-telehealth-site",
        "mqgt-documentation-site",
    }

    if name in runtime_overrides:
        return "Private Runtime", "Private", "Wave 1"
    if name in science_overrides:
        return "Public Science", "Public", "Wave 2"
    if name in interface_overrides:
        return "Public Interface", "Public", "Wave 2"

    if any(k in text for k in ["api", "agent", "ops", "dashboard", "cli", "ingest", "studio", "router"]):
        return "Private Runtime", "Private", "Wave 1"
    if any(k in text for k in ["paper", "thesis", "theory", "toe", "validation", "preregistration", "figure", "data-public"]):
        return "Public Science", "Public", "Wave 2"
    if any(k in text for k in ["site", "public", "export"]):
        return "Public Interface", "Public", "Wave 2"

    return "Archive/Freeze", "Public->Archive", "Wave 3"


def write_matrix(repos: list[dict], rows: list[dict]) -> None:
    now = dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    counts = Counter(r["category"] for r in rows)
    private_now = sum(1 for r in repos if r.get("isPrivate"))
    public_now = len(repos) - private_now

    lines: list[str] = []
    lines.append("# cbaird26 Repo Classification Matrix")
    lines.append("")
    lines.append(f"Generated UTC: `{now}`")
    lines.append("")
    lines.append("Classification policy:")
    lines.append("- `Private Runtime`: orchestration, backend, prompts, runtime controls, deployment ops.")
    lines.append("- `Public Science`: papers, reproducibility artifacts, and scientific evidence packets.")
    lines.append("- `Public Interface`: safe front-door static surfaces and public comms assets.")
    lines.append("- `Archive/Freeze`: legacy or low-activity repos shifted to archival posture.")
    lines.append("")
    lines.append("| Repo | Current | Category | Target Visibility | Wave | Status | Updated |")
    lines.append("|---|---:|---|---|---|---|---|")

    for r in rows:
        lines.append(
            f"| [{r['name']}]({r['url']}) | {r['current']} | {r['category']} | "
            f"{r['target']} | {r['wave']} | {r['status']} | {r['updated']} |"
        )

    lines.append("")
    lines.append("## Totals")
    lines.append(f"- Total repos inventoried: **{len(rows)}**")
    lines.append(f"- Currently public: **{public_now}**")
    lines.append(f"- Currently private: **{private_now}**")
    lines.append(f"- Private Runtime: **{counts['Private Runtime']}**")
    lines.append(f"- Public Science: **{counts['Public Science']}**")
    lines.append(f"- Public Interface: **{counts['Public Interface']}**")
    lines.append(f"- Archive/Freeze: **{counts['Archive/Freeze']}**")

    (OPS_DIR / "CB26_REPO_CLASSIFICATION_MATRIX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_wave_tracker(rows: list[dict], wave: str, filename: str, description: str) -> None:
    selected = [r for r in rows if r["wave"] == wave]
    lines: list[str] = []
    lines.append(f"# {wave} Tracker")
    lines.append("")
    lines.append(description)
    lines.append("")
    lines.append("| Repo | Current | Target | Control Pack | Freeze/Rollback | Status |")
    lines.append("|---|---:|---|---|---|---|")
    for r in selected:
        lines.append(
            f"| [{r['name']}]({r['url']}) | {r['current']} | {r['target']} | ready | required | {r['status']} |"
        )
    lines.append("")
    lines.append(f"- Total repos in {wave}: **{len(selected)}**")
    (OPS_DIR / filename).write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_final_report(rows: list[dict]) -> None:
    now = dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    by_wave = Counter(r["wave"] for r in rows)
    lines: list[str] = []
    lines.append("# cbaird26 Hybrid Migration Completion Report")
    lines.append("")
    lines.append(f"Report UTC: `{now}`")
    lines.append("")
    lines.append("## Scope")
    lines.append("- Master rollout framework implemented for all inventoried repositories in the account.")
    lines.append("- Inventory, wave trackers, guardrail automation script, and execution playbooks are now in place.")
    lines.append("")
    lines.append("## Inventory Snapshot")
    lines.append(f"- Total repos covered: **{len(rows)}**")
    lines.append(f"- Wave 1 (Private Runtime): **{by_wave['Wave 1']}**")
    lines.append(f"- Wave 2 (Public Science + Interface): **{by_wave['Wave 2']}**")
    lines.append(f"- Wave 3 (Archive/Freeze): **{by_wave['Wave 3']}**")
    lines.append("")
    lines.append("## Deliverables Completed")
    lines.append("- `CB26_REPO_CLASSIFICATION_MATRIX.md` refreshed from live GitHub inventory.")
    lines.append("- `CB26_WAVE1_RUNTIME_TRACKER.md`, `CB26_WAVE2_PUBLIC_TRACKER.md`, `CB26_WAVE3_ARCHIVE_TRACKER.md` generated.")
    lines.append("- Guardrail execution tooling and policy references prepared for account-wide enforcement.")
    lines.append("- Final completion report published with residual-risk callouts.")
    lines.append("")
    lines.append("## Residual Risks")
    lines.append("- Existing public forks/clones outside account control remain unaffected by visibility changes.")
    lines.append("- Cross-repo branch protection must be applied via org/repo admin privileges and verified after rollout.")
    lines.append("- Service-level cutovers require per-runtime smoke validation before public traffic switch.")
    lines.append("")
    lines.append("## Next Immediate Action")
    lines.append("- Execute Wave 1 runtime repos first using freeze+rollback controls before any account-wide visibility flips.")

    (OPS_DIR / "CB26_MIGRATION_COMPLETION_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    repos = run_json(
        [
            "gh",
            "repo",
            "list",
            "Cbaird26",
            "--limit",
            "250",
            "--json",
            "name,isPrivate,updatedAt,url,description,primaryLanguage",
        ]
    )
    repos.sort(key=lambda r: ((r.get("updatedAt") or ""), (r.get("name") or "")), reverse=True)

    rows: list[dict] = []
    for repo in repos:
        category, target, wave = classify(repo)
        rows.append(
            {
                "name": repo["name"],
                "url": repo["url"],
                "current": "Private" if repo.get("isPrivate") else "Public",
                "category": category,
                "target": target,
                "wave": wave,
                "status": "planned",
                "updated": (repo.get("updatedAt") or "")[:10],
            }
        )

    write_matrix(repos, rows)
    write_wave_tracker(
        rows,
        "Wave 1",
        "CB26_WAVE1_RUNTIME_TRACKER.md",
        "Runtime repos targeted for private migration controls, freeze baselines, and rollback proof.",
    )
    write_wave_tracker(
        rows,
        "Wave 2",
        "CB26_WAVE2_PUBLIC_TRACKER.md",
        "Public science/interface repos targeted for boundary hardening while preserving public visibility.",
    )
    write_wave_tracker(
        rows,
        "Wave 3",
        "CB26_WAVE3_ARCHIVE_TRACKER.md",
        "Legacy archive repos targeted for read-only posture and canonical pointer updates.",
    )
    write_final_report(rows)
    print(f"Generated rollout docs for {len(rows)} repositories.")


if __name__ == "__main__":
    main()
