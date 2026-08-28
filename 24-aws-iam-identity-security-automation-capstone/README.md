# ☁️ AWS IAM Identity Security Automation Capstone (n8n + AWS + Slack + DataTable + TheHive 5)

<p align="center">
  <a href="https://www.linkedin.com/in/abdul4rehman215/"><img src="https://img.shields.io/badge/LinkedIn-abdul4rehman215-0A66C2?style=for-the-badge&logo=linkedin" alt="LinkedIn"></a>
  <a href="https://github.com/abdul4rehman215"><img src="https://img.shields.io/badge/GitHub-abdul4rehman215-111827?style=for-the-badge&logo=github" alt="GitHub"></a>
  <img src="https://img.shields.io/badge/Project-Capstone%20Prototype-7C3AED?style=for-the-badge" alt="Project Type">
  <img src="https://img.shields.io/badge/Domain-Cloud%20Identity%20Security-FF9900?style=for-the-badge" alt="Domain">
  <img src="https://img.shields.io/badge/Focus-SOC%20Automation-059669?style=for-the-badge" alt="Focus">
</p>

<p align="center">
  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/AWS%20IAM%20logos.png" alt="AWS IAM Logos" width="900"/>
</p>

## 🎯 Problem vs Solution

Cloud identity findings often arrive as isolated alerts with incomplete context. In real SOC operations, that creates four recurring issues:

- analysts lose time pivoting manually across GuardDuty, Security Hub, CloudTrail, IAM, Slack, and ticketing
- containment is delayed because enrichment and response context are missing
- IAM hygiene drift stays unnoticed until it becomes an incident
- final case outcomes never flow back into operational tracking

This capstone solves that by designing a **four-workflow AWS IAM automation prototype**:

1. **Flow A** triages and enriches identity findings
2. **Flow B** executes containment and promotes the matching TheHive alert into a case
3. **Flow C** performs scheduled IAM hygiene reviews and opens proactive alerts
4. **Flow D** synchronizes TheHive case closure back into tracking

Together, these workflows demonstrate one connected lifecycle for **detection, enrichment, containment, hygiene monitoring, ticketing, and closure synchronization**.

---

## 🧠 What this capstone proves

This project demonstrates that I can design and document a practical cloud identity automation pipeline that connects:

- **AWS-native detection and context**
- **n8n orchestration and branching logic**
- **Slack analyst notifications**
- **DataTable state tracking**
- **TheHive 5 alert and case handling**
- **operational lifecycle closure**

This is not just a set of imported JSON files. It is a portfolio-grade prototype showing workflow design, normalization, enrichment, ticketing integration, scheduled posture monitoring, closure feedback, and documentation-first engineering.

---

## 🧩 High-level architecture

<p align="center">
  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/24-aws-iam-identity-security-automation-capstone/resources/aws-iam-identity-security-capstone-architecture.png" alt="AWS IAM Security Automation Capstone Architecture" width="900"/>
</p>

### Master lifecycle view

