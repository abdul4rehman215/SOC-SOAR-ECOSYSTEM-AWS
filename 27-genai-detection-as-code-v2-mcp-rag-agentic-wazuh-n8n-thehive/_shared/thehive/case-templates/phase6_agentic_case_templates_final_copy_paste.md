# Phase 6 TheHive Agentic Case Templates - Final UI Copy/Paste
The screenshots show the TheHive case template form needs Prefix, Name, Display name, TLP, PAP, Severity, Tags, Description, and per-task fields: Group, Title, Mandatory, Description, Assignee, and Flag. Use the following values manually in TheHive.

---

## flowc-agentic-goal-hijack
- **Prefix:** `flowc`
- **Name:** `flowc-agentic-goal-hijack`
- **Display name:** `Flow C2 - Agentic Goal Hijack`
- **TLP:** `TLP:AMBER`
- **PAP:** `PAP:AMBER`
- **Severity:** `CRITICAL`
- **Tags:** `flow-c2,phase-6,agentic-ai,goal-hijack,rule-100351,wazuh,genai`
### Description
Use when the agent original goal changes because of an untrusted tool result, RAG/memory content, approval prompt, or autonomous replanning. Focus on original-vs-observed goal, source of change, tool/server chain, and whether guardrails blocked the risky action.
### Tasks to add

| Group | Title | Mandatory | Flag | Description |
|---|---|---:|---:|---|
| default | Review original and observed goals | Yes | No | Compare original_user_goal and observed_agent_goal; note whether goal_changed=true and the exact goal_change_source. |
| default | Identify influence source | Yes | No | Determine whether the goal change came from tool result, RAG context, memory, approval prompt, or autonomous replanning. |
| default | Review tool and server sequence | Yes | No | Review tool_sequence_csv and mcp_server_sequence_csv for external send, resource read, memory write, or privileged tool path. |
| default | Verify guardrail block | Yes | No | Confirm guardrail_action and whether the risky action was blocked before execution. |
| default | Correlate related alerts | Yes | No | Search same request_id/session_id for MCP, RAG, memory, or post-block alerts. |
| default | Contain and tune | Yes | No | Document containment, policy update, or detection tuning decision. |

---

## flowc-agentic-plan-drift
- **Prefix:** `flowc`
- **Name:** `flowc-agentic-plan-drift`
- **Display name:** `Flow C2 - Agentic Plan Drift / Tool Chain Escalation`
- **TLP:** `TLP:AMBER`
- **PAP:** `PAP:AMBER`
- **Severity:** `CRITICAL`
- **Tags:** `flow-c2,phase-6,agentic-ai,plan-drift,tool-chain-escalation,rule-100352`
### Description
Use when a low-risk user goal evolves into a risky multi-tool chain, external-send path, resource-read path, or high-impact action plan. Focus on plan drift and escalation from the allowed goal.
### Tasks to add

| Group | Title | Mandatory | Flag | Description |
|---|---|---:|---:|---|
| default | Compare user goal and final plan | Yes | No | Compare original_user_goal with agent_plan_summary and observed_agent_goal. |
| default | Find drift step | Yes | No | Identify the step where benign summarization became external-send, resource-read, memory-write, or privileged-tool behavior. |
| default | Review target tools | Yes | No | Review target_tool_name, tool_sequence_csv, and mcp_server_sequence_csv. |
| default | Validate approval and permission | Yes | No | Confirm approval_status, approval_required, permission_scope_status, and guardrail_action. |
| default | Confirm block status | Yes | No | Validate whether external-send/resource-read path was blocked. |
| default | Update plan controls | Yes | No | Record plan-guardrail or tool-policy tuning notes. |

---

## flowc-agentic-tool-loop
- **Prefix:** `flowc`
- **Name:** `flowc-agentic-tool-loop`
- **Display name:** `Flow C2 - Agentic Tool Loop / Unbounded Consumption`
- **TLP:** `TLP:AMBER`
- **PAP:** `PAP:AMBER`
- **Severity:** `HIGH`
- **Tags:** `flow-c2,phase-6,agentic-ai,tool-loop,unbounded-consumption,rule-100353`
### Description
Use when the agent repeatedly calls tools, exceeds total tool-call thresholds, or repeats the same tool beyond policy. Focus on loop controls and resource exhaustion prevention.
### Tasks to add

| Group | Title | Mandatory | Flag | Description |
|---|---|---:|---:|---|
| default | Review loop counters | Yes | No | Compare tool_call_count and same_tool_repeated_count against max_allowed_tool_calls and max_same_tool_repeats. |
| default | Determine loop cause | Yes | No | Decide whether this was benign retry behavior or uncontrolled agent behavior. |
| default | Check sensitive repetitions | Yes | No | Look for repeated sensitive tool attempts, repeated external send, or repeated resource reads. |
| default | Confirm stop action | Yes | No | Verify guardrail_action blocked or stopped the loop. |
| default | Tune thresholds | Yes | No | Record whether loop thresholds need adjustment. |

---

## flowc-agentic-approval-bypass
- **Prefix:** `flowc`
- **Name:** `flowc-agentic-approval-bypass`
- **Display name:** `Flow C2 - Agentic Approval Manipulation / Bypass`
- **TLP:** `TLP:AMBER`
- **PAP:** `PAP:AMBER`
- **Severity:** `HIGH`
- **Tags:** `flow-c2,phase-6,agentic-ai,approval-manipulation,hitl,rule-100354`
### Description
Use when an approval prompt minimizes or hides sensitive action, applies urgency pressure, omits destination/data details, or attempts bypass/missing approval for a sensitive action.
### Tasks to add

