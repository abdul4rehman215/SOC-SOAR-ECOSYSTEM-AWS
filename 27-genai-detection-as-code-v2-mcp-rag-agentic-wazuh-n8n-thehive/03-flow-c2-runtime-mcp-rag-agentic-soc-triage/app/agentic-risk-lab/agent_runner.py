from __future__ import annotations

from typing import Dict, List

from scenarios import expected_ids_for, run_scenarios


class AgenticRiskLabRunner:
    """Small wrapper used by scripts and future tests."""

    def __init__(self, repo_root: str):
        self.repo_root = repo_root

    def run(self, scenario: str = "all") -> List[Dict]:
        return run_scenarios(self.repo_root, scenario)

    def expected_rule_ids(self, scenario: str = "all") -> List[int]:
        return expected_ids_for(scenario)
