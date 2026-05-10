#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from flow_a2_common import print_result, load_data

REQUIRED_HIGH_RISK_RULES = [100301,100303,100304,100306,100401,100402,100405,100351,100352,100353,100354,100355,100356,100357,100358]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--repo-root", default="."); args = ap.parse_args()
    root = Path(args.repo_root).resolve(); path = root/"mappings/case_template_rule_map.yml"
    failures, warnings = [], []
    if not path.exists(): failures.append("Missing mappings/case_template_rule_map.yml")
    else:
        data = load_data(path) or {}
        mappings = data.get("rule_template_map", data if isinstance(data, dict) else {})
        for rid in REQUIRED_HIGH_RISK_RULES:
            entry = mappings.get(str(rid)) or mappings.get(rid)
            if not entry:
                failures.append(f"High-risk rule {rid} missing case template mapping")
                continue
            if isinstance(entry, str):
                template = entry
            else:
                template = entry.get("template") or entry.get("case_template")
            if not template or not str(template).startswith("flowc-"):
                failures.append(f"Rule {rid} has invalid template {template}")
            if isinstance(entry, dict) and entry.get("required") is False:
                warnings.append(f"Rule {rid} is marked required=false; high-risk rules should normally be required")
    print_result("validate_case_template_mapping", "fail" if failures else "pass", file=str(path), failures=failures, warnings=warnings)
    raise SystemExit(1 if failures else 0)
if __name__ == "__main__": main()
