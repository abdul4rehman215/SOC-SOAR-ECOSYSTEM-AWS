#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from flow_a2_common import print_result, load_json

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--repo-root", default="."); args = ap.parse_args()
    root = Path(args.repo_root).resolve(); path = root / "policies/mcp/mcp_policy_bundle.json"
    failures, warnings = [], []
    if not path.exists(): failures.append("Missing policies/mcp/mcp_policy_bundle.json")
    else:
        data = load_json(path)
        allow = data.get("tool_allowlist", [])
        sens = data.get("sensitive_tools", [])
        hitl = data.get("hitl_required_tools", [])
        scopes = data.get("allowed_permission_scopes", {})
        roots = data.get("allowed_resource_roots", [])
        if not isinstance(allow, list) or not allow: failures.append("tool_allowlist must be non-empty list")
        if not set(sens).issubset(set(allow)): failures.append("sensitive_tools must be subset of tool_allowlist")
        if not set(sens).issubset(set(hitl)): failures.append("all sensitive_tools must also be hitl_required_tools")
        if not isinstance(scopes, dict) or not scopes: failures.append("allowed_permission_scopes must be non-empty object")
        for t in allow:
            if t not in scopes: failures.append(f"allowed tool {t} missing allowed_permission_scopes entry")
        for t in allow:
            if not str(t).endswith("_mock") and t in {"send_external_webhook", "run_shell_command", "delete_resource"}:
                failures.append(f"Unsafe real tool name appears in allowlist: {t}")
        if not isinstance(roots, list) or not roots: warnings.append("allowed_resource_roots missing or empty")
    print_result("validate_mcp_policy_bundle", "fail" if failures else "pass", file=str(path), failures=failures, warnings=warnings)
    raise SystemExit(1 if failures else 0)
if __name__ == "__main__": main()
