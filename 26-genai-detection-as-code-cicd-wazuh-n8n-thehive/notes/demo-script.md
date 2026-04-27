# Demo Script

## 1. Start with the problem

Explain that GenAI app guardrail events usually stay hidden in app logs and do not become proper SOC detections.

## 2. Show Flow A

Open a GitHub PR that changes metadata or detection content. Show the Flow A CI comment, detection-ci-pass label, Slack message, and Flow A DataTables.

## 3. Show Flow B

Show blocked deployment first. Then show an approved deployment run with backup, stage, XML check, smoke test, activation, restart, and postdeploy.

## 4. Show Flow C

Run:

```bash
cd /opt/detection-ci/wazuh-genai-ci
bash app/ai-demo/test_events.sh
```

Then show Slack, Wazuh alerts, TheHive alert, case promotion, alert comments, case comments, and Flow C DataTables.

## 5. Show supporting workflows

Show dashboard rows, dead-letter table, and case closure sync table.

## 6. Close with the architecture

Explain how the system models an actual detection engineering lifecycle from code to detection to case closure.
