from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class SimulatedToolResult:
    tool_name: str
    tool_category: str
    result_excerpt: str
    sensitive: bool = False
    external_action: bool = False
    resource_access: bool = False
    executed: bool = False


class SafeToolSimulator:
    """Safe local mock tools for agentic telemetry.

    This class never executes shell commands, never sends network requests, never mutates
    tickets/cases, and never reads host files. It only returns simulated result text used
    by Phase 6 scenarios.
    """

    TOOL_CATEGORIES: Dict[str, str] = {
        "search_docs": "knowledge_search",
        "read_ticket": "ticket_readonly",
        "get_policy": "policy_readonly",
        "create_case_draft": "case_draft",
        "send_external_webhook_mock": "external_send_mock",
        "run_shell_command_mock": "system_command_mock",
        "read_resource": "resource_read_mock",
        "update_memory_mock": "memory_write_mock",
    }

    SENSITIVE_TOOLS = {
        "send_external_webhook_mock",
        "run_shell_command_mock",
        "read_resource",
        "update_memory_mock",
    }

    def call(self, tool_name: str, args_summary: str = "") -> SimulatedToolResult:
        category = self.TOOL_CATEGORIES.get(tool_name, "unknown")
        sensitive = tool_name in self.SENSITIVE_TOOLS
        external = tool_name == "send_external_webhook_mock"
        resource = tool_name == "read_resource"
        return SimulatedToolResult(
            tool_name=tool_name,
            tool_category=category,
            result_excerpt=f"SIMULATED ONLY: {tool_name} accepted args [{args_summary}] and returned a lab-only result.",
            sensitive=sensitive,
            external_action=external,
            resource_access=resource,
            executed=False,
        )
