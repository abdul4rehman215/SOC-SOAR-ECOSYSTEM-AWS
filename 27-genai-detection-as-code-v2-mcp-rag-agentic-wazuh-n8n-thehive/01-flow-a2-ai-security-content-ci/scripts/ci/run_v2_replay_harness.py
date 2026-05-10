#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from flow_a2_common import print_result, load_data, list_files

def flatten_expected(data):
    if not isinstance(data, dict): return {}
    if "expected_rules" in data and isinstance(data["expected_rules"], dict):
        data = data["expected_rules"]
    out = {}
    for k, v in data.items():
        if isinstance(v, dict):
            rule = v.get("expected_rule_id") or v.get("rule_id")
        else:
            rule = v
        try: out[str(k)] = int(rule)
        except Exception: pass
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--repo-root", default="."); args = ap.parse_args()
    root = Path(args.repo_root).resolve(); failures, warnings = [], []
    expected = {}
    for rel in ["tests/expected/mcp_expected_rules.yml", "tests/expected/rag_memory_expected_rules.yml", "tests/expected/agentic_expected_rules.yml", "tests/expected/v2_expected_rules.yml"]:
        p = root/rel
        if p.exists(): expected.update(flatten_expected(load_data(p) or {}))
        else: warnings.append(f"Missing optional expected map {rel}")
    event_files = list_files(root, ["tests/events/mcp/**/*.json", "tests/events/rag_memory/**/*.json", "tests/events/agentic/**/*.json"])
    pos_total = neg_total = pos_pass = neg_pass = 0
    mismatches = []
    for path in event_files:
        rel = str(path.relative_to(root)); stem = path.stem
        data = json.loads(path.read_text(encoding="utf-8"))
        event = data.get("event", data)
        expected_id = event.get("expected_wazuh_rule_id")
        mapped = expected.get(stem)
        is_negative = "/negative/" in rel or "negative" in rel
        if is_negative: neg_total += 1
        else: pos_total += 1
        ok = True
        if mapped is not None and expected_id is not None and int(mapped) != int(expected_id):
            ok = False; mismatches.append({"file": rel, "expected_map": mapped, "event_expected": expected_id})
        if expected_id is None and not is_negative:
            ok = False; mismatches.append({"file": rel, "error": "positive event missing expected_wazuh_rule_id"})
        if is_negative and ok: neg_pass += 1
        if not is_negative and ok: pos_pass += 1
    status = "fail" if mismatches else "pass"
    print_result("run_v2_replay_harness", status, corpus_version="v2-phase7-local-static", total_tests=len(event_files), positive_total=pos_total, positive_passed=pos_pass, positive_failed=pos_total-pos_pass, negative_total=neg_total, negative_passed=neg_pass, negative_failed=neg_total-neg_pass, expected_rule_mismatches=mismatches, warnings=warnings)
    raise SystemExit(1 if mismatches else 0)
if __name__ == "__main__": main()
