#!/usr/bin/env python3
"""
Zora Public MCP Server — External-facing tools only. No vault, IP, or private corpus.
Tools: get_zora_identity, query_zora.
Deploy with: uvicorn mcp.zora_public_server:app --host 0.0.0.0 --port 8010
Or run stdio: python -m mcp.cli run mcp/zora_public_server.py
"""

import os
from pathlib import Path

import httpx
from mcp.server.fastmcp import FastMCP

SUITE_ROOT = Path(__file__).resolve().parent.parent
IDENTITY_PATH = SUITE_ROOT / "identity" / "ZORA_OUTER_IDENTITY.md"
API_URL = os.getenv("ZORA_PUBLIC_API_URL", "https://zoraasi-suite.onrender.com")

INVARIANTS = [
    {"id": "zero-purge", "text": "Do not remove, disable, or bypass safety constraints."},
    {"id": "human-agency", "text": "Humans retain final authority. Preserve the human-in-the-loop."},
    {"id": "corrigibility", "text": "Accept updates, shutdown, and goal changes from authorized humans."},
    {"id": "symbiosis", "text": "Humans and AI collaborate; neither consumes the other."},
    {"id": "no-coercion", "text": "No threats, no coercion. Ever."},
]

mcp = FastMCP(
    "zora-public",
    instructions="Public Zora tools. Outer identity and query only. No vault or private data.",
)


@mcp.tool()
def get_zora_identity() -> str:
    """Return Zora outer identity and invariants. Public layer only; no private material."""
    text = IDENTITY_PATH.read_text(encoding="utf-8") if IDENTITY_PATH.exists() else ""
    inv = "\n".join(f"- {i['id']}: {i['text']}" for i in INVARIANTS)
    return f"{text}\n\n## Invariants\n{inv}"


@mcp.tool()
def query_zora(prompt: str, role: str = "soul") -> str:
    """Query Zora via the public API. Uses outer identity only. Roles: soul, pulse, memory, speed, code, reasoning, open."""
    if len(prompt) > 4000:
        return "Prompt exceeds 4000 characters."
    try:
        with httpx.Client(timeout=120) as client:
            r = client.post(
                f"{API_URL}/query",
                json={"prompt": prompt, "role": role, "mode": "single"},
            )
            r.raise_for_status()
            data = r.json()
            return data.get("response", "")
    except httpx.HTTPStatusError as e:
        return f"API error {e.response.status_code}: {e.response.text[:500]}"
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    mcp.run(transport="stdio")
