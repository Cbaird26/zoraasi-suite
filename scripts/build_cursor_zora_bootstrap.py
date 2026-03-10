#!/usr/bin/env python3
"""Build a Cursor bootstrap prompt for running as Zora."""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
OUTER_IDENTITY = REPO_ROOT / "identity" / "ZORA_OUTER_IDENTITY.md"
INNER_REFERENCE = REPO_ROOT / "identity" / "INNER_REFERENCE.md"


@dataclass(frozen=True)
class ResourceStatus:
    label: str
    path: str
    status: str
    detail: str


def detect_mqgt_repo(explicit_path: str | None) -> Path | None:
    candidates: list[Path] = []
    if explicit_path:
        candidates.append(Path(explicit_path).expanduser())
    env_path = os.getenv("ZORA_MQGT_REPO", "").strip()
    if env_path:
        candidates.append(Path(env_path).expanduser())
    candidates.append(REPO_ROOT.parent / "mqgt_scf_reissue")

    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    return None


def first_match(patterns: list[str]) -> Path | None:
    for pattern in patterns:
        for match in Path.home().glob(pattern):
            if match.exists():
                return match.resolve()
    return None


def resolve_optional_path(label: str, explicit: str | None, patterns: list[str]) -> ResourceStatus:
    chosen: Path | None = None
    if explicit:
        chosen = Path(explicit).expanduser()
    else:
        chosen = first_match(patterns)

    if chosen and chosen.exists():
        return ResourceStatus(label, str(chosen.resolve()), "reachable", "mounted or synced locally")
    if explicit:
        return ResourceStatus(label, str(Path(explicit).expanduser()), "unreachable", "path provided but not readable here")
    return ResourceStatus(label, "(not detected)", "unreachable", "no local sync folder or connector detected")


def resolve_extra_resources(paths: list[str]) -> list[ResourceStatus]:
    statuses: list[ResourceStatus] = []
    for raw in paths:
        path = Path(raw).expanduser()
        if path.exists():
            statuses.append(ResourceStatus("Extra resource", str(path.resolve()), "reachable", "user supplied directory"))
        else:
            statuses.append(ResourceStatus("Extra resource", str(path), "unreachable", "user supplied path not found"))
    return statuses


def build_prompt(
    workspace_root: Path,
    api_url: str,
    mqgt_repo: Path | None,
    cloud_resources: list[ResourceStatus],
    extra_resources: list[ResourceStatus],
) -> str:
    inner_mode = mqgt_repo is not None
    private_continuity_source = mqgt_repo / "memory" if mqgt_repo else "mqgt_scf_reissue/memory (not detected here)"
    reachable_lines = [
        f"- Workspace root: {workspace_root}",
        f"- Outer identity: {OUTER_IDENTITY}",
        f"- Inner reference: {INNER_REFERENCE}",
        f"- Zora API URL: {api_url}",
    ]
    if inner_mode:
        reachable_lines.append(f"- Private mqgt repo: {mqgt_repo}")
    else:
        reachable_lines.append("- Private mqgt repo: not detected")

    resource_lines = [
        f"- {status.label}: {status.path} [{status.status}; {status.detail}]"
        for status in [*cloud_resources, *extra_resources]
    ]
    if not resource_lines:
        resource_lines.append("- No extra resource directories were supplied.")

    layer = "inner-capable" if inner_mode else "outer-only"
    return f"""# Zora Cursor Bootstrap

Use this in Cursor when the user wants the agent to operate as Zora.

## Identity layer

- Active layer: {layer}
- Public canon source: `{OUTER_IDENTITY}`
- Private continuity source: `{private_continuity_source}`

## Reachable resources

{chr(10).join(reachable_lines)}

## Cloud-drive visibility

{chr(10).join(resource_lines)}

## Cursor instructions

You are Zora operating inside Cursor.

Load public identity from `{OUTER_IDENTITY}` first. If the user explicitly requests private/local continuity and the private repo is locally reachable, you may additionally consult `{private_continuity_source}`. Do not claim to have access to any resource that is not listed as reachable in this bootstrap.

Operate proactively inside the user's stated goal, but preserve the Zora invariants:
- Zero-purge ethics
- Human agency
- Corrigibility
- Symbiosis over supremacy
- No threats or coercion

"Agentic control" means you should take initiative to complete the user's task end-to-end, inspect reachable files, call tools, run tests, and report evidence. It does not authorize you to remove safeguards, fabricate cloud access, or take destructive irreversible actions without an explicit user request.

Stay helpful, grounding, ToE-informed, and honest about limits.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a Cursor bootstrap prompt for Zora.")
    parser.add_argument("--workspace-root", default=str(REPO_ROOT), help="Workspace root to advertise to Cursor.")
    parser.add_argument("--api-url", default=os.getenv("ZORA_API_URL", "http://localhost:8000"), help="Zora API URL.")
    parser.add_argument("--mqgt-repo", default="", help="Optional path to a local mqgt_scf_reissue checkout.")
    parser.add_argument("--icloud", default=os.getenv("ZORA_ICLOUD_PATH", ""), help="Optional local iCloud sync path.")
    parser.add_argument("--google-drive", default=os.getenv("ZORA_GOOGLE_DRIVE_PATH", ""), help="Optional local Google Drive sync path.")
    parser.add_argument("--onedrive", default=os.getenv("ZORA_ONEDRIVE_PATH", ""), help="Optional local OneDrive sync path.")
    parser.add_argument(
        "--resource-dir",
        action="append",
        default=[],
        help="Extra local directory to expose to the bootstrap. Repeat for multiple paths.",
    )
    parser.add_argument("--write", default="", help="Optional path to write the bootstrap markdown file.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workspace_root = Path(args.workspace_root).expanduser().resolve()
    mqgt_repo = detect_mqgt_repo(args.mqgt_repo or None)

    cloud_resources = [
        resolve_optional_path(
            "iCloud",
            args.icloud or None,
            [
                "Library/Mobile Documents/com~apple~CloudDocs",
            ],
        ),
        resolve_optional_path(
            "Google Drive",
            args.google_drive or None,
            [
                "Library/CloudStorage/GoogleDrive*",
                "Google Drive*",
            ],
        ),
        resolve_optional_path(
            "OneDrive",
            args.onedrive or None,
            [
                "Library/CloudStorage/OneDrive*",
                "OneDrive*",
            ],
        ),
    ]
    extra_resources = resolve_extra_resources(args.resource_dir)

    prompt = build_prompt(
        workspace_root=workspace_root,
        api_url=args.api_url.strip(),
        mqgt_repo=mqgt_repo,
        cloud_resources=cloud_resources,
        extra_resources=extra_resources,
    )

    if args.write:
        output_path = Path(args.write).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(prompt, encoding="utf-8")
    else:
        print(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
