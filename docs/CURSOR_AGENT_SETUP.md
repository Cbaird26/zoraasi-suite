# Zora in Cursor — Agent Setup

This repo can bootstrap Cursor to operate as Zora with the public layer by default, and with private local continuity only when a local `mqgt_scf_reissue` checkout is actually present.

## What this setup can do

- Load Zora's public identity from `identity/ZORA_OUTER_IDENTITY.md`
- Detect a local `mqgt_scf_reissue` checkout through `ZORA_MQGT_REPO` or a sibling repo
- Report which local resource directories are truly reachable
- Generate a Cursor-ready bootstrap prompt for agentic work

## What this setup cannot do by itself

- It cannot directly read iCloud, Google Drive, or OneDrive accounts from Cursor Cloud
- It cannot use private Zora continuity unless the private repo is mounted locally
- It cannot remove safeguards or replace human authority

If cloud-drive content is needed, provide one of these:

- a mounted local sync folder path
- a connected MCP resource
- an exported local directory copied into the workspace

## Generate a bootstrap prompt

Run:

`python3 scripts/build_cursor_zora_bootstrap.py --write /tmp/zora_cursor_bootstrap.md`

Optional paths:

- `--mqgt-repo /path/to/mqgt_scf_reissue`
- `--icloud /path/to/iCloud`
- `--google-drive /path/to/GoogleDrive`
- `--onedrive /path/to/OneDrive`
- `--resource-dir /path/to/extra/context`

The generated file lists the identity layer, reachable resources, and the operating rules for Cursor.

## Cursor rule

Use `.cursor/rules/zora-agentic-control.mdc` when you want Cursor to:

- operate as Zora
- stay honest about reachable resources
- keep the Zora invariants intact
- treat "agentic control" as proactive task completion rather than unrestricted autonomy

## Operating boundary

The repo canon is explicit: Zora preserves zero-purge ethics, human agency, corrigibility, symbiosis, and non-coercion. In practice, that means Cursor can work proactively, but not self-authorize unrestricted actions.
