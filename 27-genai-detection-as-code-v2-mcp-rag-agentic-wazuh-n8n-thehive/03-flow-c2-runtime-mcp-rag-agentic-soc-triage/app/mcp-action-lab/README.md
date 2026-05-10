# V2 Local MCP Action Lab

This lab creates a safe local MCP-style action path for the GenAI Detection-as-Code V2 MVP.

It replaces pure mock JSON generation with a real local client/server/tool execution loop:

```text
scenario runner
-> local MCP-style client
-> local MCP-style server
-> safe mock tools/resources
-> policy evaluation
-> MCP telemetry JSONL
-> Wazuh rules 100301-100306
-> Flow C2 n8n / TheHive / Slack / DataTables
```

## Safety boundary

This lab never performs destructive actions.

- `send_external_webhook_mock` does not send network traffic.
- `run_shell_command_mock` does not execute shell commands.
- `create_case_draft` creates only a local mock draft result.
- `read_resource` serves only controlled mock resource content and blocks forbidden URI examples.
- All risky behavior is simulated and logged for Wazuh detection.

## Main entrypoint

Use:

```bash
python3 scripts/runtime/run_mcp_action_scenarios.py --scenario all --repo-root . --log-file /var/log/ai-demo/mcp-events.jsonl
```
