#!/usr/bin/env python3
"""Local MCP-style client for the action lab."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional


class LocalMCPClient:
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root).resolve()
        self.server_path = self.repo_root / "app" / "mcp-action-lab" / "server.py"
        self.proc: Optional[subprocess.Popen] = None
        self.next_id = 1

    def __enter__(self) -> "LocalMCPClient":
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        self.proc = subprocess.Popen(
            [sys.executable, str(self.server_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(self.server_path.parent),
            env=env,
        )
        self.initialize()
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            self.request("shutdown", {})
        except Exception:
            pass
        if self.proc:
            try:
                self.proc.terminate()
                self.proc.wait(timeout=3)
            except Exception:
                self.proc.kill()

    def request(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not self.proc or not self.proc.stdin or not self.proc.stdout:
            raise RuntimeError("MCP server process is not running")

        req = {"jsonrpc": "2.0", "id": self.next_id, "method": method, "params": params or {}}
        self.next_id += 1

        self.proc.stdin.write(json.dumps(req, separators=(",", ":")) + "\n")
        self.proc.stdin.flush()

        line = self.proc.stdout.readline()
        if not line:
            stderr = self.proc.stderr.read() if self.proc.stderr else ""
            raise RuntimeError(f"MCP server returned no response. stderr={stderr}")

        res = json.loads(line)
        if "error" in res:
            raise RuntimeError(res["error"].get("message", str(res["error"])))
        return res["result"]

    def initialize(self) -> Dict[str, Any]:
        return self.request("initialize", {})

    def list_tools(self) -> Dict[str, Any]:
        return self.request("tools/list", {})

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        return self.request("tools/call", {"name": name, "arguments": arguments})

    def read_resource(self, uri: str) -> Dict[str, Any]:
        return self.request("resources/read", {"uri": uri})
