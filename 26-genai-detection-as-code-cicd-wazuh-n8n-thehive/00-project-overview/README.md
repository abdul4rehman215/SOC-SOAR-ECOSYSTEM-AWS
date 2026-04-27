# Project Overview - GenAI Detection-as-Code CI/CD for Wazuh

This overview folder explains the full capstone prototype as one connected SOC engineering lifecycle.

## Scope

The project covers:

- Detection CI validation for GenAI Wazuh content
- Controlled Wazuh deployment
- Runtime AI application telemetry ingestion
- Wazuh custom rules and decoder
- n8n triage and enrichment
- Slack analyst notifications
- TheHive alert/case handling
- Dashboard, error, and closure-support workflows

## Architecture summary

```mermaid
flowchart TB
    Repo[GitHub repository] --> A[Flow A: detection CI]
    A --> B[Flow B: controlled deployment]
    B --> W[Wazuh manager]
    App[AI demo app] --> Agent[Wazuh agent]
    Agent --> W
    W --> C[Flow C: runtime GenAI triage]
    C --> Slack[Slack]
    C --> Hive[TheHive]
    C --> Tables[DataTables]
    Hive --> D[Flow D: closure sync]
    A --> Dash[Dashboard collector]
    B --> Dash
    C --> Dash
    D --> Dash
    Err[Global error workflow] --> Dash
```

## Why this belongs as a capstone

This project combines build-time detection engineering, deployment governance, runtime AI security telemetry, and incident-response operations. Each layer is independently explainable but also contributes to a full prototype.

## Main artifact

See `artifacts/GenAI_Detection_as_Code_CICD_for_Wazuh_Project_Overview.pdf` for the visual project walkthrough.
