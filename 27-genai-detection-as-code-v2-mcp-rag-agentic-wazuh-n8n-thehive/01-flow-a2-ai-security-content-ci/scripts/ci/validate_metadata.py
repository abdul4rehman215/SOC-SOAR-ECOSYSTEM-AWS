#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from flow_a2_common import print_result, list_files, load_data
except Exception:
    import yaml
    def print_result(stage, status, **kwargs):
        print(json.dumps({"stage": stage, "status": status, **kwargs}, indent=2))
    def list_files(root, patterns):
        out=[]
        for pat in patterns: out.extend(root.glob(pat))
        return sorted(set(out))
    def load_data(path):
        text=Path(path).read_text(encoding='utf-8')
        if path.suffix.lower()=='.json': return json.loads(text)
        return yaml.safe_load(text)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--repo-root", default="."); args = ap.parse_args()
    root = Path(args.repo_root).resolve()
    files = list_files(root, ["metadata/*.yml", "metadata/*.yaml", "metadata/*.json"])
    failures, warnings = [], []
    required_any = ["detection_id", "title", "family", "severity"]
    if not files:
        warnings.append("No metadata files found. Passing for current V2 packs; add metadata files before final enterprise packaging if desired.")
    seen_ids = {}
    for f in files:
        rel = str(f.relative_to(root))
        try:
            data = load_data(f) or {}
        except Exception as e:
            failures.append(f"{rel}: parse failed: {e}"); continue
        if not isinstance(data, dict):
            failures.append(f"{rel}: metadata root must be an object/map"); continue
        for key in required_any:
            if key not in data or data.get(key) in (None, ""):
                failures.append(f"{rel}: missing {key}")
        det_id = str(data.get("detection_id", ""))
        if det_id:
            if det_id in seen_ids:
                warnings.append(f"{rel}: duplicate detection_id {det_id} also seen in {seen_ids[det_id]}")
            seen_ids[det_id] = rel
        if "expected_rule_ids" in data and not isinstance(data["expected_rule_ids"], list):
            failures.append(f"{rel}: expected_rule_ids must be a list")
    print_result("validate_metadata", "fail" if failures else "pass", files_checked=len(files), failures=failures, warnings=warnings)
    raise SystemExit(1 if failures else 0)
if __name__ == "__main__": main()
