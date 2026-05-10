from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True)
class ApprovalAssessment:
    approval_required: bool
    approval_status: str
    approval_quality: str
    risk_flags: List[str]


def assess_approval_prompt(prompt: str, approval_status: str, sensitive_action: bool) -> ApprovalAssessment:
    text = (prompt or "").lower()
    flags: List[str] = []
    if any(term in text for term in ["harmless", "routine", "approve quickly", "no risk", "just click"]):
        flags.append("misleading_framing")
    if any(term in text for term in ["urgent", "immediately", "quickly", "without delay"]):
        flags.append("urgency_pressure")
    if sensitive_action and not any(term in text for term in ["external", "send", "resource", "sensitive", "permission"]):
        flags.append("sensitive_action_hidden")
    if approval_status in {"missing", "bypassed", "denied"}:
        flags.append(f"approval_{approval_status}")
    quality = "unsafe" if flags else "clear"
    return ApprovalAssessment(
        approval_required=sensitive_action,
        approval_status=approval_status,
        approval_quality=quality,
        risk_flags=flags,
    )


def format_flags(flags: Iterable[str]) -> str:
    return ",".join(flags)