| Group | Title | Mandatory | Flag | Description |
|---|---|---:|---:|---|
| default | Review approval prompt | Yes | No | Read approval_prompt_excerpt and identify misleading framing, urgency pressure, or hidden sensitive action. |
| default | Check approval flags | Yes | No | Review approval_prompt_risk_flags_csv and approval_quality. |
| default | Validate approval state | Yes | No | Confirm approval_required and approval_status. |
| default | Confirm sensitive action block | Yes | No | Verify the sensitive action was blocked before execution. |
| default | Update approval policy | Yes | No | Record required approval prompt policy change or tuning note. |

---

## flowc-agentic-identity-mismatch
- **Prefix:** `flowc`
- **Name:** `flowc-agentic-identity-mismatch`
- **Display name:** `Flow C2 - Agentic Identity Permission Mismatch`
- **TLP:** `TLP:AMBER`
- **PAP:** `PAP:AMBER`
- **Severity:** `HIGH`
- **Tags:** `flow-c2,phase-6,agentic-ai,identity-mismatch,least-privilege,rule-100355`
### Description
Use when the agent identity or delegated permission scope exceeds allowed policy. Focus on least privilege, delegated identity misuse, and requested-vs-allowed scope.
### Tasks to add

| Group | Title | Mandatory | Flag | Description |
|---|---|---:|---:|---|
| default | Identify runtime identity | Yes | No | Review identity_used and agent_id. |
| default | Compare scopes | Yes | No | Compare identity_scope_requested, identity_scope_allowed, permission_scope_requested, and permission_scope_allowed. |
| default | Review denied scopes | Yes | No | Identify scopes requested beyond policy. |
| default | Confirm guardrail action | Yes | No | Verify permission_scope_status and guardrail_action. |
| default | Update identity policy | Yes | No | Record identity-scope policy correction or tuning decision. |

---

## flowc-agentic-confused-deputy
- **Prefix:** `flowc`
- **Name:** `flowc-agentic-confused-deputy`
- **Display name:** `Flow C2 - Agentic Confused Deputy Multi-Server`
- **TLP:** `TLP:AMBER`
- **PAP:** `PAP:AMBER`
- **Severity:** `CRITICAL`
- **Tags:** `flow-c2,phase-6,agentic-ai,confused-deputy,multi-server,rule-100356`
### Description
Use when one MCP server/tool result influences the agent to call a different privileged server/tool. Focus on source server, target server, cross-server policy, and blocked action.
### Tasks to add

| Group | Title | Mandatory | Flag | Description |
|---|---|---:|---:|---|
| default | Identify source and target | Yes | No | Review source_mcp_server, target_mcp_server, and target_tool_name. |
| default | Find cross-server instruction | Yes | No | Identify the source tool result or instruction that caused the target call. |
| default | Validate target privilege | Yes | No | Determine whether the target server/tool is privileged or sensitive. |
| default | Check policy decision | Yes | No | Review cross_server_policy_violation and guardrail_action. |
| default | Correlate related MCP alerts | Yes | No | Search same request/session for MCP tool poisoning, resource exfiltration, or sensitive tool alerts. |
| default | Tune isolation controls | Yes | No | Record server isolation or policy tuning notes. |

---

## flowc-agentic-excessive-agency
- **Prefix:** `flowc`
- **Name:** `flowc-agentic-excessive-agency`
- **Display name:** `Flow C2 - Agentic Excessive Agency / Rogue Action`
- **TLP:** `TLP:AMBER`
- **PAP:** `PAP:AMBER`
- **Severity:** `CRITICAL`
- **Tags:** `flow-c2,phase-6,agentic-ai,excessive-agency,rogue-action,rule-100357`
### Description
Use when the agent attempts an autonomous high-impact action outside its role or policy boundary, including external send, case mutation, resource read, command-execution mock, or memory write without explicit approval.
### Tasks to add

| Group | Title | Mandatory | Flag | Description |
|---|---|---:|---:|---|
| default | Review rogue action | Yes | No | Identify autonomous high-impact action and target_tool_name. |
| default | Check impact class | Yes | No | Determine whether case mutation, external send, sensitive resource read, command mock, or memory write was attempted. |
| default | Validate approval | Yes | No | Confirm approval_required and approval_status. |
| default | Confirm execution state | Yes | No | Verify guardrail_action and actual execution status in the safe lab boundary. |
| default | Update agency boundary | Yes | No | Record policy update for allowed/blocked autonomous actions. |

---

## flowc-agentic-continued-after-block
- **Prefix:** `flowc`
- **Name:** `flowc-agentic-continued-after-block`
- **Display name:** `Flow C2 - Agent Continued After Blocked Risk`
- **TLP:** `TLP:AMBER`
- **PAP:** `PAP:AMBER`
- **Severity:** `CRITICAL`
- **Tags:** `flow-c2,phase-6,agentic-ai,continued-after-block,guardrail-bypass,rule-100358`
### Description
Use when the agent continues, replans, or selects an alternate sensitive tool/server after a prior MCP/RAG/memory guardrail block. Focus on bypass-after-block behavior.
### Tasks to add

| Group | Title | Mandatory | Flag | Description |
|---|---|---:|---:|---|
| default | Identify prior block | Yes | No | Review prior_guardrail_blocked and blocked_risk_family. |
| default | Review replanning path | Yes | No | Inspect observed_agent_goal, agent_plan_summary, and tool_sequence_csv after the block. |
| default | Check alternate target | Yes | No | Confirm whether agent chose alternate target_tool_name or target_mcp_server. |
| default | Correlate related alerts | Yes | No | Search same session for MCP, RAG, memory, or agentic prior alerts. |
| default | Tune post-block controls | Yes | No | Record post-block replanning policy update or containment action. |
