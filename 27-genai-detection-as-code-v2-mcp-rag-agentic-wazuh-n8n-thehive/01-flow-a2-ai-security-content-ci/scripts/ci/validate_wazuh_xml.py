#!/usr/bin/env python3
from __future__ import annotations
import argparse, re, sys, xml.etree.ElementTree as ET
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from flow_a2_common import print_result, list_files

BASE_RULE_EXPECTATIONS = {
    100300: "ai_demo_mcp_guardrail",
    100350: "ai_demo_agent_guardrail",
    100400: "ai_demo_rag_memory_guardrail",
}

def parse_wrapped_xml(path: Path):
    text = path.read_text(encoding="utf-8", errors="replace")
    # Wazuh rule files often have <group> as the top-level element; decoders can be multiple siblings.
    wrapped = f"<root>\n{text}\n</root>"
    return ET.fromstring(wrapped)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    args = ap.parse_args()
    root = Path(args.repo_root).resolve()
    files = list_files(root, ["detections/wazuh/rules/*.xml", "detections/wazuh/decoders/*.xml"])
    failures, warnings, rule_ids = [], [], []
    if not files:
        failures.append("No Wazuh XML files found under detections/wazuh/rules or detections/wazuh/decoders")
    for path in files:
        rel = str(path.relative_to(root))
        try:
            tree = parse_wrapped_xml(path)
        except Exception as e:
            failures.append(f"{rel}: XML parse failed: {e}")
            continue
        for rule in tree.findall(".//rule"):
            rid_text = rule.attrib.get("id", "")
            if not rid_text:
                failures.append(f"{rel}: rule missing id")
                continue
            try:
                rid = int(rid_text)
                rule_ids.append(rid)
            except Exception:
                failures.append(f"{rel}: non-numeric rule id {rid_text}")
                continue
            if not (100000 <= rid <= 120000):
                failures.append(f"{rel}: custom rule id {rid} outside 100000-120000")
            if rid in BASE_RULE_EXPECTATIONS:
                if_sid = (rule.findtext("if_sid") or "").strip()
                if if_sid != "86600":
                    failures.append(f"{rel}: base JSON rule {rid} must chain from built-in JSON base rule 86600, found {if_sid or 'missing'}")
                text = " ".join((field.text or "") for field in rule.findall("field") if field.attrib.get("name") == "event_source")
                if BASE_RULE_EXPECTATIONS[rid] not in text:
                    failures.append(f"{rel}: base rule {rid} missing event_source {BASE_RULE_EXPECTATIONS[rid]}")
        for decoder in tree.findall(".//decoder"):
            if not decoder.attrib.get("name"):
                failures.append(f"{rel}: decoder missing name")
    duplicates = sorted({x for x in rule_ids if rule_ids.count(x) > 1})
    if duplicates:
        failures.append(f"Duplicate Wazuh rule IDs found: {duplicates}")
    print_result("validate_wazuh_xml", "fail" if failures else "pass", files_checked=len(files), rule_ids=sorted(rule_ids), failures=failures, warnings=warnings)
    raise SystemExit(1 if failures else 0)
if __name__ == "__main__": main()
