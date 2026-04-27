#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CUSTOM_RULE_MIN = int(os.getenv("WAZUH_CUSTOM_RULE_MIN", "100000"))
CUSTOM_RULE_MAX = int(os.getenv("WAZUH_CUSTOM_RULE_MAX", "120000"))
ENFORCE_RULE_RANGE = os.getenv("WAZUH_RULE_ID_ENFORCE", "true").lower() in {"1", "true", "yes"}


def load_manifest(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def xmllint_available() -> bool:
    return shutil.which("xmllint") is not None


def parse_xml(path: Path):
    tree = ET.parse(path)
    return tree.getroot()


def validate_with_xmllint(path: Path):
    cp = subprocess.run(
        ["xmllint", "--noout", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    return cp.returncode == 0, (cp.stderr or cp.stdout).strip()


def iter_all_elements(root):
    for elem in root.iter():
        yield elem


def local_name(tag: str) -> str:
    return tag.split("}")[-1] if "}" in tag else tag


def inspect_rule_file(path: Path):
    warnings = []
    errors = []
    root = parse_xml(path)
    rule_ids = []
    for elem in iter_all_elements(root):
        if local_name(elem.tag) == "rule":
            rid = elem.attrib.get("id")
            if rid is None:
                errors.append("Found <rule> without id attribute")
                continue
            if not rid.isdigit():
                errors.append(f"Rule id '{rid}' is not numeric")
                continue
            rid_num = int(rid)
            rule_ids.append(rid_num)
            if ENFORCE_RULE_RANGE and not (CUSTOM_RULE_MIN <= rid_num <= CUSTOM_RULE_MAX):
                errors.append(
                    f"Rule id {rid_num} is outside custom range {CUSTOM_RULE_MIN}-{CUSTOM_RULE_MAX}"
                )
    if not rule_ids:
        warnings.append("No <rule> elements found in file")
    if len(rule_ids) != len(set(rule_ids)):
        errors.append("Duplicate rule ids found in same file")
    return warnings, errors


def inspect_decoder_file(path: Path):
    warnings = []
    errors = []
    root = parse_xml(path)
    has_decoder = any(local_name(elem.tag) == "decoder" for elem in iter_all_elements(root))
    if not has_decoder:
        warnings.append("No <decoder> elements found in file")
    return warnings, errors


def main():
    if len(sys.argv) != 2:
        print(json.dumps({
            "stage": "xml_validation",
            "status": "fail",
            "error": "Usage: validate_wazuh_xml.py <changed_files.json>"
        }))
        sys.exit(1)

    manifest = load_manifest(Path(sys.argv[1]))
    files = list(dict.fromkeys(manifest.get("wazuh_rules", []) + manifest.get("wazuh_decoders", [])))

    result = {
        "stage": "xml_validation",
        "status": "skip" if not files else "pass",
        "checked": len(files),
        "passed_files": [],
        "failed_files": [],
        "warnings": [],
        "notes": [],
        "engine": "xmllint" if xmllint_available() else "python_xml_etree",
    }

    for rel in files:
        path = ROOT / rel
        file_report = {"file": rel, "errors": [], "warnings": []}

        if not path.exists():
            file_report["errors"].append("File not found in workspace")
            result["failed_files"].append(file_report)
            result["status"] = "fail"
            continue

        if xmllint_available():
            ok, msg = validate_with_xmllint(path)
            if not ok:
                file_report["errors"].append(msg or "xmllint validation failed")
                result["failed_files"].append(file_report)
                result["status"] = "fail"
                continue

        try:
            if rel.startswith("detections/wazuh/rules/"):
                warns, errs = inspect_rule_file(path)
            else:
                warns, errs = inspect_decoder_file(path)
            file_report["warnings"].extend(warns)
            file_report["errors"].extend(errs)
        except ET.ParseError as e:
            file_report["errors"].append(f"XML parse error: {e}")
        except Exception as e:
            file_report["errors"].append(f"Unexpected validation error: {e}")

        if file_report["errors"]:
            result["failed_files"].append(file_report)
            result["status"] = "fail"
        else:
            if file_report["warnings"]:
                result["warnings"].append(file_report)
            result["passed_files"].append(rel)

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
