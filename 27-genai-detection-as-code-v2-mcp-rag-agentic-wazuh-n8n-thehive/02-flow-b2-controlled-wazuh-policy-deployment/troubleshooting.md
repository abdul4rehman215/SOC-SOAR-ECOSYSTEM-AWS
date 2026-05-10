# 🧯 🚦 Flow B2 Troubleshooting

## Workflow does not run

Confirm the workflow is published/active and no duplicate workflow is competing for the same webhook/GitHub trigger.

## DataTable node is green but row is missing

Check column types and matching keys. n8n DataTables can appear successful if the row matches an existing record or if a stale schema is cached.

## External action is missing

For GitHub, Slack, or TheHive nodes, reselect credentials after importing the workflow JSON.

## Context disappears after Slack/GitHub nodes

Slack and HTTP nodes return response objects. The workflow must restore previous context before final audit rows.

## MVP limitation

This is a lab prototype. Treat failures as useful engineering evidence and improve the runner, schema, credential, and retry behavior before production.
