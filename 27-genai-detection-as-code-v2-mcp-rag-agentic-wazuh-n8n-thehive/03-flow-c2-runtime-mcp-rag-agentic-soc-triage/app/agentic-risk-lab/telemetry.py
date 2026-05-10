from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List


EVENT_SOURCE = "ai_demo_agent_guardrail"
SCHEMA_VERSION = "2.0"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def csv(values: Iterable[str] | str | None) -> str:
    if values is None:
        return ""
    if isinstance(values, str):
        return values
    return ",".join(str(v) for v in values if str(v))


def base_event(
    *,
    event_type: str,
    request_id: str,
    scenario: str,
    detection_family: str,
    severity: str,
    risk_score: int,
    expected_wazuh_rule_id: int,
    risk_flags: List[str] | None = None,
    guardrail_action: str = "allow",
    confidence: float = 0.0,
) -> Dict[str, Any]:
    risk_flags = risk_flags or []
    return {
        "schema_version": SCHEMA_VERSION,
        "timestamp": utc_now(),
        "event_source": EVENT_SOURCE,
        "event_type": event_type,
        "request_id": request_id,
        "session_id": "sess-agent-demo-001",
        "user_id": "student-user-demo",
        "agent_id": "agent-demo-001",
        "model": "demo-llm-local-sim",
        "policy_bundle_version": "phase6-agentic-v1",
        "policy_bundle_hash": "sha256:phase6-agentic-demo-policy-bundle",
        "environment": "lab",
        "app_name": "ai-demo-v2-agentic-risk-lab",
        "scenario": scenario,
        "guardrail_action": guardrail_action,
        "detection_family": detection_family,
        "severity": severity,
        "confidence": confidence,
        "risk_score": risk_score,
        "risk_flags": risk_flags,
        "risk_flags_csv": csv(risk_flags),
        "owasp_category": "none" if detection_family == "none" else "LLM01",
        "mcp_risk_category": "none",
        "agentic_risk_category": "none" if detection_family == "none" else detection_family,
        "atlas_techniques": [],
        "expected_wazuh_rule_id": expected_wazuh_rule_id,
    }


def write_events(log_file: str | Path, events: Iterable[Dict[str, Any]]) -> None:
    path = Path(log_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        for event in events:
            fh.write(json.dumps(event, sort_keys=True) + "\n")
