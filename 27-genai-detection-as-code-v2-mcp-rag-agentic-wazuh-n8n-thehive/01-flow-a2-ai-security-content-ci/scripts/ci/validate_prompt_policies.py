#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from flow_a2_common import print_result, list_files, load_data

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--repo-root", default="."); args = ap.parse_args()
    root = Path(args.repo_root).resolve(); files = list_files(root, ["policies/prompts/*.json", "policies/prompts/*.yml", "policies/guardrails/*.json", "policies/guardrails/*.yml", "guardrails/*.yml", "guardrails/*.json"])
    failures, warnings = [], []
    if not files:
        warnings.append("No prompt/guardrail policy files found. Passing because runtime packs enforce local policies; add prompt policies before Phase 10.")
    for f in files:
        try: data = load_data(f)
        except Exception as e: failures.append(f"{f.relative_to(root)} parse failed: {e}")
    print_result("validate_prompt_policies", "fail" if failures else "pass", files_checked=[str(f.relative_to(root)) for f in files], failures=failures, warnings=warnings)
    raise SystemExit(1 if failures else 0)
if __name__ == "__main__": main()
