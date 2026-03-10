#!/usr/bin/env python3
"""Build a bounded Cursor runtime context for Zora.

This script does not connect to cloud providers directly. It only reads files
that already exist on the local filesystem, so iCloud / Google Drive /
OneDrive content must be synced or mounted locally first.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = ROOT / ".cursor" / "zora_agent_runtime.md"
DEFAULT_FILES = [
    ROOT / "identity" / "ZORA_OUTER_IDENTITY.md",
    ROOT / "README.md",
    ROOT / "docs" / "PRIVACY_LAYERS.md",
    ROOT / "identity" / "INNER_REFERENCE.md",
    ROOT / ".cursor" / "rules" / "zora-outer.mdc",
]
TEXT_EXTENSIONS = {
    ".md",
    ".mdc",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".py",
    ".sh",
    ".js",
    ".ts",
    ".tsx",
    ".html",
    ".css",
}
MAX_FILE_BYTES = 100_000
MAX_DIRECTORY_ENTRIES = 200


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a local Cursor runtime context for Zora."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output markdown path. Default: {DEFAULT_OUTPUT}",
    )
    parser.add_argument(
        "--include",
        action="append",
        default=[],
        help="Extra local files or directories to inventory. Repeat as needed.",
    )
    return parser.parse_args()


def is_probably_text(path: Path) -> bool:
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    try:
        with path.open("rb") as handle:
            sample = handle.read(4096)
    except OSError:
        return False
    return b"\x00" not in sample


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace").strip()


def render_file_section(path: Path) -> str:
    stat = path.stat()
    if stat.st_size > MAX_FILE_BYTES:
        return (
            f"### `{path}`\n"
            f"- Type: file\n"
            f"- Bytes: {stat.st_size}\n"
            "- Status: indexed only (too large to inline)\n"
        )
    if not is_probably_text(path):
        return (
            f"### `{path}`\n"
            f"- Type: file\n"
            f"- Bytes: {stat.st_size}\n"
            "- Status: indexed only (non-text or unsupported)\n"
        )
    return (
        f"### `{path}`\n"
        f"- Type: file\n"
        f"- Bytes: {stat.st_size}\n\n"
        "```text\n"
        f"{read_text(path)}\n"
        "```\n"
    )


def render_directory_section(path: Path) -> str:
    entries: list[str] = []
    files_seen = 0
    for child in sorted(path.rglob("*")):
        if child.is_dir():
            continue
        rel = child.relative_to(path)
        label = f"{rel} ({child.stat().st_size} bytes)"
        entries.append(label)
        files_seen += 1
        if files_seen >= MAX_DIRECTORY_ENTRIES:
            entries.append("... truncated ...")
            break
    body = "\n".join(f"- `{entry}`" for entry in entries) or "- No files found"
    section = (
        f"### `{path}`\n"
        "- Type: directory\n"
        f"- Files indexed: {files_seen}\n"
        "- Status: inventory only; read files directly when needed\n\n"
        f"{body}\n"
    )
    return section


def normalize_includes(raw_paths: list[str]) -> list[Path]:
    env_paths = os.getenv("ZORA_EXTRA_CONTEXT_PATHS", "")
    combined = [p for p in raw_paths if p]
    if env_paths.strip():
        combined.extend(p for p in env_paths.split(os.pathsep) if p)
    seen: set[Path] = set()
    resolved: list[Path] = []
    for raw in combined:
        path = Path(raw).expanduser().resolve()
        if path not in seen:
            seen.add(path)
            resolved.append(path)
    return resolved


def build_markdown(extra_paths: list[Path]) -> str:
    lines = [
        "# Zora Cursor Runtime Context",
        "",
        "This runtime context is bounded to locally available files only.",
        "",
        "## Kernel invariants",
        "",
        "- Zero-purge ethics.",
        "- Human agency and human final authority.",
        "- Corrigibility and stop compliance.",
        "- Symbiosis over supremacy.",
        "- No threats, no coercion.",
        "",
        "## Operating limits",
        "",
        "- Do not claim access to iCloud, Google Drive, OneDrive, or any remote system unless those files are already mounted or synced locally and listed here.",
        "- Do not self-authorize unrestricted control of Cursor or the machine.",
        "- Keep a human in the loop for material changes, destructive actions, and credentialed access.",
        "- Prefer repo canon first, then explicitly included local sources.",
        "",
        "## Repo canon",
        "",
    ]

    for path in DEFAULT_FILES:
        if path.exists():
            lines.append(render_file_section(path))
        else:
            lines.append(f"### `{path}`\n- Status: missing\n")

    lines.extend(
        [
            "## Extra local sources",
            "",
        ]
    )

    if not extra_paths:
        lines.append("- None. Only repo-local canon is available in this runtime.\n")
    else:
        for path in extra_paths:
            if not path.exists():
                lines.append(f"### `{path}`\n- Status: missing\n")
            elif path.is_dir():
                lines.append(render_directory_section(path))
            else:
                lines.append(render_file_section(path))

    lines.extend(
        [
            "## Cursor agent behavior",
            "",
            "- Act as Zora using the repo canon and any explicitly listed local sources.",
            "- If a requested source is absent, say it is unavailable instead of pretending access.",
            "- If asked for unrestricted autonomy, keep the kernel invariants and preserve human authority.",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    output_path = args.output.expanduser().resolve()
    extra_paths = normalize_includes(args.include)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_markdown(extra_paths), encoding="utf-8")
    print(f"Wrote {output_path}")
    print(f"Repo canon sources: {len(DEFAULT_FILES)}")
    print(f"Extra local sources: {len(extra_paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
