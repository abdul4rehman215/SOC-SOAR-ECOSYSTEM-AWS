# 🧠 GenAI Detection-as-Code V2 — MCP, RAG/Memory, Agentic AI Security Operations

### Wazuh + n8n + TheHive + Slack + GitHub prototype for AI runtime security, detection CI/CD, policy deployment, regression analytics, and SOC posture metrics.

<p align="center">
  <a href="https://www.linkedin.com/in/abdul4rehman215/"><img src="https://img.shields.io/badge/LinkedIn-abdul4rehman215-0A66C2?style=for-the-badge&logo=linkedin" alt="LinkedIn"></a>
  <a href="https://github.com/abdul4rehman215"><img src="https://img.shields.io/badge/GitHub-abdul4rehman215-111827?style=for-the-badge&logo=github" alt="GitHub"></a>
  <img src="https://img.shields.io/badge/Project-Capstone%20MVP%20V2-7C3AED?style=for-the-badge" alt="Project Type">
  <img src="https://img.shields.io/badge/Domain-GenAI%20Security%20Operations-FF6B00?style=for-the-badge" alt="Domain">
  <img src="https://img.shields.io/badge/Frameworks-OWASP%20GenAI%20%7C%20MCP%20%7C%20ATLAS--Inspired-22C55E?style=for-the-badge" alt="Framework Alignment">
  <img src="https://img.shields.io/badge/Stack-Wazuh%20%7C%20n8n%20%7C%20TheHive%20%7C%20Slack%20%7C%20GitHub-0EA5E9?style=for-the-badge" alt="Stack">
</p>

<p align="center">
  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/genai-rag-mcp-agenticai-v2.png" alt="GENAI LOGOS" width="900"/>
</p>

---

## 🎯 Problem vs solution

Enterprise AI applications are no longer just chat boxes. Modern GenAI systems can call tools, read MCP resources, retrieve RAG context, write memory, request approvals, and execute multi-step agent plans. Traditional SOC pipelines usually detect host, network, cloud, and identity events, but the AI **action path** often stays inside the application layer.

This capstone MVP V2 extends the previous GenAI Detection-as-Code CI/CD project into a broader **AI Security Operations prototype**. V1 focused mainly on prompt/output detection rules and a classic detection CI/CD lifecycle. V2 expands that model to protect the full GenAI runtime stack:

```text
prompt → agent plan → MCP tool discovery/call/result → RAG retrieval → memory write → approval decision → SOC triage
```

The prototype connects GitHub PR validation, controlled Wazuh deployment, runtime MCP/RAG/agentic detections, TheHive case handling, Slack notifications, n8n DataTables, regression tests, false-positive analytics, and dashboard metrics into one portfolio-ready security engineering system.

Framework-wise, this project is best described as **OWASP GenAI / OWASP LLM-aligned, partially OWASP MCP-aligned, and MITRE ATLAS-inspired**. It does not claim full OWASP compliance or a complete ATLAS technique matrix implementation. Instead, it uses those frameworks as practical security design references for AI-specific detection engineering and SOC automation.

---

## 📑 Table of contents

