#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from flow_a2_common import print_result, list_files, load_json

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--repo-root", default="."); args = ap.parse_args()
    root = Path(args.repo_root).resolve(); files = list_files(root, ["app/mcp-action-lab/manifest.json", "mcp/manifests/*.json", "mcp/servers/**/manifest.json"])
    failures, warnings, tools_seen = [], [], []
    if not files: failures.append("No MCP manifest found. Expected app/mcp-action-lab/manifest.json or mcp/manifests/*.json")
    for f in files:
        rel = str(f.relative_to(root))
        try: data = load_json(f)
        except Exception as e: failures.append(f"{rel}: JSON parse failed: {e}"); continue
        for key in ["name", "version", "transport", "tools"]:
            if key not in data: failures.append(f"{rel}: missing {key}")
        if data.get("safe_mock_boundary") is not True:
            warnings.append(f"{rel}: safe_mock_boundary is not true; verify this manifest does not describe production tools")
        if not isinstance(data.get("tools", []), list) or not data.get("tools"):
            failures.append(f"{rel}: tools must be a non-empty list")
        tools_seen.extend(data.get("tools", []) if isinstance(data.get("tools"), list) else [])
    print_result("validate_mcp_manifest", "fail" if failures else "pass", manifests_checked=len(files), tools_seen=sorted(set(map(str, tools_seen))), failures=failures, warnings=warnings)
    raise SystemExit(1 if failures else 0)
if __name__ == "__main__": main()
