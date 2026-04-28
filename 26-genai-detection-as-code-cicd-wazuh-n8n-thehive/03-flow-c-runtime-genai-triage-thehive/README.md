# Flow C - Runtime GenAI Triage with Wazuh, Slack, TheHive, and DataTables

Flow C is the runtime AI security workflow. It receives Wazuh alerts generated from AI demo guardrail telemetry, enriches them with GenAI context, notifies Slack, creates/updates TheHive alerts, comments on alerts, promotes high-risk cases, comments on cases, and writes audit/dashboard state.

<p align="center"><img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/26-genai-detection-as-code-cicd-wazuh-n8n-thehive/resources/GitHub%20and%20LinkedIn%20Flow%20C.png" alt="GenAI Detection-as-Code Wazuh Capstone Architecture" width="900"/></p>

## What it solves

AI application abuse can happen at the prompt/context/output layer. Flow C makes that telemetry visible to the SOC by converting app guardrail events into Wazuh detections and then into analyst-ready triage artifacts.

## Main logic

```mermaid
flowchart LR
    App[AI demo app] --> JSONL[/guardrail-events.jsonl/]
    JSONL --> Agent[Wazuh agent localfile]
    Agent --> Manager[Wazuh manager]
    Manager --> Rule{GenAI rules}
    Rule -->|100201| Direct[Direct prompt injection]
    Rule -->|100202| Indirect[Indirect injection]
    Rule -->|100203| Output[Improper output handling]
    Rule --> Integration[custom-n8n-genai]
    Integration --> N8N[Flow C webhook]
    N8N --> Normalize[Normalize Wazuh alert]
    Normalize --> Enrich[OWASP LLM + ATLAS + risk score]
    Enrich --> Hive[TheHive create/update alert]
    Hive --> AlertComment[Create alert comment]
    AlertComment --> Promote{risk_score >= 95?}
    Promote -- yes --> Case[Promote to case template]
    Case --> CaseComment[Create case comment]
    Promote -- no --> Skip[Skip promotion]
    CaseComment --> Slack[Slack alert]
    Skip --> Slack
    Slack --> Tables[Alert/audit/case tables]
    Tables --> Dashboard[Dashboard events]
```

## Detection families

| Rule ID | Family | OWASP | Purpose |
|---|---|---|---|
| `100201` | `genai_prompt_injection` | LLM01 | Direct prompt injection |
| `100202` | `genai_indirect_injection` | LLM01 | Indirect prompt injection / untrusted retrieved context |
| `100203` | `genai_output_handling` | LLM05 | Improper output handling risk |

## Included files

- final Flow C n8n workflow JSON
- AI demo Flask app
- Wazuh decoder and rules
- Wazuh custom integration script
- localfile and manager integration config snippets
- test events and expected rules
- metadata, mappings, schemas, guardrail policy
- Flow C DataTables
- Flow C PDF

## TheHive behavior

Flow C uses TheHive as a true incident-response system:

- Create or update alert by source/sourceRef.
- Add automated alert comment.
- Promote high-risk direct and indirect prompt injection alerts to cases.
- Use separate case templates for direct and indirect prompt injection.
- Add automated case comment after promotion.
- Record case-promotion state in DataTables.

## Validation tests used

- AI demo app service active and health endpoint OK.
- `test_events.sh` generated direct, indirect, improper-output, and benign events.
- Wazuh alerts fired for `100201`, `100202`, and `100203`.
- Slack showed all three alerts.
- TheHive alerts/cases/comments were created.
- Case promotion skipped for lower-risk improper output handling.
- Flow C DataTables and dashboard rows were updated.
