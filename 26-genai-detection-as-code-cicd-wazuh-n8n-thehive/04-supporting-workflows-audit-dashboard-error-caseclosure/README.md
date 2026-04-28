# Supporting Workflows - Audit, Dashboard, Error Handling, and Case Closure

This folder contains the support layer around the three main workflows. These workflows do not replace Flow A, B, or C; they make the prototype observable, resilient, and lifecycle-complete.

<p align="center"><img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/26-genai-detection-as-code-cicd-wazuh-n8n-thehive/resources/GitHub%20supporting%20Flow.png" alt="GenAI Detection-as-Code Wazuh Capstone Architecture" width="900"/></p>

## Included supporting workflows

| Workflow | Purpose |
|---|---|
| SOC Dashboard Event Collector | Receives metric events from Flow A/B/C/D/error workflows and upserts dashboard rows |
| Global Error Dead-Letter Handler | Captures failed workflow executions, inserts dead-letter rows, and notifies Slack |
| Flow D TheHive Case Closure Sync | Polls TheHive for closed Flow C cases and syncs closure outcome to Slack/DataTables/dashboard |

## Support architecture

```mermaid
flowchart LR
    A[Flow A] --> Dash[Dashboard collector]
    B[Flow B] --> Dash
    C[Flow C] --> Dash
    Err[Global error workflow] --> Dead[flow_dead_letter_events]
    Err --> Dash
    Hive[TheHive cases] --> D[Flow D closure sync]
    D --> Slack[Slack closure message]
    D --> Audit[flow_c_audit_events]
    D --> Close[flow_c_case_closure_sync]
    D --> Dash
```

## Why this layer matters

The support workflows prove that the project does not stop at alert creation. It also tracks failures, stores metric events, and syncs case closure outcomes back into the project audit trail.

## Included files

- dashboard collector workflow JSON
- global error workflow JSON
- case closure sync workflow JSON
- dead-letter, dashboard, and case-closure DataTable exports/schemas
- supporting workflows PDF
