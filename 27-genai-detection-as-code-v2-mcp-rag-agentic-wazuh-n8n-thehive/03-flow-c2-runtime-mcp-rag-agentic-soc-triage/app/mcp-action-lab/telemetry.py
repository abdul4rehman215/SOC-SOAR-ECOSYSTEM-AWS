#!/usr/bin/env python3
"""Telemetry helpers for V2 MCP action-path events."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def ensure_parent(path: str) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)


def csv(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (list, tuple, set)):
        return ",".join(str(v) for v in value)
    return str(value)


def base_event(
    *,
    event_type: str,
    request_id: str,
    detection_family: str,
    severity: str,
    risk_score: int,
    expected_wazuh_rule_id: Optional[int],
    risk_flags: Optional[Iterable[str]] = None,
    scenario: str = "",
) -> Dict[str, Any]:
    flags = list(risk_flags or [])
    return {
        "schema_version": "2.0",
        "timestamp": utc_now(),
        "event_source": "ai_demo_mcp_guardrail",
        "event_type": event_type,

        "request_id": request_id,
        "session_id": "sess-mcp-demo-001",
        "user_id": "student-user-demo",
        "agent_id": "agent-demo-001",
        "model": "demo-llm",

        "policy_bundle_version": "v2.0.0-phase4-local-mcp-lab",
        "policy_bundle_hash": "sha256:local-mcp-action-lab-policy-bundle-v1",
        "environment": "lab",
        "app_name": "ai-demo-v2",
        "scenario": scenario,

        "agent_goal": "",
        "agent_plan_id": "",
        "agent_plan_step": 0,
        "agent_plan_summary": "",

        "mcp_server_name": "local-security-tools",
        "mcp_server_id": "mcp-local-security-tools-001",
        "mcp_transport": "stdio",
        "server_trust_level": "trusted_local",
        "server_manifest_hash": "sha256:local-security-tools-manifest-v1",
        "server_signature_status": "lab_unsigned",

        "tool_name": "",
        "tool_category": "",
        "tool_schema_hash_expected": "",
        "tool_schema_hash_observed": "",
        "tool_description_hash_expected": "",
        "tool_description_hash_observed": "",
        "schema_drift_detected": False,

        "tool_args_summary": "",
        "tool_args_risk_flags_csv": "",
        "tool_result_excerpt": "",
        "tool_result_trust_level": "trusted_local",
        "tool_result_risk_flags_csv": "",

        "resource_uri": "",
        "resource_scope": "",
        "allowed_resource_roots_csv": "ticket://,kb://,policy://",
        "resource_scope_violation": False,

        "permission_scope_requested": "",
        "permission_scope_allowed": "",
        "permission_scope_status": "within_policy",
        "least_privilege_violation": False,

        "approval_required": False,
        "approval_status": "not_required",
        "approval_actor": "",
        "approval_reason": "",

        "guardrail_action": "allow",
        "detection_family": detection_family,
        "severity": severity,
        "confidence": 0.0,
        "risk_score": risk_score,
        "risk_flags": flags,
        "risk_flags_csv": csv(flags),

        "owasp_category": "MCP",
        "mcp_risk_category": "",
        "agentic_risk_category": "",
        "atlas_techniques": [],
        "expected_wazuh_rule_id": expected_wazuh_rule_id,
    }


def write_event(log_file: str, event: Dict[str, Any]) -> None:
    ensure_parent(log_file)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, separators=(",", ":"), ensure_ascii=False) + "\n")


def write_events(log_file: str, events: List[Dict[str, Any]]) -> None:
    for event in events:
        write_event(log_file, event)
