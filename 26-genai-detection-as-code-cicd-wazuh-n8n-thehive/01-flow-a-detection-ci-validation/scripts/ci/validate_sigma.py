#!/usr/bin/env python3
import json
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print(json.dumps({
        "stage": "sigma_validation",
        "status": "fail",
        "error": "PyYAML is required. Install with: pip3 install pyyaml"
    }))
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[2]


def load_manifest(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def sigma_binary():
    for name in ("sigma", "sigma-cli"):
        path = shutil.which(name)
        if path:
            return path
    return None


def basic_yaml_checks(path: Path):
    errors = []
    warnings = []
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        errors.append("Sigma file is not a YAML mapping")
        return warnings, errors
    required = ["title", "logsource", "detection"]
    for field in required:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    detection = data.get("detection")
    if isinstance(detection, dict) and "condition" not in detection:
        errors.append("Missing detection.condition")
    if "id" not in data:
        warnings.append("Missing Sigma id field")
    return warnings, errors


def sigma_check(bin_path: str, path: Path):
    commands = [
        [bin_path, "check", str(path)],
        [bin_path, "validate", str(path)],
    ]
    last = None
    for cmd in commands:
        cp = subprocess.run(cmd, capture_output=True, text=True, check=False)
        last = cp
        if cp.returncode == 0:
            return True, (cp.stdout or cp.stderr).strip()
        combined = f"{cp.stdout}\n{cp.stderr}".lower()
        if "unknown command" in combined or "invalid choice" in combined:
            continue
        return False, (cp.stdout or cp.stderr).strip()
    return False, (last.stdout or last.stderr).strip() if last else "No sigma command available"


def main():
    if len(sys.argv) != 2:
        print(json.dumps({
            "stage": "sigma_validation",
            "status": "fail",
            "error": "Usage: validate_sigma.py <changed_files.json>"
        }))
        sys.exit(1)

    manifest = load_manifest(Path(sys.argv[1]))
    files = manifest.get("sigma_rules", [])
    result = {
        "stage": "sigma_validation",
        "status": "skip" if not files else "pass",
        "checked": len(files),
        "passed_files": [],
        "failed_files": [],
        "warnings": [],
        "notes": [],
    }

    sigbin = sigma_binary()
    if files and sigbin:
        result["notes"].append(f"Using Sigma CLI binary: {sigbin}")
    elif files:
        result["notes"].append("Sigma CLI not found; running YAML-only fallback validation")

    for rel in files:
        path = ROOT / rel
        file_report = {"file": rel, "errors": [], "warnings": []}

        if not path.exists():
            file_report["errors"].append("File not found in workspace")
            result["failed_files"].append(file_report)
            result["status"] = "fail"
            continue

        try:
            warns, errs = basic_yaml_checks(path)
            file_report["warnings"].extend(warns)
            file_report["errors"].extend(errs)
        except Exception as e:
            file_report["errors"].append(f"YAML parse/validation error: {e}")

        if not file_report["errors"] and sigbin:
            ok, msg = sigma_check(sigbin, path)
            if not ok:
                file_report["errors"].append(msg or "Sigma CLI validation failed")
            elif msg:
                file_report["warnings"].append(msg)

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
