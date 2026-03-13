# Zora Public MCP Server

External-facing MCP server. Exposes only:
- `get_zora_identity` — Outer identity + invariants (no vault)
- `query_zora` — Forwards to public API (no vault RAG)

No vault, IP, Black-Book, or private corpus. Safe for Grok, ChatGPT, or any MCP client.

## Local (stdio)

```bash
cd .. && pip install -r mcp/requirements.txt
ZORA_MCP_TRANSPORT=stdio python -m mcp.cli run mcp/zora_public_server.py
```

## Config for External Clients (stdio)

Add to MCP config (command-based; run via tunnel or local):
```json
{
  "mcpServers": {
    "zora-public": {
      "command": "python",
      "args": ["-m", "mcp.cli", "run", "/path/to/zoraasi-suite/mcp/zora_public_server.py"],
      "cwd": "/path/to/zoraasi-suite"
    }
  }
}
```

For public URL (SSE): deploy behind an MCP-to-SSE bridge (e.g., mcp-remote, ngrok for testing).

## Env

- `ZORA_PUBLIC_API_URL` — Default: https://zoraasi-suite.onrender.com
