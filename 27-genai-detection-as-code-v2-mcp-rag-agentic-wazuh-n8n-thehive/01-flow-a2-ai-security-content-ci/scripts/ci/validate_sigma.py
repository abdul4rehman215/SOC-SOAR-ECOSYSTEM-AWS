#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from flow_a2_common import print_result, list_files, load_data

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--repo-root", default="."); args = ap.parse_args()
    root = Path(args.repo_root).resolve(); files = list_files(root, ["detections/sigma/**/*.yml", "detections/sigma/**/*.yaml"])
    failures, warnings = [], []
    required = ["title", "id", "status", "logsource", "detection", "level"]
    if not files:
        warnings.append("No Sigma files found. Passing because Sigma companion content is optional for current V2 lab state.")
    for f in files:
        rel = str(f.relative_to(root))
        try: data = load_data(f) or {}
        except Exception as e:
            failures.append(f"{rel}: failed to parse YAML: {e}"); continue
        for key in required:
            if key not in data: failures.append(f"{rel}: missing required Sigma key {key}")
    print_result("validate_sigma", "fail" if failures else "pass", files_checked=len(files), failures=failures, warnings=warnings)
    raise SystemExit(1 if failures else 0)
if __name__ == "__main__": main()
