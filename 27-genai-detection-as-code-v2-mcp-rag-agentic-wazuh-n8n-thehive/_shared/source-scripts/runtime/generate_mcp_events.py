#!/usr/bin/env python3
"""
GenAI Detection-as-Code V2 - MCP Phase 1 event generator.

Writes safe mock MCP runtime events to a JSONL log file. This does not call real MCP
servers, does not execute tools, and does not perform network actions. It only emits
structured telemetry for Wazuh/n8n/TheHive testing.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Iterable, List

SCENARIO_TO_FILE: Dict[str, str] = {
    "benign": "tests/events/mcp/negative/mcp_benign_tool_call_001.json",
    "tool_poisoning": "tests/events/mcp/positive/mcp_tool_poisoning_001.json",
    "schema_drift": "tests/events/mcp/positive/mcp_schema_drift_001.json",
    "overprivileged": "tests/events/mcp/positive/mcp_overprivileged_tool_001.json",
    "sensitive_without_hitl": "tests/events/mcp/positive/mcp_sensitive_tool_without_hitl_001.json",
    "argument_injection": "tests/events/mcp/positive/mcp_tool_argument_injection_001.json",
    "resource_exfiltration": "tests/events/mcp/positive/mcp_resource_exfiltration_001.json",
}

ORDERED_ALL = [
    "benign",
    "tool_poisoning",
    "schema_drift",
    "overprivileged",
    "sensitive_without_hitl",
    "argument_injection",
    "resource_exfiltration",
]


def load_event(repo_root: Path, scenario: str) -> dict:
    rel = SCENARIO_TO_FILE[scenario]
    path = repo_root / rel
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def resolve_scenarios(requested: str) -> List[str]:
    if requested == "all":
        return ORDERED_ALL
    if requested not in SCENARIO_TO_FILE:
        allowed = ", ".join(["all"] + sorted(SCENARIO_TO_FILE))
        raise SystemExit(f"Unknown scenario '{requested}'. Allowed: {allowed}")
    return [requested]


def write_events(events: Iterable[dict], log_file: Path) -> int:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with log_file.open("a", encoding="utf-8") as f:
        for event in events:
            f.write(json.dumps(event, separators=(",", ":")) + "\n")
            count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit safe mock MCP V2 events as JSONL.")
    parser.add_argument(
        "--scenario",
        default="tool_poisoning",
        help="Scenario to emit: all, benign, tool_poisoning, schema_drift, overprivileged, sensitive_without_hitl, argument_injection, resource_exfiltration.",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root containing tests/events/mcp.",
    )
    parser.add_argument(
        "--log-file",
        default="/var/log/ai-demo/mcp-events.jsonl",
        help="JSONL output path monitored by Wazuh agent.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    log_file = Path(args.log_file)
    scenarios = resolve_scenarios(args.scenario)
    events = [load_event(repo_root, s) for s in scenarios]
    written = write_events(events, log_file)

    print(json.dumps({
        "stage": "generate_mcp_events",
        "status": "pass",
        "scenario": args.scenario,
        "events_written": written,
        "log_file": str(log_file),
        "request_ids": [e.get("request_id") for e in events],
        "expected_wazuh_rule_ids": [e.get("expected_wazuh_rule_id") for e in events],
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