- [What this project proves](#-what-this-project-proves)
- [Architecture](#-architecture)
- [Workflow map](#-workflow-map)
- [Core technologies used](#-core-technologies-used)
- [OWASP and MITRE ATLAS alignment](#-owasp-and-mitre-atlas-alignment)
- [SOC value and expected impact](#-soc-value-and-expected-impact)
- [Repository layout](#-repository-layout)
- [Included artifacts](#-included-artifacts)
- [Zero-to-hero usage guide](#-zero-to-hero-usage-guide)
- [Main workflow summaries](#-main-workflow-summaries)
- [Data model](#-data-model)
- [Validation evidence](#-validation-evidence)
- [Prototype boundaries and honest limitations](#-prototype-boundaries-and-honest-limitations)
- [Production-hardening roadmap](#-production-hardening-roadmap)
- [Future improvements](#-future-improvements)
- [Interview talking points](#-interview-talking-points)
- [Security notes](#-security-notes)

---

## 🧪 What this project proves

| Capability | Demonstrated by |
|---|---|
| 🧬 AI-security detection engineering | Wazuh custom decoders/rules for MCP, RAG/memory, and agentic runtime threats |
| 🔁 Detection-as-code | Flow A2 validates Wazuh XML, schemas, MCP policy, RAG policy, agentic policy, mappings, DataTable schemas, and replay harness results |
| 🚦 Controlled deployment | Flow B2 gates deployment using A2 pass labels, approval, and `/deploy-lab` before staging/activating Wazuh and policy bundles |
| 🧠 Runtime SOC triage | Flow C2 receives Wazuh alerts and creates Slack + TheHive + DataTable evidence for MCP/RAG/agentic events |
| 🧰 Direct policy monitoring | Flow E monitors MCP policy events directly from app/policy layer before full Wazuh integration |
| 🧪 Regression engineering | Flow F replays red-team event corpora and tracks expected rule misses/unexpected alerts |
| 📉 Tuning analytics | Flow G computes false-positive and closure analytics for noisy rules and recommendations |
| 📊 SOC posture board | Dashboard rollup aggregates CI, deployment, runtime, regression, and FP metrics |
| 🧾 Documentation-first portfolio | Five PDF reports, workflow exports, scripts, case templates, schemas, configs, interview notes, and troubleshooting guides |

---

## 🏗️ Architecture

<p align="center">
  <img src="resources/genai-detection-v2-master-architecture.png" alt="GenAI Detection-as-Code V2 master architecture placeholder" width="900"/>
</p>


```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
    "background": "#030712",
    "fontSize": "26px",
    "primaryTextColor": "#ffffff",
    "lineColor": "#f8fafc"
  },
  "flowchart": {
    "nodeSpacing": 42,
    "rankSpacing": 54,
    "curve": "basis"
  }
}}%%

flowchart LR

    %% =====================================================
    %% COLUMN 1 — SECURITY CONTENT CI + DEPLOYMENT
    %% =====================================================
    subgraph CI[" "]
        direction TB

        H1["🧪 1 · SECURITY CONTENT CI"]

        Dev["👨‍💻 Security Engineer"]

        PR["🐙 GitHub PR"]

        A2["⚡ Flow A2<br/>AI Security Content CI"]

        PASS["✅ CI PASS<br/>Labels + Approval"]

        B2["🚀 Flow B2<br/>Controlled Wazuh<br/>+ Policy Deployment"]

        H1 --> Dev --> PR --> A2 --> PASS --> B2
    end


    %% =====================================================
    %% COLUMN 2 — TELEMETRY + WAZUH
    %% =====================================================
    subgraph WAZ[" "]
        direction TB

        H2["🛡️ 2 · TELEMETRY + WAZUH"]

        MCP["🔧 MCP Action Lab"]
        RAG["🧠 RAG / Memory Lab"]
        AGT["🤖 Agentic-Risk Lab"]

        LOG1["📄 mcp-events.jsonl"]
        LOG2["📄 rag-memory-events.jsonl"]
        LOG3["📄 agentic-events.jsonl"]

        HOST["📥 Wazuh Agent<br/>localfile Ingestion"]

        MAN["🛡️ Wazuh Manager<br/>Rules + Decoders Active"]

        H2 --> MCP --> LOG1
        H2 --> RAG --> LOG2
        H2 --> AGT --> LOG3

        LOG1 --> HOST
        LOG2 --> HOST
        LOG3 --> HOST

        HOST --> MAN
    end


    %% =====================================================
    %% COLUMN 3 — SOC AUTOMATION
    %% =====================================================
    subgraph AUTO[" "]
        direction TB

        H3["🧠 3 · SOC AUTOMATION"]

        C2["⚙️ Flow C2<br/>Runtime MCP / RAG / Agentic<br/>SOC Triage"]

        E["🛡️ Flow E<br/>MCP Policy Monitor"]

        F["🧨 Flow F<br/>Red-Team Regression"]

        G["📊 Flow G<br/>False Positive Analytics"]

        ROUTE["🔀 OUTPUT ROUTING<br/>Alert · Case · Audit · Metrics"]

        H3 --> C2
        H3 --> E
        H3 --> F
        H3 --> G

        C2 --> ROUTE
        E --> ROUTE
        F --> ROUTE
        G --> ROUTE
    end


    %% =====================================================
    %% COLUMN 4 — SOC OUTPUTS
    %% =====================================================
    subgraph OUTPUT[" "]
        direction TB

        H4["📡 4 · SOC OUTPUTS"]

        SLACK["💬 Slack<br/>SOC Channel"]

        HIVE["🐝 TheHive 5<br/>Alerts + Cases"]

        TABLES["📋 n8n DataTables<br/>Alert + Audit + Case State"]

        DASH["📈 Dashboard<br/>Rollup"]

        FINAL["✅ SOC VISIBILITY<br/>Alerts · Cases · Metrics"]

        H4 --> SLACK
        H4 --> HIVE
        H4 --> TABLES

        TABLES --> DASH
        DASH --> FINAL
    end


    %% =====================================================
    %% KEEP ALL FOUR COLUMNS PARALLEL
    %% =====================================================
    CI ==> WAZ
    WAZ ==> AUTO
    AUTO ==> OUTPUT


    %% =====================================================
    %% PREMIUM HEADERS
    %% =====================================================
    classDef ciHeader fill:#082f49,stroke:#67e8f9,stroke-width:6px,color:#ffffff,font-size:30px;
    classDef wazHeader fill:#312e81,stroke:#a78bfa,stroke-width:6px,color:#ffffff,font-size:30px;
    classDef autoHeader fill:#581c87,stroke:#e879f9,stroke-width:6px,color:#ffffff,font-size:30px;
    classDef outHeader fill:#14532d,stroke:#86efac,stroke-width:6px,color:#ffffff,font-size:30px;

    class H1 ciHeader;
    class H2 wazHeader;
    class H3 autoHeader;
    class H4 outHeader;


    %% =====================================================
    %% CI / DEPLOYMENT COLORS
    %% =====================================================
    classDef engineer fill:#172554,stroke:#60a5fa,stroke-width:5px,color:#ffffff,font-size:26px;
    classDef github fill:#1e3a8a,stroke:#818cf8,stroke-width:5px,color:#ffffff,font-size:26px;
    classDef flowA fill:#075985,stroke:#38bdf8,stroke-width:5px,color:#ffffff,font-size:26px;
    classDef pass fill:#166534,stroke:#86efac,stroke-width:5px,color:#ffffff,font-size:26px;
    classDef deploy fill:#4338ca,stroke:#a5b4fc,stroke-width:5px,color:#ffffff,font-size:26px;

    class Dev engineer;
    class PR github;
    class A2 flowA;
    class PASS pass;
    class B2 deploy;


    %% =====================================================
    %% TELEMETRY + WAZUH COLORS
    %% =====================================================
    classDef lab1 fill:#7c2d12,stroke:#fb923c,stroke-width:5px,color:#ffffff,font-size:25px;
    classDef lab2 fill:#4c1d95,stroke:#c084fc,stroke-width:5px,color:#ffffff,font-size:25px;
    classDef lab3 fill:#0f766e,stroke:#5eead4,stroke-width:5px,color:#ffffff,font-size:25px;

    classDef log fill:#1f2937,stroke:#94a3b8,stroke-width:4px,color:#ffffff,font-size:24px;

    classDef agent fill:#0c4a6e,stroke:#38bdf8,stroke-width:5px,color:#ffffff,font-size:26px;
    classDef manager fill:#083344,stroke:#22d3ee,stroke-width:6px,color:#ffffff,font-size:27px;

    class MCP lab1;
    class RAG lab2;
    class AGT lab3;

    class LOG1,LOG2,LOG3 log;
    class HOST agent;
    class MAN manager;


    %% =====================================================
    %% SOC AUTOMATION COLORS
    %% =====================================================
    classDef c2 fill:#7e22ce,stroke:#f0abfc,stroke-width:5px,color:#ffffff,font-size:26px;
    classDef monitor fill:#312e81,stroke:#818cf8,stroke-width:5px,color:#ffffff,font-size:25px;
    classDef regression fill:#991b1b,stroke:#fb7185,stroke-width:5px,color:#ffffff,font-size:25px;
    classDef analytics fill:#0f766e,stroke:#5eead4,stroke-width:5px,color:#ffffff,font-size:25px;
    classDef routing fill:#854d0e,stroke:#fde047,stroke-width:5px,color:#ffffff,font-size:26px;

    class C2 c2;
    class E monitor;
    class F regression;
    class G analytics;
    class ROUTE routing;


    %% =====================================================
    %% SOC OUTPUT COLORS
    %% =====================================================
    classDef slack fill:#7e22ce,stroke:#e879f9,stroke-width:5px,color:#ffffff,font-size:26px;
    classDef hive fill:#854d0e,stroke:#fde047,stroke-width:5px,color:#ffffff,font-size:26px;
    classDef tables fill:#0369a1,stroke:#7dd3fc,stroke-width:5px,color:#ffffff,font-size:26px;
    classDef dash fill:#0f766e,stroke:#5eead4,stroke-width:5px,color:#ffffff,font-size:26px;
    classDef final fill:#166534,stroke:#86efac,stroke-width:6px,color:#ffffff,font-size:27px;

    class SLACK slack;
    class HIVE hive;
    class TABLES tables;
    class DASH dash;
    class FINAL final;


    %% =====================================================
    %% GLOSSY PARALLEL PANELS
    %% =====================================================
    style CI fill:#06131d,stroke:#22d3ee,stroke-width:4px
    style WAZ fill:#0d1022,stroke:#818cf8,stroke-width:4px
    style AUTO fill:#160b25,stroke:#e879f9,stroke-width:4px
    style OUTPUT fill:#07140d,stroke:#4ade80,stroke-width:4px


    %% =====================================================
    %% THICK BRIGHT CONNECTORS
    %% =====================================================
    linkStyle default stroke:#f8fafc,stroke-width:4px;
```

### Runtime path

```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
    "background": "#030712",
    "fontSize": "27px",
    "primaryTextColor": "#ffffff",
    "lineColor": "#f8fafc"
  },
  "flowchart": {
    "nodeSpacing": 46,
    "rankSpacing": 56,
    "curve": "basis"
  }
}}%%

flowchart LR

    %% =====================================================
    %% 1 · RUNTIME SOURCE
    %% =====================================================
    subgraph SOURCE[" "]
        direction TB

        H1["⚡ 1 · RUNTIME SOURCE"]

        A["🧪 MCP / RAG /<br/>Agentic Lab"]

        B["📝 Structured JSONL<br/>Runtime Event"]

        C["📤 Event Written<br/>to Local Log"]

        H1 --> A --> B --> C
    end


    %% =====================================================
    %% 2 · WAZUH DETECTION
    %% =====================================================
    subgraph WAZUH[" "]
        direction TB

        H2["🛡️ 2 · WAZUH DETECTION"]

        D["📥 Wazuh Agent<br/>Localfile Ingestion"]

        E["🛡️ Wazuh Manager"]

        F["🎯 Rule Matching<br/>MCP · RAG · Agentic"]

        G["🚨 Custom Integration<br/>Alert Webhook"]

        H2 --> D --> E --> F --> G
    end


    %% =====================================================
    %% 3 · n8n SOC TRIAGE
    %% =====================================================
    subgraph TRIAGE[" "]
        direction TB

        H3["🧠 3 · SOC TRIAGE"]

        I["⚙️ n8n Flow C2<br/>Receive Alert"]

        J["🧹 Normalize<br/>+ Classify Domain"]

        K["📊 Score + Enrich<br/>Security Context"]

        L["🧬 Deduplicate<br/>+ Prepare Output"]

        H3 --> I --> J --> K --> L
    end


    %% =====================================================
    %% 4 · SOC OUTPUTS
    %% =====================================================
    subgraph OUTPUT[" "]
        direction TB

        H4["📡 4 · SOC OUTPUTS"]

        M["🐝 TheHive 5<br/>Create / Update Alert<br/>Promote High-Risk Case"]

        N["💬 Slack<br/>Analyst-Readable Alert"]

        O["📋 DataTables<br/>MCP · RAG · Agentic<br/>Audit + Case Rows"]

        P["✅ SOC VISIBILITY<br/>Case · Alert · Audit State"]

        H4 --> M
        H4 --> N
        H4 --> O

        M --> P
        N --> P
        O --> P
    end


    %% =====================================================
    %% KEEP THE 4 COLUMNS PARALLEL
    %% =====================================================
    SOURCE ==> WAZUH
    WAZUH ==> TRIAGE
    TRIAGE ==> OUTPUT


    %% =====================================================
    %% PREMIUM GLOSSY HEADERS
    %% =====================================================
    classDef sourceHeader fill:#0c4a6e,stroke:#67e8f9,stroke-width:6px,color:#ffffff,font-size:31px;
    classDef wazuhHeader fill:#312e81,stroke:#a78bfa,stroke-width:6px,color:#ffffff,font-size:31px;
    classDef triageHeader fill:#581c87,stroke:#e879f9,stroke-width:6px,color:#ffffff,font-size:31px;
    classDef outputHeader fill:#14532d,stroke:#86efac,stroke-width:6px,color:#ffffff,font-size:31px;

    class H1 sourceHeader;
    class H2 wazuhHeader;
    class H3 triageHeader;
    class H4 outputHeader;


    %% =====================================================
    %% RUNTIME SOURCE
    %% =====================================================
    classDef lab fill:#172554,stroke:#60a5fa,stroke-width:5px,color:#ffffff,font-size:27px;

    classDef json fill:#075985,stroke:#22d3ee,stroke-width:5px,color:#ffffff,font-size:27px;

    classDef event fill:#134e4a,stroke:#2dd4bf,stroke-width:5px,color:#ffffff,font-size:27px;

    class A lab;
    class B json;
    class C event;


    %% =====================================================
    %% WAZUH
    %% =====================================================
    classDef agent fill:#1e3a8a,stroke:#60a5fa,stroke-width:5px,color:#ffffff,font-size:27px;

    classDef manager fill:#083344,stroke:#22d3ee,stroke-width:6px,color:#ffffff,font-size:28px;

    classDef rules fill:#713f12,stroke:#fbbf24,stroke-width:5px,color:#ffffff,font-size:27px;

    classDef webhook fill:#991b1b,stroke:#fb7185,stroke-width:5px,color:#ffffff,font-size:27px;

    class D agent;
    class E manager;
    class F rules;
    class G webhook;


    %% =====================================================
    %% TRIAGE
    %% =====================================================
    classDef flow fill:#7e22ce,stroke:#f0abfc,stroke-width:6px,color:#ffffff,font-size:28px;

    classDef normalize fill:#4c1d95,stroke:#c084fc,stroke-width:5px,color:#ffffff,font-size:27px;

    classDef enrich fill:#4338ca,stroke:#a5b4fc,stroke-width:5px,color:#ffffff,font-size:27px;

    classDef dedupe fill:#0f766e,stroke:#5eead4,stroke-width:5px,color:#ffffff,font-size:27px;

    class I flow;
    class J normalize;
    class K enrich;
    class L dedupe;


    %% =====================================================
    %% SOC OUTPUTS
    %% =====================================================
    classDef hive fill:#854d0e,stroke:#fde047,stroke-width:5px,color:#ffffff,font-size:27px;

    classDef slack fill:#7e22ce,stroke:#e879f9,stroke-width:5px,color:#ffffff,font-size:27px;

    classDef tables fill:#0369a1,stroke:#7dd3fc,stroke-width:5px,color:#ffffff,font-size:27px;

    classDef final fill:#166534,stroke:#86efac,stroke-width:6px,color:#ffffff,font-size:28px;

    class M hive;
    class N slack;
    class O tables;
    class P final;


    %% =====================================================
    %% GLOSSY PARALLEL PANELS
    %% =====================================================
    style SOURCE fill:#06131d,stroke:#22d3ee,stroke-width:4px
    style WAZUH fill:#0d1022,stroke:#818cf8,stroke-width:4px
    style TRIAGE fill:#160b25,stroke:#e879f9,stroke-width:4px
    style OUTPUT fill:#07140d,stroke:#4ade80,stroke-width:4px


    %% =====================================================
    %% BRIGHT CONNECTORS
    %% =====================================================
    linkStyle default stroke:#f8fafc,stroke-width:5px;
```

---

## 🗺️ Workflow map

| Folder | Workflow | Purpose | Status |
|---|---|---|---|
| `01-flow-a2-ai-security-content-ci/` | Flow A2 | GitHub PR-triggered AI-security CI gate | ✅ Tested PASS + FAIL |
| `02-flow-b2-controlled-wazuh-policy-deployment/` | Flow B2 | Controlled Wazuh + policy deployment | ✅ Tested BLOCKED + DEPLOYED |
| `03-flow-c2-runtime-mcp-rag-agentic-soc-triage/` | Flow C2 | Runtime SOC triage for MCP, RAG/memory, agentic AI | ✅ Tested C1/C2/C3 |
| `04-supporting-workflows-efg-dashboard-analytics/` | Flow E/F/G/Dashboard | Policy monitor, regression, FP analytics, metrics rollup | ✅ Tested support layer |
| `00-project-overview/` | Master overview | Project narrative, evidence pack, launch material | ✅ Portfolio-ready |

The flows are intentionally separated instead of being forced into one giant canvas. Flow A2 validates content before deployment, Flow B2 controls rollout, Flow C2 handles runtime SOC response, and the supporting workflows provide engineering feedback loops for monitoring, regression, tuning, and dashboard visibility.

---

## 🧰 Core technologies used

| Tool / platform | Role in this project |
|---|---|
| **GitHub Pull Requests** | Source-control entry point for AI-security content changes, PR comments, labels, approval state, and deployment signals |
| **n8n** | Main orchestration layer for GitHub triggers, CI reporting, deployment gating, Slack reporting, TheHive actions, Wazuh alert routing, DataTables, and supporting analytics workflows |
| **Wazuh Manager** | SIEM/detection layer for custom MCP, RAG/memory, and agentic runtime telemetry using custom rules and decoders |
| **Wazuh Agent** | Runtime collector that reads JSONL lab/application telemetry and forwards it to the Wazuh manager |
| **Custom Wazuh rules and decoders** | Detection content for MCP abuse, RAG/memory poisoning, agentic policy violations, prompt/context manipulation, and AI security event normalization |
| **TheHive 5** | Alert/case-management layer for high-risk runtime events, case templates, alert comments, case promotion, and analyst follow-up |
| **Slack** | Analyst-facing notification channel for CI results, blocked/deployed decisions, runtime alerts, regression reports, false-positive analytics, and dashboard rollups |
| **n8n DataTables** | Prototype state/audit layer for CI runs, changed files, stage results, deployment runs, runtime events, policy violations, case promotions, regression metrics, FP analytics, and dashboard summaries |
| **Python / Bash** | Local runners and helper scripts for Flow A2 validation, Flow B2 deployment, runtime event generation, regression replay, and policy analytics |
| **MCP/RAG/Agentic demo lab** | Controlled test environment used to generate realistic AI security telemetry without relying on a production AI application |
| **OWASP GenAI / LLM Top 10** | Main AI security reference for prompt injection, insecure output/tool handling, supply-chain risk, sensitive disclosure, and excessive agency style controls |
| **OWASP MCP Top 10** | MCP-specific reference for tool poisoning, command execution, context injection/over-sharing, audit/telemetry, and protocol-layer governance |
| **MITRE ATLAS-style mapping** | AI threat-modeling language used to describe adversarial AI behavior and make runtime alerts more analyst-readable |

---

## 🧭 OWASP and MITRE ATLAS alignment

This project uses OWASP and MITRE ATLAS as **security design and explanation frameworks**, not as a formal compliance certification.

### OWASP GenAI / OWASP LLM alignment

The strongest alignment is with **OWASP Top 10 for LLM Applications / OWASP GenAI Security** because the project focuses on AI application behavior, tool use, retrieved context, memory writes, and agentic decisions.

| OWASP LLM / GenAI risk family | Where it appears in the project |
|---|---|
| **LLM01 — Prompt Injection** | Flow C2 runtime triage, MCP/context test events, prompt policy checks, Slack/TheHive analyst summaries |
| **LLM02 — Insecure Output Handling** | Policy validation and runtime handling for unsafe tool/action outcomes and downstream AI-generated behavior |
| **LLM03 — Data / memory poisoning style risk** | RAG/memory tests, memory-write telemetry, RAG-memory DataTables, TheHive case evidence |
| **LLM05 — Supply Chain Vulnerabilities** | Flow A2 policy/content validation, tool schema hash checks, Flow B2 controlled deployment and policy bundle rollout |
| **LLM06 — Sensitive Information Disclosure** | MCP/RAG/agentic event enrichment and audit trails where risky context or memory exposure needs analyst review |
| **LLM07 — Insecure Plugin / Tool Design** | MCP tool discovery/call/result monitoring, tool schema hash validation, MCP policy violation routing |
| **LLM08 — Excessive Agency** | Agentic plan/goal risk detection, approval policy checks, agentic incident and plan-step DataTables |
| **LLM09 — Overreliance** | Workflow design keeps human approval gates, deployment labels, TheHive review, and analyst-facing context instead of silent automated trust |

### OWASP MCP alignment

The project also partially maps to **OWASP MCP Top 10** because Flow C2 and Flow E specifically handle MCP action telemetry and policy events.

| OWASP MCP risk family | Project coverage |
|---|---|
| **MCP03 — Tool Poisoning** | Tool schema/hash validation, MCP policy bundle checks, MCP runtime alert classification |
| **MCP04 — Software Supply Chain / Dependency Tampering** | Flow A2 CI validation and Flow B2 controlled deployment for policy/rule bundles |
| **MCP05 — Command Injection & Execution** | MCP action telemetry and high-risk tool/action scenarios routed to Slack/TheHive/DataTables |
| **MCP06 / MCP10 — Context injection and over-sharing** | RAG/context/memory events, MCP context handling, runtime triage evidence, analyst notes |
| **MCP08 — Lack of Audit and Telemetry** | DataTables, Slack notifications, TheHive alerts/cases, dashboard rollup, and supporting policy monitor workflow |

### MITRE ATLAS-inspired coverage

The project is **MITRE ATLAS-inspired**, not fully ATLAS-mapped. It uses ATLAS-style thinking for adversarial AI behavior such as prompt injection, memory/context poisoning, unsafe tool use, and agentic manipulation. A production version could add explicit ATLAS tactic/technique IDs in the Wazuh rules, Slack messages, TheHive custom fields, and DataTable schemas.

<!--

### Important wording for portfolio use

Use this wording to avoid overclaiming:
--->

> This prototype is OWASP GenAI/LLM-aligned, partially OWASP MCP-aligned, and MITRE ATLAS-inspired. It demonstrates practical SOC automation for AI runtime threats, but it is not a complete OWASP compliance implementation or full ATLAS matrix mapping.

Useful references:

- OWASP Top 10 for Large Language Model Applications: `https://owasp.org/www-project-top-10-for-large-language-model-applications/`
- OWASP MCP Top 10: `https://owasp.org/www-project-mcp-top-10/`
- MITRE ATLAS: `https://atlas.mitre.org/`

---

## 📈 SOC value and expected impact

Because this is an MVP prototype, the value is expressed as **expected SOC impact**, not fictional production statistics.

### Expected SOC value

- **Earlier detection-content quality control:** Flow A2 catches broken AI-security policies, schema problems, mapping issues, and replay failures before deployment.
- **Safer Wazuh deployment:** Flow B2 prevents direct rule/policy rollout unless CI labels, approval, and deployment signal are present.
- **Operational AI runtime visibility:** Flow C2 turns MCP/RAG/agentic runtime events into Slack alerts, TheHive artifacts, and audit rows instead of leaving them as raw application logs.
- **Better analyst context:** Alerts include domain classification, risk context, policy decision, recommended action, TheHive links, and evidence fields.
- **Reduced manual tracking:** DataTables record CI runs, deployments, runtime alerts, policy violations, case promotions, regression outcomes, and dashboard summaries.
- **Detection tuning loop:** Flow F and Flow G show how regression and false-positive analytics can support detection lifecycle management.
- **Portfolio-grade evidence:** The project includes workflow exports, scripts, rules, decoders, documentation, PDFs, and validated screenshots for interview/demo use.

### Lifecycle demonstrated

```text
GitHub AI-security change
→ Flow A2 CI validation
→ labels and PR comment
→ Flow B2 approval gate
→ staged Wazuh/policy deployment
→ runtime MCP/RAG/agentic event
→ Wazuh alert
→ Flow C2 triage
→ Slack + TheHive + DataTables
→ regression/FP/dashboard feedback loop
```

### Why this matters

Most GenAI security demos stop at a single prompt-injection example or a single SIEM alert. This project shows how AI-security events can be handled as an operational SOC lifecycle: validate the content, deploy it safely, detect runtime abuse, generate case evidence, and measure detection quality over time.

---

## 📁 Repository layout

```text
27-genai-detection-as-code-v2-mcp-rag-agentic-wazuh-n8n-thehive/
├── README.md
├── FILE_INDEX.md
├── SECURITY_NOTES.md
├── architecture-notes.txt
├── detailed-repo-layout.md
├── interview_qna.md
├── troubleshooting.md
├── 00-project-overview/
├── 01-flow-a2-ai-security-content-ci/
├── 02-flow-b2-controlled-wazuh-policy-deployment/
├── 03-flow-c2-runtime-mcp-rag-agentic-soc-triage/
├── 04-supporting-workflows-efg-dashboard-analytics/
├── _shared/
├── notes/
├── project-pdfs/
└── resources/
```

---

## 📦 Included artifacts

- ✅ Five premium project PDFs and DOCX files
- ✅ Final n8n workflow JSON exports
- ✅ Wazuh decoders and rules for MCP/RAG/agentic detections
- ✅ MCP, RAG/memory, and agentic demo lab code
- ✅ Runtime event generators and replay corpora
- ✅ Flow A2 CI validators and mapping files
- ✅ Flow B2 deployment runner, config template, and rollback helpers
- ✅ Flow E/F/G/Dashboard scripts and schemas
- ✅ TheHive case template copy-paste material
- ✅ DataTable schemas and evidence CSV exports
- ✅ Architecture notes, interview Q&A, troubleshooting, and production roadmap
- ✅ LinkedIn launch post pack and architecture image prompt

---

## 🚀 Zero-to-hero usage guide

This repository folder is designed as a **portfolio and implementation artifact**, not a one-command production installer. The exact lab was built on Wazuh, n8n, TheHive, Slack, and GitHub with remote SSH access to a Wazuh manager.

### 1. Import workflows

Import the final JSON files from each flow folder into n8n:

```text
01-flow-a2-ai-security-content-ci/n8n-workflows/
02-flow-b2-controlled-wazuh-policy-deployment/n8n-workflows/
03-flow-c2-runtime-mcp-rag-agentic-soc-triage/n8n-workflows/
04-supporting-workflows-efg-dashboard-analytics/n8n-workflows/
```

### 2. Configure credentials

Create n8n credentials for:

| Credential | Used by |
|---|---|
| GitHub API | Flow A2 and Flow B2 PR comments, labels, and PR state |
| Slack API | all analyst notifications |
| TheHive 5 API | Flow C2 alert/case creation and comments |
| SSH key / `.env.ci` | Flow A2 validation and Flow B2 deployment runners |

Use `_shared/config-templates/.env.ci.example` as the safe template. Do not commit real secrets.

### 3. Install Wazuh content

Use Flow B2 for controlled deployment, or manually review:

```text
03-flow-c2-runtime-mcp-rag-agentic-soc-triage/detections/wazuh/
```

### 4. Generate runtime evidence

Run the lab scripts under Flow C2:

```bash
python3 scripts/runtime/run_mcp_action_scenarios.py
python3 scripts/runtime/run_rag_memory_scenarios.py
python3 scripts/runtime/run_agentic_scenarios.py
```

### 5. Review SOC outputs

Validate evidence in:

- Slack SOC alert channel
- TheHive alerts/cases
- Wazuh alerts
- n8n execution logs
- n8n DataTables
- project PDFs under `project-pdfs/`

---

## 🧭 Main workflow summaries

### Flow A2 — AI Security Content CI

Flow A2 is the GitHub PR validation workflow. It validates AI-security content before anything is allowed to move toward deployment. It checks Wazuh XML, Sigma-style content, metadata, MCP policy files, MCP policy bundles, tool schema hashes, prompt policies, RAG memory policies, agentic policies, case-template mappings, rule-family maps, DataTable schemas, and replay harness results.

**Main output:** GitHub PR comment, pass/fail labels, Slack CI report, changed-file audit rows, stage-result rows, and CI run rows.

**Security purpose:** prevent broken AI-security rules, unsafe policy changes, or missing metadata from becoming deployed detection content.

### Flow B2 — Controlled Wazuh + AI Security Policy Deployment

Flow B2 is the deployment gate. It listens for a deployment signal and checks whether the PR has the required pass labels, approval/approved label, ready-to-deploy state, and valid `/deploy-lab` trigger. If the gate fails, it blocks deployment before touching Wazuh. If the gate passes, it runs the deployment runner to checkout the approved commit, stage rules/policies, create backups, run predeploy checks, activate content, restart Wazuh, and record deployment results.

**Main output:** blocked/deployed GitHub comment, Slack deployment message, deployment DataTable rows, policy bundle deployment rows, backup/staging references, and stage-result evidence.

**Security purpose:** turn AI-security content deployment into a controlled, auditable change-management process.

### Flow C2 — Runtime MCP, RAG/Memory, and Agentic SOC Triage

Flow C2 is the strongest runtime workflow. It receives Wazuh alerts generated from MCP, RAG/memory, and agentic AI test events. It normalizes the event, determines the AI security domain, enriches the alert, deduplicates state, sends Slack notifications, creates/updates TheHive alerts, promotes high-risk alerts to cases, and writes domain-specific DataTable rows.

**Main output:** Slack runtime alert, TheHive alert/case, MCP/RAG/agentic DataTables, policy violation rows, plan-step rows, audit events, and case-promotion evidence.

**Security purpose:** demonstrate how a SOC can operationalize AI runtime telemetry instead of treating LLM/MCP/RAG/agentic risk as only an application-side concern.

### Supporting workflows — Flow E, Flow F, Flow G, and dashboard rollup

The supporting workflows provide engineering feedback loops around the main flows:

- **Flow E MCP Runtime Policy Monitor:** monitors MCP policy events directly and reports policy violations.
- **Flow F Red-Team Replay Regression:** replays expected attack/benign corpora and tracks passed tests, expected misses, and unexpected alerts.
- **Flow G False Positive Analytics:** summarizes noisy detections and recommends tuning actions.
- **Dashboard Rollup:** combines CI, deployment, runtime, regression, and false-positive metrics into SOC-facing summaries.

**Main output:** Slack operational summaries, DataTable metrics, regression rows, FP/tuning rows, and dashboard rollup evidence.

**Security purpose:** show that detection engineering needs monitoring, regression, tuning, and dashboard visibility, not only one-time alert creation.

---

## 🧱 Data model

Key DataTables used by the prototype:

| Area | Tables |
|---|---|
| Flow A2 CI | `flow_a2_ci_runs`, `flow_a2_ci_changed_files`, `flow_a2_ci_stage_results`, `flow_v2_regression_runs` |
| Flow B2 deployment | `flow_b2_deployment_runs`, `flow_v2_policy_bundle_deployments` |
| Flow C2 MCP runtime | `flow_v2_mcp_runtime_events`, `flow_v2_mcp_policy_violations`, `flow_v2_mcp_case_promotions`, `flow_v2_mcp_audit_events` |
| Flow C2 RAG/memory | `flow_v2_rag_memory_events` |
| Flow C2 agentic | `flow_v2_agentic_incidents`, `flow_v2_agentic_plan_steps`, `flow_v2_agentic_policy_violations` |
| Supporting workflows | `flow_v2_mcp_policy_monitor_events`, `flow_v2_phase9_regression_runs`, `flow_v2_false_positive_analytics`, `flow_v2_rule_tuning_recommendations`, `flow_v2_dashboard_summary` |

### Audit strategy

The prototype uses DataTables as a lightweight audit/state layer so each workflow produces evidence beyond Slack messages:

- Flow A2 records what changed, which stages passed/failed, and the final CI decision.
- Flow B2 records whether deployment was blocked or deployed, why the gate passed/failed, and what backup/staging paths were used.
- Flow C2 records runtime AI security events by domain so MCP, RAG/memory, and agentic incidents do not get mixed together.
- Supporting workflows record regression, false-positive, policy-monitor, and dashboard metrics for engineering review.

---

## ✅ Validation evidence

The prototype was tested through:

- **A2 Test A1:** valid agentic-policy PR passed 13/13 stages.
- **A2 Test A2:** malformed/broken agentic-policy PR failed and applied fail labels.
- **B2 Test B1:** failed PR deployment was blocked before touching Wazuh.
- **B2 Test B2:** approved pass-labeled PR deployed Wazuh content and policy bundles.
- **C2 Test C1:** MCP runtime alert flowed into Slack, TheHive, and MCP DataTables.
- **C2 Test C2:** RAG/memory poisoning alert routed into the RAG/memory table after final routing fix.
- **C2 Test C3:** agentic goal/plan risk alert routed into agentic incident, plan, and policy tables.
- **Support tests:** Flow E, F, G, and dashboard rollup validated monitoring, regression, FP analytics, and metrics reporting.

---

## ⚠️ Prototype boundaries and honest limitations

This is a working MVP/capstone prototype, not a production-managed enterprise deployment. The goal is to prove the architecture, detection lifecycle, automation logic, and evidence flow.

| Boundary | Current MVP behavior | Production expectation |
|---|---|---|
| Lab scope | Built and tested in a controlled lab with one repo, one Wazuh manager path, and controlled AI demo telemetry | Multi-repo, multi-env, multi-agent rollout with environment-specific controls |
| n8n execution | Workflow logic runs inside n8n with command nodes and API nodes | Dedicated runner isolation, stricter service accounts, separate execution workers, and hardened credential boundaries |
| DataTables | Used as lightweight audit/state storage | PostgreSQL, SIEM data lake, or case-management database for durable long-term state |
| OWASP/ATLAS coverage | Mapped to OWASP GenAI/LLM, selected OWASP MCP categories, and ATLAS-style AI threat thinking | Add explicit framework IDs, coverage matrices, control owners, evidence links, and review cycles |
| Detection content | Custom Wazuh rules/decoders and demo event corpora validate the core concept | Larger rule corpus, per-rule unit tests, canary deployment, and monitored FP/FN feedback |
| TheHive handling | Alert/case creation, templates, comments, and promotion demonstrated | Full analyst workflow, SLAs, closure taxonomy, custom fields, owner assignment, and bi-directional case sync |
| Secrets | Real secrets are intentionally excluded from repository artifacts | Secret manager, short-lived credentials, audit logging, and formal rotation policy |
| Deployment safety | Backup, staging, XML check, restart, and rollback path demonstrated | Blue/green or canary Wazuh deployment, automated rollback verification, and change-management integration |

The project should be presented as a **validated prototype and portfolio-grade engineering build**. It shows strong implementation depth, but production use would require additional hardening, testing scale, access control, and operational governance.

---

## 🛡️ Security notes

This repo folder intentionally excludes live secrets, private SSH keys, Slack webhooks, GitHub PATs, Wazuh API passwords, and `.env.ci` runtime files. See `SECURITY_NOTES.md`.

---

## 🏭 Production-hardening roadmap

This is an MVP prototype. For production-grade use, improve:

- proper GitHub Actions or runner-host isolation for CI scripts
- stronger n8n credential isolation and environment management
- Wazuh rule lifecycle testing across multiple agents
- TheHive closure taxonomy standardization
- DataTable replacement with durable PostgreSQL or SIEM data lake
- automated false-positive sampling and analyst feedback loops
- per-rule unit tests and canary deployment before global rollout
- alert dedup strategy across multiple sessions/users/environments
- role-based deployment approvals and audit signing
- explicit OWASP GenAI / OWASP MCP / MITRE ATLAS ID mapping in rules, cases, and reports

---

## 🔭 Future improvements

Future work can turn this MVP from a strong lab prototype into a more production-like AI Security Operations platform:

1. **Add explicit framework mapping fields** for OWASP LLM, OWASP MCP, MITRE ATLAS tactic/technique, severity rationale, and mitigation guidance.
2. **Move DataTables to durable storage** such as PostgreSQL, OpenSearch, or a SIEM data lake for long-term analytics and joins.
3. **Introduce CI runners instead of local command nodes** for stronger isolation and repeatable validation environments.
4. **Expand runtime telemetry sources** beyond the demo lab to include real application middleware, API gateways, MCP servers, vector databases, and agent orchestration logs.
5. **Add canary deployment for Wazuh rules** before applying content globally.
6. **Build analyst feedback loops** so TheHive closure reasons and false-positive notes automatically feed tuning recommendations.
7. **Add dashboards for coverage and drift** showing which MCP/RAG/agentic scenarios are covered, missing, noisy, or recently changed.
8. **Implement stronger deduplication and correlation** across user ID, session ID, request ID, tool name, memory object, and agent plan ID.
9. **Add formal case SLAs and owner routing** for high-risk AI runtime events.
10. **Package lab replay as repeatable test suites** so the project can be revalidated after every rule/policy/workflow change.

---

## 🧑‍💼 Interview talking points

- “I extended a GenAI detection CI/CD prototype into an AI Security Operations platform that covers MCP, RAG/memory, and agentic AI runtime risk.”
- “Flow A2 validates AI-security content before deployment, Flow B2 gates deployment, and Flow C2 handles runtime SOC triage.”
- “The strongest part is Flow C2: one workflow handles three AI risk families and routes each to different DataTables, TheHive templates, and Slack summaries.”
- “The project is OWASP GenAI/LLM-aligned, partially OWASP MCP-aligned, and MITRE ATLAS-inspired, but I intentionally avoid overclaiming full compliance.”
- “I also built regression and false-positive analytics workflows because detections need measurement and tuning, not only alerts.”

---

## 🌐 Project Posts on LinkedIn

I also shared this project on LinkedIn through multiple posts covering the implementation, workflow, and key outcomes.

> To be added Soon....

<!--

<p align="left">
  <a href="https://tinyurl.com/aws-iam-flow-a"><img src="https://img.shields.io/badge/LinkedIn-Post%2001-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Post 01" /></a>
  <a href="https://tinyurl.com/aws-iam-flow-b"><img src="https://img.shields.io/badge/LinkedIn-Post%2002-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Post 02" /></a>
  <a href="https://tinyurl.com/aws-iam-flow-c"><img src="https://img.shields.io/badge/LinkedIn-Post%2003-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Post 03" /></a>
  <a href="https://tinyurl.com/aws-iam-flow-d"><img src="https://img.shields.io/badge/LinkedIn-Post%2004-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Post 04" /></a>
  <a href="https://tinyurl.com/3w7uaz74"><img src="https://img.shields.io/badge/LinkedIn-Post%2005-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Post 05" /></a>
  <a href="https://tinyurl.com/kjbzxyb8"><img src="https://img.shields.io/badge/Capstone-Post%2006-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Post 06" /></a>
  <a href="https://www.linkedin.com/posts/abdul4rehman215_detectionengineering-securityoperations-soar-activity-7452698979034660865-N8iD?"><img src="https://img.shields.io/badge/Architecture-Post%2007-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Post 07" /></a>
  <a href="https://www.linkedin.com/posts/abdul4rehman215_opentowork-cybersecurity-socanalyst-share-7450140849482645505-eXr4?"><img src="https://img.shields.io/badge/Recruiter-Post%2008-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Post 08" /></a>
</p>

---

-->

## ⭐ Final Note

This project reflects **real hands-on implementation** focused on practical security workflow execution, technical depth, and portfolio-grade documentation.

It demonstrates the ability to:

> **Build → Validate → Investigate → Document → Present**

If this project adds value, consider starring the repository ⭐

---

## 👨‍💻 Author

Built and documented by **[abdul4rehman215](https://www.linkedin.com/in/abdul4rehman215/)** as a capstone-style SOC + AI Security automation MVP.

SOC • SIEM • Detection Engineering • Incident Response • Threat Intelligence • Security Automation

---

### 📧 Reach Out

  <a href="https://github.com/abdul4rehman215">
    <img src="https://img.shields.io/badge/Follow-181717?style=for-the-badge&logo=github&logoColor=white" alt="Follow" />
  </a>
  <a href="https://linkedin.com/in/abdul4rehman215">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white&v=1" alt="LinkedIn" />
  </a>
  <a href="mailto:abdul4rehman215@gmail.com">
    <img src="https://img.shields.io/badge/Email-EE0000?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" />
  </a>

---