```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
    "background": "#050814",
    "fontSize": "28px",
    "primaryTextColor": "#ffffff",
    "lineColor": "#f8fafc"
  },
  "flowchart": {
    "nodeSpacing": 55,
    "rankSpacing": 65,
    "curve": "basis"
  }
}}%%

flowchart LR

    %% =====================================================
    %% 1 · SECURITY AUTOMATION
    %% =====================================================
    subgraph AUTO[" "]
        direction TB

        H1["⚡ 1 · SECURITY AUTOMATION"]

        A["☁️ Flow A<br/>AWS Identity Triage<br/>+ Enrichment"]

        C["🧹 Flow C<br/>Scheduled IAM Hygiene<br/>+ Proactive Alerts"]

        H1 ==> A
        H1 ==> C
    end


    %% =====================================================
    %% 2 · RESPONSE + CASE MANAGEMENT
    %% =====================================================
    subgraph CASE[" "]
        direction TB

        H2["🛡️ 2 · RESPONSE + CASES"]

        B["🚨 Flow B<br/>Containment<br/>+ TheHive Promotion"]

        TH["🐝 TheHive 5<br/>Alerts + Cases"]

        E["✅ Flow D<br/>Case Closure Sync<br/>Back to Tracking"]

        H2 ==> B
        B ==> TH
        TH ==> E
    end


    %% =====================================================
    %% 3 · SHARED OUTPUTS
    %% =====================================================
    subgraph OUTPUT[" "]
        direction TB

        H3["📡 3 · ANALYST + TRACKING OUTPUTS"]

        O["🔀 Shared Output Hub<br/>Automation Events"]

        F["💬 Slack<br/>Analyst Notifications"]

        G["📊 DataTable<br/>Tracking"]

        H3 ==> O

        O ==> F
        O ==> G
    end


    %% =====================================================
    %% CORE AUTOMATION LOGIC
    %% =====================================================
    A ==> B

    A ==> TH
    C ==> TH


    %% =====================================================
    %% NOTIFICATION / TRACKING EVENTS
    %% Replaces repeated crossing arrows
    %% =====================================================
    A -.-> O
    B -.-> O
    C -.-> O
    E -.-> O


    %% =====================================================
    %% PREMIUM HEADER STYLES
    %% =====================================================
    classDef automationHeader fill:#082f49,stroke:#38bdf8,stroke-width:5px,color:#ffffff,font-size:30px;

    classDef caseHeader fill:#3f0d20,stroke:#fb7185,stroke-width:5px,color:#ffffff,font-size:30px;

    classDef outputHeader fill:#312e81,stroke:#c084fc,stroke-width:5px,color:#ffffff,font-size:30px;

    class H1 automationHeader;
    class H2 caseHeader;
    class H3 outputHeader;


    %% =====================================================
    %% SECURITY AUTOMATION COLORS
    %% =====================================================
    classDef flowA fill:#0c4a6e,stroke:#38bdf8,stroke-width:5px,color:#ffffff,font-size:28px;

    classDef flowC fill:#4c1d95,stroke:#c084fc,stroke-width:5px,color:#ffffff,font-size:28px;

    class A flowA;
    class C flowC;


    %% =====================================================
    %% RESPONSE / CASE COLORS
    %% =====================================================
    classDef containment fill:#9a3412,stroke:#fb923c,stroke-width:5px,color:#ffffff,font-size:28px;

    classDef thehive fill:#713f12,stroke:#facc15,stroke-width:6px,color:#ffffff,font-size:29px;

    classDef closure fill:#0f766e,stroke:#2dd4bf,stroke-width:5px,color:#ffffff,font-size:28px;

    class B containment;
    class TH thehive;
    class E closure;


    %% =====================================================
    %% OUTPUT COLORS
    %% =====================================================
    classDef hub fill:#4338ca,stroke:#818cf8,stroke-width:5px,color:#ffffff,font-size:27px;

    classDef slack fill:#7e22ce,stroke:#e879f9,stroke-width:5px,color:#ffffff,font-size:28px;

    classDef tracking fill:#14532d,stroke:#4ade80,stroke-width:5px,color:#ffffff,font-size:28px;

    class O hub;
    class F slack;
    class G tracking;


    %% =====================================================
    %% GLOSSY CONTAINERS
    %% =====================================================
    style AUTO fill:#071822,stroke:#38bdf8,stroke-width:3px

    style CASE fill:#170810,stroke:#fb7185,stroke-width:3px

    style OUTPUT fill:#120b24,stroke:#c084fc,stroke-width:3px


    %% =====================================================
    %% BRIGHT CONNECTORS
    %% =====================================================
    linkStyle default stroke:#f8fafc,stroke-width:5px;
```

### Operational sequence in plain English

- **Flow A** receives AWS identity findings through SNS/webhook ingestion, validates the source, enriches IAM context, adds CloudTrail/last-used context, scores risk, updates Slack/DataTable, and creates a TheHive alert in the ticketing-enabled variant.
- **Flow B** receives a Security Hub custom action or approved containment event, disables the exposed IAM access key when applicable, updates Slack/DataTable, finds the matching TheHive alert from Flow A, promotes it to a case, and leaves a case comment.
- **Flow C** runs on a schedule, generates the IAM credential report, parses the CSV output, identifies hygiene findings such as missing MFA or unused keys, posts a digest to Slack, updates DataTable, and creates TheHive alerts for actionable hygiene issues.
- **Flow D** polls TheHive for recent cases, identifies those that are closed/resolved/duplicated/false-positive, normalizes the closure data, updates DataTable, and posts a closure sync notification to Slack.

---

## 🔗 How the four flows connect in production

| Flow | Primary function | Main inbound trigger | Main downstream output |
|---|---|---|---|
| **Flow A** | AWS identity triage and enrichment | SNS/webhook for identity findings | Slack, DataTable, TheHive alert |
| **Flow B** | IAM containment and case promotion | Security Hub custom action / approved event | Slack, DataTable, TheHive case |
| **Flow C** | Scheduled IAM hygiene checks | n8n schedule trigger | Slack digest, DataTable, TheHive hygiene alerts |
| **Flow D** | Closed-case lifecycle sync | n8n schedule/manual trigger | Slack closure notice, DataTable final state |

