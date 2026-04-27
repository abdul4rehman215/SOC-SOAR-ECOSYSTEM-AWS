# AI Demo App

The AI demo app emits schema-aligned guardrail telemetry for Flow C.

It writes JSONL events to:

```text
/var/log/ai-demo/guardrail-events.jsonl
```

Routes:

- `/demo/direct-prompt-injection` -> expected Wazuh rule 100201
- `/demo/indirect-injection` -> expected Wazuh rule 100202
- `/demo/improper-output-handling` -> expected Wazuh rule 100203
- `/demo/benign` -> non-target/base behavior
- `/health` -> service health check

Run local test:

```bash
cd /opt/detection-ci/wazuh-genai-ci
bash app/ai-demo/test_events.sh
```
