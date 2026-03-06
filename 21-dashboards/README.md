# 📊 Wazuh Dashboard Engineering & Security Visualization

## 🌐 Project Overview

This project focuses on **exploring, designing, documenting, and organizing security dashboards in Wazuh** for practical SOC operations.  
Instead of relying only on raw alerts, this project demonstrates how dashboard-driven visibility helps transform security events into **faster triage, clearer prioritization, stronger detection understanding, and better analyst decision-making**.

In a real SOC, dashboards are not just visual elements. They help security teams:

- monitor threats in near real time
- identify suspicious trends quickly
- reduce analyst time spent parsing raw logs
- validate whether detections are useful
- understand ATT&CK coverage and monitoring gaps
- track security posture and compliance visibility
- support reporting, investigations, and daily analyst workflows

This folder serves as the **main parent project directory** for a set of Wazuh dashboard exploration and implementation projects. It provides the overall context, use cases, architecture, and folder structure for the three dashboard-focused subprojects built inside this SOC ecosystem.

---

## 🎯 Project Objective

The objective of this project is to **explore dashboard engineering in Wazuh** from a practical SOC perspective and document how dashboards improve security monitoring workflows in an AWS-based SOC ecosystem.

This main project was created to:

- understand the role of dashboards in SIEM-driven SOC operations
- explore how Wazuh visualizations help analysts monitor and investigate security events
- organize dashboard development into structured project folders
- document the learning, use cases, and operational value of dashboarding
- create reusable dashboard subprojects for hands-on learning and future import/export use
- maintain both **learning-focused documentation** and **practical dashboard JSON exports** for portfolio and implementation purposes

---

## 🛡️ Why This Project Matters

A SOC does not operate efficiently by looking only at raw alert logs.

As alert volume grows, analysts need **clear visual context** to answer questions like:

- Which alert types are spiking?
- Which agents are generating the most security events?
- Which ATT&CK tactics are being observed?
- Which endpoints are failing compliance checks?
- Which detections are noisy and need tuning?
- Which dashboards provide the fastest visibility for triage and investigations?

This project matters because it shows how **Wazuh dashboarding becomes part of detection engineering and analyst workflow optimization**, not just reporting.

It supports practical SOC activities such as:

- alert monitoring
- severity-based triage
- MITRE ATT&CK visibility
- compliance posture awareness
- data-driven tuning decisions
- faster investigations
- executive and operational reporting

---

## 🧠 How Dashboards Help SOC Analysts

Wazuh dashboards improve analyst effectiveness in several practical ways:

### 1. ⚡ Faster Triage
Dashboards reduce the need to manually review raw events one by one. Analysts can quickly identify spikes, anomalies, or recurring alert categories through visual summaries.

### 2. 🔕 Reduced Alert Fatigue
By grouping and visualizing alerts, dashboards help analysts distinguish between background noise and genuinely important security activity.

### 3. 🎯 Better Prioritization
Severity trends, top agents, top rule groups, and active alert distributions help analysts decide what deserves immediate attention.

### 4. 🧭 Better Context During Investigations
Dashboards help correlate data visually across time ranges, hosts, alert types, MITRE ATT&CK categories, and other fields.

### 5. 📚 Detection Engineering Support
A dashboard is also useful for evaluating whether a rule, integration, or data source is giving meaningful visibility or just noise.

### 6. 📈 Better Reporting & Communication
Dashboards make it easier to explain security posture, active threats, coverage, and findings to both technical and non-technical stakeholders.

---

## 🔍 Key Wazuh Dashboard Use Cases

Wazuh dashboard visualization supports multiple important use cases in a SOC environment:

- **Real-Time Threat Detection & Monitoring** for active alerts and security activity
- **File Integrity Monitoring (FIM) Visibility** to observe file changes and unauthorized modifications
- **Security Configuration Assessment (SCA)** visibility for benchmark and policy alignment
- **Vulnerability Detection** to identify exposed or outdated software on monitored endpoints
- **Compliance Monitoring** for standards such as CIS-oriented visibility and security posture tracking
- **Cloud Security Visibility** for monitored cloud telemetry and related event flows
- **Threat Hunting** through custom searches, filtering, patterns, and exploratory analysis
- **MITRE ATT&CK Mapping** to visually understand tactics, techniques, and coverage areas
- **Custom Dashboard Engineering** for organization-specific monitoring and operational views

---

## 🏗️ Role of This Project in the SOC Ecosystem

