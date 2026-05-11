# 🚦 Flow B2 - Controlled Wazuh + AI Security Policy Deployment

Flow B2 is the controlled deployment gate. It only deploys Wazuh content and AI security policy bundles after Flow A2 has passed and the PR has the required approval/deploy signal.

<p align="center"><img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/27-genai-detection-as-code-v2-mcp-rag-agentic-wazuh-n8n-thehive/resources/Flow%20B2%20github.png" alt="GenAI Detection-as-Code Wazuh Capstone Architecture" width="900"/></p>

## 🎯 Purpose

Flow B2 reduces deployment risk by enforcing labels, approval, and a valid `/deploy-lab` signal before staging and activating Wazuh rules/decoders and MCP/RAG/agentic policy bundles.

## 🧩 Workflow logic

```mermaid
flowchart LR
  PR[GitHub PR event/comment] --> State[Get PR state]
  State --> Gate[Check labels + approval]
  Gate -->|blocked| Block[GitHub + Slack blocked report]
  Gate -->|allowed| Deploy[Run B2 deployment runner]
  Deploy --> Parse[Parse deployment result]
  Parse --> Report[GitHub + Slack deployment report]
  Report --> Tables[Deployment + policy bundle DataTables]
```

## ✅ Tested evidence

- Failed PR deployment was blocked before touching Wazuh.
- Approved pass-labeled PR deployed successfully.
- GitHub comment, Slack, backup path, stage results, and DataTables were captured.

## 📂 Important files

- `n8n-workflows/Flow_B2_Controlled_Wazuh_AI_Security_Deployment_FINAL_V5_WORKFLOW_WITH_V7_RUNNER.json`
- `scripts/deploy/run_flow_b2_local_deploy.py`
- `scripts/deploy/rollback_wazuh_and_policy_bundle.sh`
- `config/env.ci.example`
- `data-tables/schemas/flow_b2_deployment_runs_schema.csv`
- `data-tables/schemas/flow_v2_policy_bundle_deployments_schema.csv`
- `artifacts/02_Flow_B2_Controlled_Wazuh_Policy_Deployment_Premium.pdf`

## 🏭 Production improvements

Replace lab SSH deployment with a hardened deployment runner, signed artifacts, canary Wazuh rule deployment, formal rollback testing, and stronger approval enforcement.
