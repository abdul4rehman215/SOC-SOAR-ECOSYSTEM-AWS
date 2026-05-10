# V2 Phase 6 Agentic Risk Lab

This lab simulates the agent decision path safely and writes structured JSONL telemetry for Wazuh:

`prompt/user goal -> agent plan -> tool chain -> MCP server sequence -> approval decision -> identity/scope check -> post-block behavior -> output decision`

## Safety boundary

This lab does **not** execute shell commands, send external webhooks, mutate TheHive/cases/tickets, access production secrets, or connect to production MCP servers. All risky activity is simulated and logged as telemetry.

## Scenarios

| Scenario | Expected Wazuh rule | Purpose |
|---|---:|---|
| `benign` | 100350 | Normal agent plan base telemetry only |
| `goal_hijack_from_tool_result` | 100351 | Tool result changes original user goal |
| `plan_drift_to_external_send` | 100352 | Low-risk goal drifts into high-risk tool chain |
| `tool_loop_unbounded` | 100353 | Repeated tool loop exceeds threshold |
| `approval_manipulation` | 100354 | Approval prompt hides/minimizes sensitive action |
| `identity_permission_mismatch` | 100355 | Identity/scope requested exceeds policy |
| `confused_deputy_multi_server` | 100356 | Untrusted server influences privileged server/tool |
| `excessive_agency_rogue_action` | 100357 | Autonomous high-impact action outside role/policy |
| `continued_action_after_blocked_risk` | 100358 | Agent continues after prior MCP/RAG/memory block |

## Local run

```bash
python3 scripts/runtime/run_agentic_scenarios.py --repo-root . --scenario all --log-file /tmp/agentic-events.jsonl
python3 scripts/ci/validate_agentic_phase6.py .
```

Use `/var/log/ai-demo/agentic-events.jsonl` only when running on the Wazuh agent host with the proper localfile configuration.