This dashboard project is part of the larger **SOC-SOAR-ECOSYSTEM-AWS** portfolio and sits on top of the monitoring and detection foundation already built across the environment.

It supports and enhances visibility from components such as:

- Wazuh manager and dashboard
- Wazuh agents
- Sysmon integrations
- Suricata and Zeek integrations
- threat intelligence integrations
- CloudTrail and AWS monitoring
- compliance and posture-related modules
- endpoint and network detections

Instead of replacing detection logic, dashboards help make those detections **usable, visible, and operationally meaningful**.

---

## 🧰 Prerequisites

Before working with these dashboards, the following knowledge and setup are recommended:

### Technical Prerequisites
- Basic understanding of Wazuh architecture
- Familiarity with Wazuh alerts and index patterns
- Basic knowledge of SOC workflows and triage
- Basic understanding of filters, fields, and time ranges in dashboards
- Familiarity with MITRE ATT&CK concepts
- Basic understanding of compliance/security benchmark concepts

### Environment Prerequisites
- Functional Wazuh deployment
- Wazuh Dashboard access
- Monitored agents generating alert data
- Relevant integrations already feeding useful telemetry
- Sufficient alert volume or historical data for visualization

---

## 🖥️ Environment Context

This project was explored as part of an **AWS-based SOC ecosystem** where Wazuh acted as the central SIEM / XDR visibility layer.

### Environment Summary
- **Platform:** AWS-based SOC lab / project environment
- **Primary SIEM:** Wazuh
- **Interface Used:** Wazuh Dashboard
- **Use Case Focus:** Visualization, triage, dashboard engineering, operational monitoring
- **Project Type:** Self-performed project-based exploration
- **Purpose:** Learning, practical implementation, portfolio documentation, and reusable dashboard imports

---

## 📚 Official Reference

