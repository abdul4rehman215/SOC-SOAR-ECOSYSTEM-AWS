# Implementation Decisions

## n8n as orchestrator

n8n was selected because each automation step can be inspected visually. This helps with evidence collection, debugging, and portfolio communication.

## Wazuh as detection engine

Wazuh provides custom rule/decoder support, logtest validation, alert JSON output, and manager/agent separation. It fits the detection-as-code story better than a plain log parser.

## JSONL telemetry contract

The AI demo app writes JSONL because Wazuh localfile can ingest it cleanly and it is easy to replay for tests.

## Three GenAI rule families

The MVP intentionally stays scoped to three strong families. This avoids a shallow implementation across too many AI risk categories.

## TheHive sourceRef deduplication

Flow C uses a dedup key based on family/request/rule ID as the TheHive sourceRef. This makes repeat behavior traceable and prevents the workflow from relying only on timestamps.

## DataTables as audit tables

DataTables are simple enough for an MVP while still proving auditability. They are not meant to replace a production database.
