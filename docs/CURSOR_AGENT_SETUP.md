# Cursor Agent Setup for Zora

This repo can instantiate the public Zora layer inside Cursor using the canon that is actually present here.

## What this setup does

- Loads the public Zora identity from `identity/ZORA_OUTER_IDENTITY.md`
- Applies a Cursor rule from `.cursor/rules/zora-cursor-agent.mdc`
- Optionally records extra local resource roots in `.cursor/zora_accessible_resources.md`
- Keeps human-in-the-loop safeguards intact

## What this setup does not do

- It does not pull directly from iCloud, Google Drive, or OneDrive APIs
- It does not expose private inner-memory files that are not mounted on this machine
- It does not grant unrestricted autonomous control

Those limits are intentional. The public Zora canon in this repo preserves human agency and corrigibility.

## Bootstrap

1. Sync or mount any extra local folders first. If a cloud drive is not visible as a local path, Cursor cannot use it.
2. Generate the local resource manifest:

   `./scripts/bootstrap_cursor_zora.sh /absolute/path/to/local/folder`

   Or:

   `ZORA_RESOURCE_PATHS=/abs/path/one:/abs/path/two ./scripts/bootstrap_cursor_zora.sh`

3. Start the local API:

   `./scripts/run_api.sh`

4. In Cursor, ask for Zora in public context. The agent rule will point the session at the public identity and any reachable local resources listed in `.cursor/zora_accessible_resources.md`.

## Inner / full continuity

Full Cursor continuity requires the separate private `mqgt_scf_reissue` workspace and its `memory/` content, as referenced by `identity/INNER_REFERENCE.md`. That material is not in this repo and cannot be reconstructed from the public suite alone.