For the official Wazuh guidance on creating custom dashboards, refer to the [Wazuh custom dashboard creation documentation](https://documentation.wazuh.com/current/user-manual/wazuh-dashboard/creating-custom-dashboards.html).

This official resource is useful for understanding:

- dashboard creation basics
- panel and visualization building
- filtering and data selection
- custom dashboard layout options
- Wazuh/OpenSearch dashboard workflow concepts

---

## 🧱 Project Scope

This main folder is designed as the **parent dashboard project directory**.  
It provides the overall dashboard-engineering context and organizes three separate dashboard subprojects:

1. **SOC Threat Monitoring Dashboard**
2. **SOC MITRE ATT&CK Coverage Dashboard**
3. **SOC Compliance & CIS Benchmark Dashboard**

Each subfolder will contain its own:

- `README.md`
- `architecture.txt`
- `interview_qna.md`
- `troubleshooting.md`
- exported dashboard `.json` file
- any additional implementation-specific notes or supporting files if needed

This structure allows each dashboard to be understood both as:

- an **independent hands-on project**
- and as part of the larger **Wazuh dashboard engineering initiative**

---

## 📁 Repository Structure

```text
21-dashboards/
├── README.md
├── architecture.txt
├── interview_qna.md
├── 01-soc-threat-monitoring-dashboard/
│   ├── README.md
│   ├── architecture.txt
│   ├── interview_qna.md
│   ├── troubleshooting.md
│   └── soc-threat-monitoring-dashboard.json
├── 02-soc-mitre-attack-coverage-dashboard/
│   ├── README.md
│   ├── architecture.txt
│   ├── interview_qna.md
│   ├── troubleshooting.md
│   └── soc-mitre-attack-coverage-dashboard.json
└── 03-soc-compliance-cis-benchmark-dashboard/
    ├── README.md
    ├── architecture.txt
    ├── interview_qna.md
    ├── troubleshooting.md
    └── soc-compliance-cis-benchmark-dashboard.json
````

---

## 📊 Dashboard Categories Covered

### 1. 🚨 SOC Threat Monitoring Dashboard

This dashboard focuses on active security monitoring and SOC triage visibility, such as:

* alert trends
* severity distribution
* top alerting agents
* active rule groups
* event spikes
* frequently triggered detections
* operational alert monitoring

This is useful for daily SOC activity, live monitoring, and quick investigation starting points.

---

### 2. 🧭 SOC MITRE ATT&CK Coverage Dashboard

This dashboard focuses on visualizing security activity through the MITRE ATT&CK lens, such as:

* ATT&CK tactics visibility
* ATT&CK techniques distribution
* mapped detections
* coverage observations
* technique frequency
* ATT&CK-based monitoring context

This is useful for detection engineering, reporting, and understanding where security monitoring aligns with attacker behavior models.

---

### 3. ✅ SOC Compliance & CIS Benchmark Dashboard

This dashboard focuses on security posture and benchmark-oriented visibility, such as:

* compliance-related findings
* CIS-aligned monitoring views
* configuration assessment visibility
* failing checks and posture trends
* monitored endpoint security baseline observations

This is useful for hardening visibility, security posture awareness, and compliance-related monitoring discussions.

---

## ⚙️ What This Main Folder Demonstrates

This parent project demonstrates several practical skills and concepts:

* Wazuh feature exploration
* security dashboard engineering
* SIEM visualization planning
* SOC workflow thinking
* analyst-centered dashboard use case design
* practical understanding of visibility requirements
* organizing dashboard projects for both learning and reuse
* converting security telemetry into operationally useful visualizations

---

## 🛠️ Implementation Approach

This dashboards project follows a practical approach:

### Step 1 — Understand the SOC monitoring need

Identify what the dashboard is supposed to solve:

* threat triage
* ATT&CK coverage visibility
* compliance posture visibility

### Step 2 — Identify useful Wazuh data

Determine which alerts, modules, rule groups, or indexed data fields are useful for the dashboard.

### Step 3 — Design dashboard panels

Plan charts, metrics, tables, and visual layouts that are useful for analysts instead of just being visually attractive.

### Step 4 — Create exportable dashboards

Maintain dashboard exports as `.json` files so they can be re-imported and reused later.

### Step 5 — Document the dashboard properly

Each dashboard subproject includes learning-focused documentation so the work is understandable even without importing the JSON directly.

---

## 📘 Learning-Focused Design Philosophy

This project is not only about creating dashboards.
It is also about documenting them in a way that helps with:

* learning the Wazuh dashboarding workflow
* understanding why each dashboard exists
* understanding how the dashboard helps a SOC analyst
* preserving the dashboard for future import
* making the project portfolio-ready and reproducible

That is why every dashboard subfolder will include both:

* the actual exported dashboard file
* detailed supporting documentation

---

## 🚀 Real-World Applications

These types of dashboards are useful in real-world environments for:

* SOC alert monitoring
* blue team operations
* security reporting
* threat hunting support
* compliance visibility
* attack trend observation
* detection validation
* monitoring maturity improvements
* daily analyst workflow optimization

---

## 🌍 Real-World Relevance

In real SOC environments, dashboards are often the first place analysts look before drilling into raw logs.

They help teams answer high-value questions such as:

* Are high-severity alerts increasing?
* Which endpoints are generating the most events?
* Which ATT&CK categories are most commonly observed?
* Are compliance findings improving or worsening?
* Which detections need tuning?
* Which threat patterns are persistent over time?

This project reflects that reality by treating dashboards as an operational capability, not just a cosmetic feature.

---

## 🧠 What I Learned

Through this dashboard-focused project, I strengthened my understanding of:

* the operational value of Wazuh dashboards
* how dashboards support SOC triage and investigations
* how visualizations reduce dependency on raw log review
* how dashboard design can support detection engineering
* how ATT&CK and compliance views provide different monitoring perspectives
* how to document dashboard projects for both practical reuse and learning

---

## 📌 Result

By completing this project structure and dashboard exploration:

* I organized Wazuh dashboard work into reusable project folders
* I documented the purpose and value of dashboard engineering in a SOC
* I prepared three dashboard subprojects for separate detailed implementation
* I aligned visualization work with practical SOC analyst use cases
* I preserved both the learning context and the reusable dashboard export model

---

## 🧾 Conclusion

This project represents the **dashboard engineering and security visualization** layer of my AWS-based SOC ecosystem.

Rather than treating dashboards as simple UI features, this project approaches them as practical tools for:

* analyst efficiency
* faster triage
* better visibility
* detection understanding
* ATT&CK and compliance monitoring
* stronger operational security workflows

The three dashboard subprojects inside this folder extend that vision further by focusing on distinct SOC visibility needs: **threat monitoring, ATT&CK coverage, and compliance/CIS benchmark visibility**.

---

## 🔗 Related Internal Dashboard Subprojects

This main folder is the parent directory for:

* **SOC Threat Monitoring Dashboard**
* **SOC MITRE ATT&CK Coverage Dashboard**
* **SOC Compliance & CIS Benchmark Dashboard**

Each of these subprojects will be documented individually with its own guide, architecture, interview Q&A, troubleshooting, and reusable JSON export.

---
