#!/usr/bin/env python3
"""Generate a preservation-first corpus scaffold from existing repo trackers."""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ARCHIVE_DIR = ROOT / "docs" / "archive"
WAVE2_TRACKER = ROOT / "docs" / "ops" / "CB26_WAVE2_PUBLIC_TRACKER.md"
WAVE3_TRACKER = ROOT / "docs" / "ops" / "CB26_WAVE3_ARCHIVE_TRACKER.md"
INNER_REFERENCE = ROOT / "identity" / "INNER_REFERENCE.md"
MANIFEST_PATH = ARCHIVE_DIR / "corpus_manifest.json"
INDEX_PATH = ARCHIVE_DIR / "CORPUS_INDEX.md"
CHRONOLOGY_PATH = ARCHIVE_DIR / "CORPUS_CHRONOLOGY.md"

TRACKER_ROW_RE = re.compile(
    r"^\|\s*\[(?P<title>[^\]]+)\]\((?P<url>[^)]+)\)\s*\|\s*"
    r"(?P<current>[^|]+)\|\s*(?P<target>[^|]+)\|\s*(?P<control>[^|]+)\|\s*"
    r"(?P<freeze>[^|]+)\|\s*(?P<status>[^|]+)\|$"
)
INNER_ROW_RE = re.compile(r"^- \*\*(?P<title>.+?)\*\* — (?P<notes>.+)$")
YEAR_RE = re.compile(r"(?<!\d)(?:19|20)\d{2}(?!\d)")
INTERFACE_OVERRIDES = {
    "zora-toe-public-kit",
    "holocron-public-export",
    "baird-telehealth-site",
    "mqgt-documentation-site",
}


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def infer_date(title: str) -> tuple[str, str | None, str]:
    match = YEAR_RE.search(title)
    if match:
        year = match.group(0)
        return f"{year} (inferred from title)", f"{year}-01-01", "inferred_from_title"
    return "undated", None, "unknown"


def edition_targets_for_layer(layer: str) -> list[str]:
    if layer == "public_interface":
        return ["pull_page_full_reading", "chronological_full"]
    return [
        "pull_page_full_reading",
        "chronological_full",
        "paper_reconstruction",
        "clean_editorial",
    ]


def classify_wave2_layer(title: str) -> str:
    if title in INTERFACE_OVERRIDES:
        return "public_interface"
    return "public_science"


def tracker_record(
    title: str,
    url: str,
    status: str,
    layer: str,
    boundary: str,
    tracker_path: Path,
) -> dict:
    date_label, date_sort, certainty = infer_date(title)
    return {
        "id": slugify(title),
        "title": title,
        "record_type": "repo_collection",
        "corpus_layer": layer,
        "visibility": "public",
        "source_kind": "github_repo",
        "canonical_location": url,
        "tracker_status": status.strip(),
        "ingest_status": "collection_only",
        "execution_boundary": boundary,
        "date_label": date_label,
        "date_sort": date_sort,
        "date_certainty": certainty,
        "edition_targets": edition_targets_for_layer(layer),
        "notes": (
            "Seeded from tracker metadata only. Expand to document-level entries after "
            "repo contents are ingested into the working corpus."
        ),
        "provenance": {
            "source_file": str(tracker_path.relative_to(ROOT)),
            "source_type": "tracker_table",
        },
    }


def parse_tracker(path: Path, layer: str, boundary: str) -> list[dict]:
    records: list[dict] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = TRACKER_ROW_RE.match(raw_line.strip())
        if not match:
            continue
        resolved_layer = classify_wave2_layer(match.group("title")) if path == WAVE2_TRACKER else layer
        records.append(
            tracker_record(
                title=match.group("title"),
                url=match.group("url"),
                status=match.group("status"),
                layer=resolved_layer,
                boundary=boundary,
                tracker_path=path,
            )
        )
    return records


def parse_inner_reference(path: Path) -> list[dict]:
    records: list[dict] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = INNER_ROW_RE.match(raw_line.strip())
        if not match:
            continue
        title = match.group("title")
        date_label, date_sort, certainty = infer_date(title)
        records.append(
            {
                "id": slugify(title),
                "title": title,
                "record_type": "private_pointer",
                "corpus_layer": "private_sealed",
                "visibility": "private",
                "source_kind": "private_path_pointer",
                "canonical_location": title,
                "tracker_status": "reference_only",
                "ingest_status": "private_workspace_only",
                "execution_boundary": "private_workspace_only",
                "date_label": date_label,
                "date_sort": date_sort,
                "date_certainty": certainty,
                "edition_targets": [
                    "pull_page_full_reading",
                    "chronological_full",
                    "paper_reconstruction",
                    "clean_editorial",
                ],
                "notes": match.group("notes"),
                "provenance": {
                    "source_file": str(path.relative_to(ROOT)),
                    "source_type": "private_pointer_list",
                },
            }
        )
    return records


