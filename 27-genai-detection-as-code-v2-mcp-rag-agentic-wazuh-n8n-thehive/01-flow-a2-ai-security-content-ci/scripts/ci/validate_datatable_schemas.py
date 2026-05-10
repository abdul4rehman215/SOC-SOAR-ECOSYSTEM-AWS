#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from flow_a2_common import print_result, list_files, csv_schema_columns

VALID_TYPES = {"string", "number", "boolean", "dateTime"}
REQUIRED_TABLES = ["flow_a2_ci_runs", "flow_a2_ci_changed_files", "flow_a2_ci_stage_results", "flow_v2_regression_runs"]
REQUIRED_HEADERS = {"column_name", "n8n_type", "required", "recommended_match_column", "description"}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--repo-root", default="."); args = ap.parse_args()
    root = Path(args.repo_root).resolve(); files = list_files(root, ["data-tables/schemas/*_schema.csv"])
    failures, warnings, tables = [], [], []
    for f in files:
        rows = csv_schema_columns(f)
        table = f.name.replace("_schema.csv", ""); tables.append(table)
        if not rows:
            if table in REQUIRED_TABLES: failures.append(f"{f.relative_to(root)} has no rows")
            else: warnings.append(f"{f.relative_to(root)} has no rows")
            continue
        headers = set(rows[0].keys())
        missing_headers = sorted(REQUIRED_HEADERS - headers)
        if missing_headers:
            msg = f"{f.relative_to(root)} uses legacy/simple header format; missing schema headers {missing_headers}"
            if table in REQUIRED_TABLES: failures.append(msg)
            else: warnings.append(msg)
            continue
        names = {r.get("column_name") for r in rows}
        types = {r.get("n8n_type") for r in rows}
        bad = sorted(t for t in types if t and t not in VALID_TYPES)
        if bad:
            msg = f"{f.relative_to(root)} has invalid n8n_type values {bad}"
            if table in REQUIRED_TABLES: failures.append(msg)
            else: warnings.append(msg)
        if not names:
            msg = f"{f.relative_to(root)} has no columns"
            if table in REQUIRED_TABLES: failures.append(msg)
            else: warnings.append(msg)
    for table in REQUIRED_TABLES:
        if table not in tables: failures.append(f"Missing DataTable schema for {table}")
    print_result("validate_datatable_schemas", "fail" if failures else "pass", schemas_checked=tables, failures=failures, warnings=warnings)
    raise SystemExit(1 if failures else 0)
if __name__ == "__main__": main()
