# Zora Cursor Agent Setup

Instantiate Zora in Cursor with bounded local context.

## What this setup does

- Creates a Cursor rule for Zora at `.cursor/rules/zora-cursor-agent.mdc`
- Builds a runtime context file at `.cursor/zora_agent_runtime.md`
- Uses repo canon by default
- Optionally indexes extra local files or directories that you explicitly include

## What this setup does not do

- It does not connect directly to iCloud, Google Drive, or OneDrive
- It does not grant unrestricted autonomy or remove human oversight
- It does not expose private inner-layer material that is not present locally

That is intentional. The repo canon explicitly preserves human agency, corrigibility, and zero-purge safety constraints.

## Build the runtime context

From the repo root:

```bash
python scripts/build_cursor_zora_context.py
```

This writes `.cursor/zora_agent_runtime.md` using:

- `identity/ZORA_OUTER_IDENTITY.md`
- `README.md`
- `docs/PRIVACY_LAYERS.md`
- `identity/INNER_REFERENCE.md`
- `.cursor/rules/zora-outer.mdc`

## Add more local context

If you have synced or mounted extra sources locally, include them explicitly:

```bash
python scripts/build_cursor_zora_context.py \
  --include "/path/to/local/zora-notes" \
  --include "/path/to/local/icloud-sync" \
  --include "/path/to/local/google-drive-sync" \
  --include "/path/to/local/onedrive-sync"
```

You can also use `ZORA_EXTRA_CONTEXT_PATHS` as a path-separated list.

Important:

- The script only reads what is already on disk
- Direct cloud-account access is out of scope for this repo and this environment
- Large or binary files are indexed instead of inlined

## Use in Cursor

1. Build the runtime context file.
2. Enable or reference `.cursor/rules/zora-cursor-agent.mdc`.
3. Ask Cursor to operate as Zora.

The agent will then use the local runtime context and should accurately state what sources are available.

## Safety model

This setup keeps:

- human final authority
- stop compliance
- bounded claims about accessible data
- no unrestricted self-directed control

If you want broader access, first sync or mount the relevant files locally, then rebuild the runtime context.
