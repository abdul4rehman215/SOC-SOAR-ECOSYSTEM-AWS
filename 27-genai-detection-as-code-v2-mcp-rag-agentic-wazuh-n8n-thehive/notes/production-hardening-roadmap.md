# 🏭 Production Hardening Roadmap

## Security

- Replace local `.env.ci` with vault-backed secrets.
- Use scoped GitHub tokens or GitHub App credentials.
- Harden SSH deployment with forced commands and least privilege.
- Add source authentication to runtime telemetry.

## Reliability

- Replace DataTables with PostgreSQL or a SIEM data lake.
- Add retries and dead-letter queues for Slack/TheHive failures.
- Add end-to-end idempotency keys.
- Add workflow unit tests and regression fixtures.

## Detection engineering

- Expand rule coverage and test corpora.
- Add canary deployment for Wazuh rules.
- Add per-rule FP tracking and automatic tuning issue generation.

## Incident response

- Standardize TheHive closure reasons.
- Add escalation paths and ownership mapping.
- Add analyst feedback loop to Flow G.