### Design intent

The workflows are intentionally documented as **separate portfolio projects** because each one proves a different SOC capability. In a real deployment, they operate as one coordinated prototype:

- Flow A creates the enriched alert context and ticketing anchor.
- Flow B acts on the same identity issue and escalates the matching alert into a real case.
- Flow C widens coverage by opening proactive IAM hygiene alerts.
- Flow D closes the loop by pushing case outcomes back into operational records.

---

## 🧰 Core technologies used

| Tool / Platform | Why it is used in this prototype |
|---|---|
| **AWS GuardDuty / Security Hub / IAM / CloudTrail** | Detection source, identity context, last-used intelligence, audit trail validation |
| **n8n** | Main orchestration layer for normalization, branching, enrichment, notifications, ticketing, and lifecycle automation |
| **Slack** | Fast analyst-facing notification channel for triage, containment, hygiene, and closure updates |
| **DataTable** | Lightweight state-tracking layer for inbox/finding lifecycle persistence |
| **TheHive 5** | Alert creation, case promotion, analyst workflow tracking, and closure lifecycle management |
| **CSV / IAM credential report** | Source of scheduled hygiene analysis for MFA, unused keys, and stale credentials |

---

## 📉 SOC value and expected impact

Because this is a prototype, the value is expressed as **expected operational impact**, not fictional production metrics.

### Expected outcomes

- **Lower MTTD:** analysts receive identity findings already enriched with IAM and CloudTrail context
- **Lower MTTR:** containment and case promotion happen in a structured, repeatable workflow
- **Reduced alert fatigue:** hygiene digests consolidate posture issues into one operational view
- **Better response consistency:** TheHive case promotion and closure sync make the lifecycle traceable
- **Stronger reporting:** DataTable state tracking becomes more complete once closure outcomes are synchronized

---

## 📁 Project layout and artifact mapping

```text
24-aws-iam-identity-security-automation-capstone/
├── README.md                                           # Capstone overview, objectives, architecture summary, and navigation
├── architecture-notes.txt                              # High-level design notes and implementation rationale
├── interview_qna.md                                    # Interview-focused talking points and project discussion prompts
├── notes/                                              # Supporting notes for positioning, decisions, and presentation
│   ├── architecture-image-prompt.md                    # Prompt/reference for generating architecture visuals
│   ├── capstone-positioning-and-usp.md                 # Project positioning, USP, and portfolio framing notes
│   ├── implementation-decisions.md                     # Key implementation decisions and tradeoffs
│   └── linkedin-links-placeholder.md                   # Placeholder for portfolio and LinkedIn reference links
├── resources/                                          # Supporting references and reusable guidance
│   └── README.md                                       # Notes about reference material used in the capstone
├── project-pdfs/                                       # Exported PDF artifacts for overview and workflow evidence
│   ├── AWS IAM n8n Automation Project Overview.pdf     # Project overview document
│   ├── Flow A AWS Identity Triage TheHive Alert.pdf    # Flow A evidence/export
│   ├── Flow B AWS Identity Containment TheHive5 Native.pdf  # Flow B evidence/export
│   ├── Flow C AWS IAM Hygiene TheHive5 Alerts.pdf      # Flow C evidence/export
│   ├── Flow D AWS TheHive Case Closure Sync.pdf        # Flow D evidence/export
│   └── README.md                                       # Notes about included PDF artifacts
├── 00-project-overview/                                # Executive overview, rollout notes, and high-level project summary
│   ├── README.md                                       # Overview of the capstone scope and structure
│   ├── architecture-notes.txt                          # Overview architecture notes
│   ├── interview_qna.md                                # Interview prep for the overall capstone
│   ├── troubleshooting.md                              # Common issues and fixes for the overall setup
│   ├── artifacts/
│   │   └── AWS IAM n8n Automation Project Overview.pdf # Overview artifact
│   └── notes/
│       ├── overview-summary.md                         # Short summary of the capstone
│       └── rollout-and-demo-notes.md                   # Demo flow and rollout notes
├── 01-flow-a-aws-identity-triage-and-enrichment/       # Flow A: triage, enrichment, and alert context building
│   ├── README.md                                       # Workflow explanation and flow-specific setup
│   ├── architecture-notes.txt                          # Flow A architecture notes
│   ├── interview_qna.md                                # Flow A interview talking points
│   ├── troubleshooting.md                              # Flow A troubleshooting guidance
│   ├── artifacts/
│   │   └── Flow A AWS Identity Triage TheHive Alert.pdf
│   └── notes/
│       ├── design-notes.md                             # Design rationale for Flow A
│       ├── extension-ideas.md                          # Future enhancements for Flow A
│       └── validation-notes.md                         # Validation and testing notes
├── 02-flow-b-aws-identity-containment-and-case-promotion/  # Flow B: containment and case promotion
│   ├── README.md                                       # Workflow explanation and operational notes
│   ├── architecture-notes.txt                          # Flow B architecture notes
│   ├── interview_qna.md                                # Flow B interview talking points
│   ├── troubleshooting.md                              # Flow B troubleshooting guidance
│   ├── artifacts/
│   │   └── Flow B AWS Identity Containment TheHive5 Native.pdf
│   └── notes/
│       ├── case-template-notes.md                      # Notes on case structure/template usage
│       ├── design-notes.md                             # Design rationale for Flow B
│       └── validation-notes.md                         # Validation and testing notes
├── 03-flow-c-aws-iam-hygiene-monitoring-and-alerting/  # Flow C: IAM hygiene monitoring and alert generation
│   ├── README.md                                       # Workflow explanation and monitoring logic
│   ├── architecture-notes.txt                          # Flow C architecture notes
│   ├── interview_qna.md                                # Flow C interview talking points
│   ├── troubleshooting.md                              # Flow C troubleshooting guidance
│   ├── artifacts/
│   │   └── Flow C AWS IAM Hygiene TheHive5 Alerts.pdf
│   └── notes/
│       ├── design-notes.md                             # Design rationale for Flow C
│       ├── finding-logic-notes.md                      # Detection/finding logic notes
│       └── validation-notes.md                         # Validation and testing notes
└── 04-flow-d-thehive-case-closure-sync/                # Flow D: TheHive case closure synchronization
    ├── README.md                                       # Workflow explanation and sync logic
    ├── architecture-notes.txt                          # Flow D architecture notes
    ├── interview_qna.md                                # Flow D interview talking points
    ├── troubleshooting.md                              # Flow D troubleshooting guidance
    ├── artifacts/
    │   └── Flow D AWS TheHive Case Closure Sync.pdf
    └── notes/
        ├── design-notes.md                             # Design rationale for Flow D
        ├── field-mapping-notes.md                      # Field mapping/reference notes
        └── validation-notes.md                         # Validation and testing notes
```