def sort_records(records: list[dict]) -> list[dict]:
    def sort_key(record: dict) -> tuple[str, str]:
        date_sort = record["date_sort"] or "9999-12-31"
        return (date_sort, record["title"].lower())

    return sorted(records, key=sort_key)


def write_manifest(records: list[dict], generated_utc: str) -> None:
    payload = {
        "schema_version": 1,
        "generated_utc": generated_utc,
        "description": (
            "Collection-level preservation-first corpus scaffold. "
            "Replace or extend repo-level records with document-level entries as "
            "sources are ingested."
        ),
        "records": records,
    }
    MANIFEST_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_index(records: list[dict], generated_utc: str) -> None:
    total = len(records)
    public_records = sum(1 for record in records if record["visibility"] == "public")
    private_records = total - public_records
    lines: list[str] = []
    lines.append("# Corpus Index")
    lines.append("")
    lines.append("Generated from tracker metadata and private pointers.")
    lines.append("")
    lines.append(f"Generated UTC: `{generated_utc}`")
    lines.append("")
    lines.append("## Purpose")
    lines.append("")
    lines.append(
        "This index is the preservation-first bridge between repo-level governance and "
        "the future document-level codex."
    )
    lines.append("")
    lines.append("## Totals")
    lines.append("")
    lines.append(f"- Total records: **{total}**")
    lines.append(f"- Public collection records: **{public_records}**")
    lines.append(f"- Private pointer records: **{private_records}**")
    lines.append("")
    lines.append("## Edition Targets")
    lines.append("")
    lines.append("- `pull_page_full_reading`: full page-faithful reading copy with light cleanup only.")
    lines.append("- `chronological_full`: same corpus arranged by date, preserving provenance.")
    lines.append("- `paper_reconstruction`: one coherent source document per scientific paper.")
    lines.append("- `clean_editorial`: later reduction and consistency pass after provenance is locked.")
    lines.append("")
    lines.append("## Records")
    lines.append("")
    lines.append(
        "| ID | Title | Type | Layer | Date | Boundary | Status | Canonical location |"
    )
    lines.append("|---|---|---|---|---|---|---|---|")
    for record in records:
        lines.append(
            f"| `{record['id']}` | {record['title']} | {record['record_type']} | "
            f"{record['corpus_layer']} | {record['date_label']} | "
            f"{record['execution_boundary']} | {record['ingest_status']} | "
            f"`{record['canonical_location']}` |"
        )
    lines.append("")
    lines.append("## Next Step")
    lines.append("")
    lines.append(
        "Expand each repo-level collection into document-level entries before starting "
        "10-page chunk analysis."
    )
    INDEX_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_chronology(records: list[dict], generated_utc: str) -> None:
    grouped: dict[str, list[dict]] = {}
    for record in records:
        key = record["date_sort"][:4] if record["date_sort"] else "Undated"
        grouped.setdefault(key, []).append(record)

    lines: list[str] = []
    lines.append("# Corpus Chronology")
    lines.append("")
    lines.append("Chronological reading aid generated from current metadata.")
    lines.append("")
    lines.append(f"Generated UTC: `{generated_utc}`")
    lines.append("")
    lines.append(
        "Dates inferred from titles are explicitly labeled; all unknown dates remain grouped as undated."
    )
    for key in sorted(grouped.keys(), key=lambda item: (item == "Undated", item)):
        lines.append("")
        lines.append(f"## {key}")
        lines.append("")
        for record in sorted(grouped[key], key=lambda item: item["title"].lower()):
            lines.append(
                f"- `{record['id']}` — {record['title']} "
                f"({record['date_label']}; {record['corpus_layer']})"
            )
    CHRONOLOGY_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    generated_utc = dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )
    records = []
    records.extend(parse_tracker(WAVE2_TRACKER, "public_science", "public_repo_safe"))
    records.extend(parse_tracker(WAVE3_TRACKER, "archive_freeze", "public_repo_safe"))
    records.extend(parse_inner_reference(INNER_REFERENCE))
    sorted_records = sort_records(records)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    write_manifest(sorted_records, generated_utc)
    write_index(sorted_records, generated_utc)
    write_chronology(sorted_records, generated_utc)
    print(f"Generated corpus scaffold for {len(sorted_records)} records.")


if __name__ == "__main__":
    main()
