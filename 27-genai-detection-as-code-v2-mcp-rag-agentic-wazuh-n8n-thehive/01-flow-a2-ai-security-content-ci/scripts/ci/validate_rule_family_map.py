#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from flow_a2_common import print_result, load_data

REQUIRED_RULES = [100301,100302,100303,100304,100305,100306,100351,100352,100353,100354,100355,100356,100357,100358,100401,100402,100403,100404,100405]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--repo-root", default="."); args = ap.parse_args()
    root = Path(args.repo_root).resolve(); path = root/"mappings/rule_family_map.yml"
    failures, warnings = [], []
    if not path.exists(): failures.append("Missing mappings/rule_family_map.yml")
    else:
        data = load_data(path) or {}; rules = data.get("rules", data if isinstance(data, dict) else {})
        for rid in REQUIRED_RULES:
            entry = rules.get(str(rid)) or rules.get(rid)
            if not isinstance(entry, dict): failures.append(f"Rule {rid} missing or invalid rule family map entry"); continue
            for key in ["family", "domain", "severity", "datatable", "expected_event_source"]:
                if key not in entry: failures.append(f"Rule {rid} missing {key} in rule_family_map")
    print_result("validate_rule_family_map", "fail" if failures else "pass", file=str(path), failures=failures, warnings=warnings)
    raise SystemExit(1 if failures else 0)
if __name__ == "__main__": main()
