#!/usr/bin/env python3
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print(json.dumps({
        "stage": "metadata_validation",
        "status": "fail",
        "error": "PyYAML is required. Install with: pip3 install pyyaml"
    }))
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[2]
REQUIRED_FIELDS = {
    "detection_id": str,
    "title": str,
    "family": str,
    "status": str,
    "severity": str,
    "owner": str,
    "owasp_category": str,
    "atlas_techniques": list,
    "mitre_attack_ids": list,
    "positive_test_ids": list,
    "negative_test_ids": list,
    "expected_rule_ids": list,
}


def load_manifest(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_doc(path: Path):
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return yaml.safe_load(text)


def possible_metadata_files(stem: str):
    candidates = []
    for ext in (".yml", ".yaml", ".json"):
        candidates.append(ROOT / "metadata" / f"{stem}{ext}")
    return candidates


def file_stem_without_suffixes(rel_path: str) -> str:
    p = Path(rel_path)
    return p.stem


def validate_metadata_doc(rel: str, path: Path):
    errors = []
    warnings = []
    try:
        data = load_doc(path)
    except Exception as e:
        return [f"Unable to parse metadata file: {e}"], []

    if not isinstance(data, dict):
        return ["Metadata file must be a mapping/object"], []

    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in data:
            errors.append(f"Missing required field: {field}")
            continue
        value = data[field]
        if expected_type is list:
            if not isinstance(value, list) or not value:
                errors.append(f"Field {field} must be a non-empty list")
        else:
            if not isinstance(value, expected_type) or not str(value).strip():
                errors.append(f"Field {field} must be a non-empty {expected_type.__name__}")

    rule_ids = data.get("expected_rule_ids", [])
    if isinstance(rule_ids, list):
        for rid in rule_ids:
            if not isinstance(rid, int):
                warnings.append(f"expected_rule_ids contains non-integer value: {rid}")

    return errors, warnings


def main():
    if len(sys.argv) != 2:
        print(json.dumps({
            "stage": "metadata_validation",
            "status": "fail",
            "error": "Usage: validate_metadata.py <changed_files.json>"
        }))
        sys.exit(1)

    manifest = load_manifest(Path(sys.argv[1]))
    changed_metadata = set(manifest.get("metadata_files", []))
    changed_detection_files = set(
        manifest.get("wazuh_rules", []) +
        manifest.get("wazuh_decoders", []) +
        manifest.get("sigma_rules", [])
    )

    required_metadata_candidates = {}
    for rel in changed_detection_files:
        stem = file_stem_without_suffixes(rel)
        matches = [p for p in possible_metadata_files(stem) if p.exists()]
        required_metadata_candidates[rel] = matches
        for m in matches:
            changed_metadata.add(str(m.relative_to(ROOT)))

    result = {
        "stage": "metadata_validation",
        "status": "pass",
        "checked": 0,
        "passed_files": [],
        "failed_files": [],
        "warnings": [],
        "notes": [],
        "missing_metadata_for": [],
    }

    for rel, matches in required_metadata_candidates.items():
        if not matches:
            result["missing_metadata_for"].append(rel)
            result["status"] = "fail"

    if not changed_metadata and not result["missing_metadata_for"]:
        result["status"] = "skip"
        result["notes"].append("No metadata files changed or inferred from changed detections")
        print(json.dumps(result, ensure_ascii=False))
        return

    for rel in sorted(changed_metadata):
        path = ROOT / rel
        file_report = {"file": rel, "errors": [], "warnings": []}
        result["checked"] += 1
        if not path.exists():
            file_report["errors"].append("Metadata file not found")
            result["failed_files"].append(file_report)
            result["status"] = "fail"
            continue
        errs, warns = validate_metadata_doc(rel, path)
        file_report["errors"].extend(errs)
        file_report["warnings"].extend(warns)
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
