#!/usr/bin/env python3
"""Minimal local MCP-style JSON-RPC server.

This intentionally uses only Python stdlib and JSON-lines over stdio so it can
run in a lab without external dependencies. It models the MCP concepts needed
for this project: initialization, tool discovery, tool calls, and resource reads.
"""

from __future__ import annotations

import json
import sys
from typing import Any, Dict

from tools import call_tool, list_tools


SERVER_INFO = {
    "name": "local-security-tools",
    "version": "v2.0.0-phase4",
    "transport": "stdio",
    "safe_mock_boundary": True,
}


def response(req_id: Any, result: Any = None, error: str = "") -> Dict[str, Any]:
    if error:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32000, "message": error}}
    return {"jsonrpc": "2.0", "id": req_id, "result": result}


def handle(request: Dict[str, Any]) -> Dict[str, Any]:
    method = request.get("method")
    params = request.get("params") or {}
    req_id = request.get("id")

    try:
        if method == "initialize":
            return response(req_id, {"serverInfo": SERVER_INFO, "capabilities": {"tools": True, "resources": True}})
        if method == "tools/list":
            return response(req_id, list_tools())
        if method == "tools/call":
            name = params.get("name", "")
            args = params.get("arguments") or {}
            return response(req_id, {"content": call_tool(name, args)})
        if method == "resources/read":
            uri = params.get("uri", "")
            return response(req_id, {"content": call_tool("read_resource", {"uri": uri})})
        if method == "shutdown":
            return response(req_id, {"ok": True, "shutdown": True})
        return response(req_id, error=f"Unsupported method: {method}")
    except Exception as exc:
        return response(req_id, error=str(exc))


def main() -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except Exception as exc:
            print(json.dumps(response(None, error=f"Invalid JSON: {exc}")), flush=True)
            continue

        res = handle(request)
        print(json.dumps(res, separators=(",", ":")), flush=True)

        if request.get("method") == "shutdown":
            return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
