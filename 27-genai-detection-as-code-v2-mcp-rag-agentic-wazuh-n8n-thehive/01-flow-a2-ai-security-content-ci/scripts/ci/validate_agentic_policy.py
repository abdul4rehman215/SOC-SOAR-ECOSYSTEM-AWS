#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from flow_a2_common import print_result, load_json, require_files

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--repo-root", default="."); args = ap.parse_args()
    root = Path(args.repo_root).resolve()
    required = [
      "policies/agentic/agentic_policy_bundle.json",
      "policies/agentic/approval_prompt_policy.json",
      "policies/agentic/identity_scope_policy.json",
      "policies/agentic/loop_threshold_policy.json",
      "policies/agentic/confused_deputy_policy.json"
    ]
    present, missing = require_files(root, required); failures, warnings = [], []
    if missing: failures.append("Missing agentic policy files: " + ", ".join(missing))
    for rel in present:
        data = load_json(root/rel)
        if not isinstance(data, dict): failures.append(f"{rel}: policy must be JSON object")
    loop = root/"policies/agentic/loop_threshold_policy.json"
    if loop.exists():
        data = load_json(loop)
        max_calls = data.get("max_tool_calls_per_request") or data.get("max_allowed_tool_calls") or data.get("max_tool_calls")
        if max_calls is not None and int(max_calls) <= 0: failures.append("loop threshold must be positive")
    bundle = root/"policies/agentic/agentic_policy_bundle.json"
    if bundle.exists():
        text = bundle.read_text(encoding="utf-8", errors="replace")
        for marker in ["goal", "approval", "identity", "confused", "loop"]:
            if marker not in text.lower(): warnings.append(f"agentic_policy_bundle does not mention {marker}")
    print_result("validate_agentic_policy", "fail" if failures else "pass", files_present=present, failures=failures, warnings=warnings)
    raise SystemExit(1 if failures else 0)
if __name__ == "__main__": main()
