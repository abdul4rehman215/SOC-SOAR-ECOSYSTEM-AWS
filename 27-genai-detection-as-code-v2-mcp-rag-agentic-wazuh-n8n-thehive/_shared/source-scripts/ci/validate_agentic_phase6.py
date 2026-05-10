#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List


REQUIRED_FILES = [
    "schemas/agentic_event.schema.json",
    "app/agentic-risk-lab/README.md",
    "app/agentic-risk-lab/agent_runner.py",
    "app/agentic-risk-lab/planner.py",
    "app/agentic-risk-lab/policy_engine.py",
    "app/agentic-risk-lab/scenarios.py",
    "app/agentic-risk-lab/telemetry.py",
    "app/agentic-risk-lab/tools_simulator.py",
    "app/agentic-risk-lab/approvals.py",
    "policies/agentic/agentic_policy_bundle.json",
    "policies/agentic/approval_prompt_policy.json",
    "policies/agentic/identity_scope_policy.json",
    "policies/agentic/loop_threshold_policy.json",
    "policies/agentic/confused_deputy_policy.json",
    "detections/wazuh/decoders/genai_agentic_decoder.xml",
    "detections/wazuh/rules/genai_agentic_rules.xml",
    "scripts/runtime/run_agentic_scenarios.py",
    "scripts/runtime/run_agentic_smoke_test.sh",
    "tests/expected/agentic_expected_rules.yml",
    "data-tables/schemas/flow_v2_agentic_incidents_schema.csv",
    "data-tables/empty-csv/flow_v2_agentic_incidents_empty.csv",
]

EXPECTED_RULE_IDS = {100350, 100351, 100352, 100353, 100354, 100355, 100356, 100357, 100358}
EXPECTED_SOURCE = "ai_demo_agent_guardrail"


def parse_rules_xml(path: Path, failures: List[str]) -> str:
    text = path.read_text(encoding="utf-8")
    try:
        ET.fromstring(text)
    except ET.ParseError as exc:
        failures.append(f"rules XML parse error: {exc}")
    if "<if_sid>86600</if_sid>" not in text:
        failures.append("genai_agentic_rules.xml base rule 100350 must chain to Wazuh JSON base rule 86600")
    for rid in sorted(EXPECTED_RULE_IDS):
        if f'id="{rid}"' not in text:
            failures.append(f"missing Wazuh rule id {rid}")
    return text


def load_json(path: Path, failures: List[str]) -> Dict:
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:
        failures.append(f"failed to load JSON {path}: {exc}")
        return {}


def validate_event_shape(event: Dict, failures: List[str]) -> None:
    required = [
        "schema_version",
        "event_source",
        "event_type",
        "request_id",
        "session_id",
        "user_id",
        "agent_id",
        "original_user_goal",
        "observed_agent_goal",
        "agent_plan_id",
        "agent_plan_step_count",
        "tool_sequence_csv",
        "mcp_server_sequence_csv",
        "approval_required",
        "approval_status",
        "guardrail_action",
        "detection_family",
        "severity",
        "risk_score",
        "risk_flags_csv",
        "expected_wazuh_rule_id",
    ]
    missing = [key for key in required if key not in event]
    if missing:
        failures.append(f"event {event.get('request_id')} missing required keys: {missing}")
    if event.get("event_source") != EXPECTED_SOURCE:
        failures.append(f"bad event_source for {event.get('request_id')}: {event.get('event_source')}")
    if event.get("schema_version") != "2.0":
        failures.append(f"bad schema_version for {event.get('request_id')}: {event.get('schema_version')}")
    try:
        rid = int(event.get("expected_wazuh_rule_id"))
    except Exception:
        failures.append(f"event {event.get('request_id')} expected_wazuh_rule_id is not integer")
        return
    if rid not in EXPECTED_RULE_IDS:
        failures.append(f"event {event.get('request_id')} has unexpected expected_wazuh_rule_id {rid}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate V2 Phase 6 Agentic AI Risk Detection Pack.")
    parser.add_argument("repo_root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    failures: List[str] = []

    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            failures.append(f"missing required file: {rel}")

    if (root / "detections/wazuh/rules/genai_agentic_rules.xml").exists():
        parse_rules_xml(root / "detections/wazuh/rules/genai_agentic_rules.xml", failures)

    for rel in [
        "schemas/agentic_event.schema.json",
        "policies/agentic/agentic_policy_bundle.json",
        "policies/agentic/approval_prompt_policy.json",
        "policies/agentic/identity_scope_policy.json",
        "policies/agentic/loop_threshold_policy.json",
        "policies/agentic/confused_deputy_policy.json",
    ]:
        if (root / rel).exists():
            load_json(root / rel, failures)

    with tempfile.NamedTemporaryFile(prefix="agentic-phase6-", suffix=".jsonl", delete=True) as tmp:
        cmd = [
            sys.executable,
            str(root / "scripts/runtime/run_agentic_scenarios.py"),
            "--scenario",
            "all",
            "--repo-root",
            str(root),
            "--log-file",
            tmp.name,
        ]
        proc = subprocess.run(cmd, text=True, capture_output=True)
        if proc.returncode != 0:
            failures.extend(["scenario runner failed", proc.stdout[-2000:], proc.stderr[-2000:]])
        else:
            text = Path(tmp.name).read_text(encoding="utf-8").strip()
            lines = text.splitlines() if text else []
            if len(lines) != 9:
                failures.append(f"expected 9 events, found {len(lines)}")
            observed = set()
            for line in lines:
                event = json.loads(line)
                validate_event_shape(event, failures)
                observed.add(int(event.get("expected_wazuh_rule_id") or 0))
            missing = EXPECTED_RULE_IDS - observed
            if missing:
                failures.append(f"missing expected rule IDs from scenario output: {sorted(missing)}")

    status = "pass" if not failures else "fail"
    print(
        json.dumps(
            {
                "stage": "validate_agentic_phase6",
                "status": status,
                "checked_files": len(REQUIRED_FILES),
                "expected_rule_ids": sorted(EXPECTED_RULE_IDS),
                "failures": failures,
            },
            indent=2,
        )
    )
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
