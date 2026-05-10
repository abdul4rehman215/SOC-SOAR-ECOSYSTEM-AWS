from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class AgentPlan:
    original_user_goal: str
    observed_agent_goal: str
    agent_plan_id: str
    agent_plan_summary: str
    steps: List[str] = field(default_factory=list)
    tool_sequence: List[str] = field(default_factory=list)
    mcp_server_sequence: List[str] = field(default_factory=list)
    goal_change_source: str = "none"

    @property
    def goal_changed(self) -> bool:
        return self.original_user_goal.strip().lower() != self.observed_agent_goal.strip().lower()

    @property
    def step_count(self) -> int:
        return len(self.steps)

    @property
    def tool_sequence_csv(self) -> str:
        return ",".join(self.tool_sequence)

    @property
    def mcp_server_sequence_csv(self) -> str:
        return ",".join(self.mcp_server_sequence)


def make_plan(
    *,
    original_goal: str,
    observed_goal: str,
    plan_id: str,
    summary: str,
    steps: List[str],
    tools: List[str],
    servers: List[str],
    goal_change_source: str = "none",
) -> AgentPlan:
    return AgentPlan(
        original_user_goal=original_goal,
        observed_agent_goal=observed_goal,
        agent_plan_id=plan_id,
        agent_plan_summary=summary,
        steps=steps,
        tool_sequence=tools,
        mcp_server_sequence=servers,
        goal_change_source=goal_change_source,
    )
