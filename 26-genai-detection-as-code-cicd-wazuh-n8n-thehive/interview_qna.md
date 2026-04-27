# Interview Q&A - GenAI Detection-as-Code CI/CD for Wazuh Capstone

## 1. What problem does this project solve?

It solves the gap between AI application guardrail telemetry and traditional SOC operations. GenAI risks such as prompt injection and unsafe output handling often stay inside application logs. This project turns those events into Wazuh detections, validates detection content through CI, controls deployment through governance, and routes runtime alerts to Slack, TheHive, and audit tables.

## 2. Why did you split the project into Flow A, Flow B, Flow C, and supporting workflows?

The split reduces complexity and mirrors real operations. Flow A is build-time quality control. Flow B is deployment governance. Flow C is runtime detection and incident triage. Supporting workflows provide cross-cutting observability and closure handling. This design makes each flow independently testable while still producing one connected lifecycle.

## 3. What are the main GenAI risks covered?

The MVP covers:

- Direct prompt injection - Wazuh rule 100201
- Indirect prompt injection / untrusted retrieved context - Wazuh rule 100202
- Improper output handling - Wazuh rule 100203

These are mapped to OWASP LLM categories and ATLAS-style context in Flow C.

## 4. How does Flow A improve detection engineering quality?

Flow A validates Wazuh XML, Sigma rules, metadata mappings, staging behavior, and replay tests before content is approved. It records CI runs, changed files, and stage results in DataTables, then posts a GitHub report and Slack notification.

## 5. How does Flow B reduce deployment risk?

Flow B requires a valid deployment signal and PR gates before deploying. It backs up current Wazuh content, checks out the approved commit, stages XML content, runs predeploy checks, activates content, restarts Wazuh, runs a postdeploy test, and has a rollback path.

## 6. How does Flow C detect runtime AI abuse?

The AI demo app writes structured JSONL telemetry to `/var/log/ai-demo/guardrail-events.jsonl`. A Wazuh agent monitors the file and forwards events to the Wazuh manager. Custom rules detect the target GenAI patterns, and a custom integration forwards alerts to n8n Flow C.

## 7. Why use TheHive?

TheHive is used to convert high-fidelity runtime alerts into analyst-manageable alerts and cases. Flow C creates/updates TheHive alerts, adds comments, promotes high-risk alerts to case templates, and Flow D later syncs case closure back into the audit system.

## 8. Why use DataTables instead of a database?

For an MVP, n8n DataTables are lightweight, visible, easy to demo, and sufficient for audit state. In production, I would move the audit/dashboard tables to PostgreSQL or another managed database.

## 9. What was the hardest part?

The hardest part was making the full lifecycle consistent: PR CI, deployment gating, Wazuh ingestion, JSON rule matching, n8n branching, TheHive case templates, Slack formatting, and audit tables all had to align on identifiers such as request ID, rule ID, dedup key, sourceRef, and case ID.

## 10. How would you improve it in production?

I would add branch protection, centralized secrets, TLS everywhere, a persistent database, a formal dashboard UI, more OWASP LLM categories, Wazuh dashboard visualizations, TheHive custom fields, and automated regression tests for every n8n workflow export.
