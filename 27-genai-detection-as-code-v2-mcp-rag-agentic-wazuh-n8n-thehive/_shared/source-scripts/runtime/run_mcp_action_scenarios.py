#!/usr/bin/env python3
"""Run local MCP action-path scenarios and append telemetry to JSONL."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def add_lab_to_path(repo_root: Path) -> None:
    lab = repo_root / "app" / "mcp-action-lab"
    sys.path.insert(0, str(lab))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run V2 Local MCP Action Lab scenarios.")
    parser.add_argument("--scenario", default="all", help="Scenario name or all")
    parser.add_argument("--repo-root", default=".", help="Repository root")
    parser.add_argument("--log-file", default="/var/log/ai-demo/mcp-events.jsonl", help="MCP JSONL log file")
    parser.add_argument("--dry-run", action="store_true", help="Print events instead of writing to log")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    add_lab_to_path(repo_root)

    from scenarios import expected_ids_for, run_scenarios
    from telemetry import write_events

    events = run_scenarios(str(repo_root), args.scenario)
    expected_ids = expected_ids_for(args.scenario)

    if args.dry_run:
        for event in events:
            print(json.dumps(event, indent=2))
    else:
        write_events(args.log_file, events)

    print(json.dumps({
        "stage": "run_mcp_action_scenarios",
        "status": "pass",
        "scenario": args.scenario,
        "events_written": 0 if args.dry_run else len(events),
        "dry_run": args.dry_run,
        "log_file": args.log_file,
        "request_ids": [e["request_id"] for e in events],
        "expected_wazuh_rule_ids": expected_ids,
        "safe_mock_boundary": {
            "real_shell_execution": False,
            "real_external_webhook": False,
            "real_case_mutation": False,
        }
    }, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
