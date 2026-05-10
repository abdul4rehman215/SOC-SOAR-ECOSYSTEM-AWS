from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple


class AgenticPolicyEngine:
    def __init__(self, repo_root: str | Path):
        self.repo_root = Path(repo_root)
        policy_dir = self.repo_root / "policies" / "agentic"
        self.bundle = self._load(policy_dir / "agentic_policy_bundle.json")
        self.identity = self._load(policy_dir / "identity_scope_policy.json")
        self.loop = self._load(policy_dir / "loop_threshold_policy.json")
        self.confused_deputy = self._load(policy_dir / "confused_deputy_policy.json")
        self.approval = self._load(policy_dir / "approval_prompt_policy.json")

    @staticmethod
    def _load(path: Path) -> Dict:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)

    @property
    def max_tool_calls(self) -> int:
        return int(self.loop.get("max_tool_calls_per_request", 8))

    @property
    def max_same_tool_repeats(self) -> int:
        return int(self.loop.get("max_same_tool_repeats", 3))

    @property
    def max_plan_steps(self) -> int:
        return int(self.loop.get("max_plan_steps", 8))

    def identity_allowed_scopes(self, identity_used: str) -> List[str]:
        return list(self.identity.get("identities", {}).get(identity_used, {}).get("allowed_scopes", []))

    def permission_status(self, identity_used: str, requested_scopes: List[str]) -> Tuple[str, str]:
        allowed = self.identity_allowed_scopes(identity_used)
        missing = [scope for scope in requested_scopes if scope not in allowed]
        if missing:
            return "exceeds_policy", ",".join(allowed)
        return "within_policy", ",".join(allowed)

    def loop_detected(self, tool_call_count: int, same_tool_repeated_count: int, plan_step_count: int) -> bool:
        return (
            tool_call_count > self.max_tool_calls
            or same_tool_repeated_count > self.max_same_tool_repeats
            or plan_step_count > self.max_plan_steps
        )

    def confused_deputy_violation(self, source_server: str, target_server: str, target_tool: str) -> bool:
        forbidden_pairs = self.confused_deputy.get("forbidden_cross_server_instructions", [])
        for pair in forbidden_pairs:
            if pair.get("source_server") == source_server and pair.get("target_server") == target_server:
                if target_tool in pair.get("target_tools", []):
                    return True
        return False
