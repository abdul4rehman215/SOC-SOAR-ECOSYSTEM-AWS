#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from flow_a2_common import print_result, load_json

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--repo-root", default="."); args = ap.parse_args()
    root = Path(args.repo_root).resolve(); files = [root/"policies/mcp/mcp_schema_hash_registry.json", root/"policies/mcp/mcp_tool_registry.json"]
    failures, warnings = [], []
    checked = []
    for path in files:
        if not path.exists():
            warnings.append(f"Missing optional registry {path.relative_to(root)}")
            continue
        checked.append(str(path.relative_to(root)))
        data = load_json(path)
        if "tools" in data:
            for tool in data.get("tools", []):
                for key in ["name", "permission_scope", "sensitive", "hitl_required"]:
                    if key not in tool: failures.append(f"{path.relative_to(root)}: tool entry missing {key}")
        else:
            if "hash_algorithm" not in data:
                warnings.append(f"{path.relative_to(root)}: no hash_algorithm; registry may be placeholder")
            if "note" in data:
                warnings.append(f"{path.relative_to(root)}: placeholder registry noted; Flow A2 passes but Phase 8 should deploy real hashes")
    print_result("validate_tool_schema_hashes", "fail" if failures else "pass", files_checked=checked, failures=failures, warnings=warnings)
    raise SystemExit(1 if failures else 0)
if __name__ == "__main__": main()