---

## 🗂️ Included artifacts

### PDFs
- full project overview PDF
- Flow A PDF
- Flow B PDF
- Flow C PDF
- Flow D PDF

### Workflow JSONs
- primary final JSON for each flow
- non-TheHive / non-ticketing variants where relevant
- build-iteration and patch variants retained for learning and reuse
- sample test payloads and CSV state files

---

## 📘 How to use this repository

### Portfolio / recruiter review
Start with:
- `README.md`
- `00-project-overview/README.md`
- each flow folder README in order from A to D

### Technical review
Open:
- `workflow-jsons/`
- each flow folder `architecture-notes.txt`
- each flow folder `troubleshooting.md`

### Demo / validation review
Use:
- the PDFs under `project-pdfs/`
- `workflow-jsons/sample-data/`
- each flow folder `notes/validation-notes.md`

---

## ⚠️ Prototype boundaries and honest limitations

This repository documents a **high-value capstone prototype**, not a production SaaS product.

- environment-specific credentials, URLs, Slack channels, and TheHive IDs are not bundled
- imported JSONs still require local credential binding in n8n
- Flow B depends on Flow A having opened the matching TheHive alert
- Flow C depends on IAM credential report readiness timing
- Flow D depends on consistent source/sourceRef or case-description mapping back to tracked findings

These limitations are part of the project’s credibility: they show where production hardening would be applied.

---

## 🔭 Future enhancements

- replace DataTable with richer persistence such as PostgreSQL or DynamoDB
- add analyst approval gates for selected containment paths
- extend ticketing abstraction to Jira or ServiceNow
- enrich Flow A and Flow C with identity ownership or asset criticality
- emit closure metrics for MTTR and lifecycle dashboards
- convert repeated logic into reusable n8n sub-workflows

---

## 🌐 Project Posts on LinkedIn

I also shared this project on LinkedIn through multiple posts covering the implementation, workflow, and key outcomes.

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

## ⭐ Final Note

This project reflects **real hands-on implementation** focused on practical security workflow execution, technical depth, and portfolio-grade documentation.

It demonstrates the ability to:

> **Build → Validate → Investigate → Document → Present**

If this project adds value, consider starring the repository ⭐

---

## 👨‍💻 Author

**Abdul Rehman**  
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

