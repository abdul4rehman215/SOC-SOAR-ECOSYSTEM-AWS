# 🧭 SOC MITRE ATT&CK Coverage Dashboard

## 🌐 Project Overview

This project demonstrates how I built a **SOC-focused MITRE ATT&CK Coverage Dashboard in Wazuh** to help analysts move beyond raw alerts and understand the **adversary behavior, attack stage, and technique patterns** behind those detections.

Traditional monitoring often answers only surface-level questions such as:

- how many alerts were generated
- what severity level they have
- which host or source IP triggered them

That is useful, but not enough for mature SOC analysis.

This dashboard adds a more meaningful layer by mapping Wazuh detections to the **MITRE ATT&CK framework**, allowing analysts to understand:

- which ATT&CK tactics are appearing
- which techniques are being observed most often
- which technique IDs are showing up in alerts
- how attacker behavior evolves over time
- whether the observed activity reflects single-stage or multi-stage attack patterns

Instead of looking at detections only as isolated alerts, this project helps interpret them as **structured attacker tradecraft visibility**.

---

## 🎯 Project Objective

The objective of this project was to build and document a **MITRE ATT&CK-focused dashboard in Wazuh** that helps SOC analysts:

- visualize alert activity through MITRE ATT&CK tactics
- identify the most common techniques being detected
- track standardized MITRE technique IDs across alerts
- monitor technique activity over time
- improve investigation context for adversary behavior analysis
- support threat hunting, triage, and ATT&CK-aligned reporting

This project also follows the same practical documentation model used across the repository:

- a full dashboard-building guide for learning purposes
- a reusable exported dashboard JSON for re-import
- a project structure suitable for portfolio, reproducibility, and hands-on practice

---

## 🛡️ SOC Problem This Dashboard Solves

In many SOC environments, teams can see alerts but struggle to quickly understand:

- what stage of the attack lifecycle is active
- what the attacker is trying to do
- whether multiple alerts point to the same technique family
- whether the environment is seeing persistence, credential access, initial access, or command-and-control related activity
- whether the activity suggests a multi-stage intrusion

Without ATT&CK-aligned visualization, analysts often need to manually read alert descriptions and mentally interpret the attack behavior.

This dashboard solves that by converting MITRE-mapped Wazuh alerts into clear visual views of:

- tactic distribution
- top techniques
- technique IDs
- technique activity over time

That gives analysts a more structured method for understanding how detections relate to attacker behavior.

---

## 🧠 Why This Project Matters

This project matters because modern SOC operations benefit from more than just alert counts and severity levels.

A mature SOC also needs to understand:

- attacker intent
- tactic progression
- repeated technique usage
- adversary patterns over time
- coverage visibility for ATT&CK-mapped detections

This dashboard makes Wazuh detections more useful by placing them into the **MITRE ATT&CK context** that many real-world blue teams, SOCs, detection engineers, and reporting teams rely on.

It supports:

- better investigation context
- more structured threat analysis
- ATT&CK-aligned communication
- improved visibility into attack behavior
- a stronger bridge between alerts and detection engineering

---

## 📌 What This Dashboard Helps Analysts See

This dashboard was designed to answer practical ATT&CK-oriented SOC questions.

| SOC Question | Visualization Used |
|---|---|
| Which MITRE tactics are most active? | MITRE – Tactics Distribution |
| Which attacker techniques appear most often? | MITRE – Top Techniques |
| Which standardized ATT&CK IDs are showing up? | MITRE – Technique IDs |
| How does technique activity change over time? | MITRE – Technique Timeline |

Together, these visualizations create a dashboard that helps analysts interpret detections as **attack behavior patterns**, not just isolated events.

---

## 🏗️ Architecture Used in This Project

```text
Attacker Machine (Kali Linux)
        |
        | Attack Simulation
        |
        v
Monitored Endpoint
(Windows / Ubuntu)
        |
        | Wazuh-monitored telemetry
        |
        v
Wazuh Manager
        |
        | Alert processing / rule matching / MITRE mapping
        |
        v
Wazuh Dashboard / OpenSearch Dashboards
        |
        | Visualization layer
        |
        v
SOC MITRE ATT&CK Coverage Dashboard
        |
        | ATT&CK-based analyst visibility
        |
        v
SOC Analyst / Detection Engineer
````

This project focuses only on the **dashboard and visualization layer** of the workflow.

Wazuh server deployment and Wazuh agent installation are already documented in separate setup folders in the repository, so they are intentionally not repeated here.

---

## 🧰 Technologies Used

```text
Wazuh SIEM
Wazuh Dashboard / OpenSearch Dashboards
MITRE ATT&CK framework
AWS EC2 / lab infrastructure
Ubuntu and/or Windows monitored systems
Kali Linux for attack simulation
Wazuh MITRE-mapped alerts
OpenSearch visualization components
```

---

## 📋 Prerequisites

Before working through this dashboard project, the following prerequisites are useful.

### Technical Knowledge

* Basic understanding of Wazuh alerts
* Basic understanding of the MITRE ATT&CK framework
* Familiarity with tactics, techniques, and ATT&CK IDs
* Basic SOC analyst workflow understanding
* Familiarity with Wazuh Discover and dashboard navigation
* Basic understanding of severity-based alert filtering

### Environment Prerequisites

* A working Wazuh environment already deployed
* Wazuh agents already sending security telemetry
* Alerts visible in the `wazuh-alerts-*` index
* MITRE fields populated in relevant detections
* Security events generated from monitored activity or controlled attack simulation

For platform-level guidance on custom dashboard creation, you can refer to the [official Wazuh custom dashboard documentation](https://documentation.wazuh.com/current/user-manual/wazuh-dashboard/creating-custom-dashboards.html).

For broader ATT&CK reference material, you can also consult the [official MITRE ATT&CK framework website](https://attack.mitre.org/).

---

## 🖥️ Environment Context

This project was built as part of a larger **AWS-based SOC ecosystem** with Wazuh used as the central SIEM and visualization platform.

### Environment Summary

* **Project Type:** Self-performed SOC engineering and detection visibility project
* **SIEM Platform:** Wazuh
* **Visualization Platform:** Wazuh Dashboard / OpenSearch Dashboards
* **Monitored Systems:** Ubuntu and/or Windows endpoint(s)
* **Attack Simulation Source:** Kali Linux
* **Use Case Focus:** ATT&CK-based threat visibility and analyst understanding
* **Primary Goal:** Convert MITRE-mapped Wazuh alerts into a practical SOC dashboard

---

## 🔎 Project Scope

This project focuses specifically on building a **SOC MITRE ATT&CK Coverage Dashboard** using existing Wazuh alert data.

It focuses on:

* validating MITRE-mapped alert fields
* filtering medium/high severity alerts for SOC relevance
* building ATT&CK-based visualizations
* combining them into a dashboard
* documenting the full process clearly
* preserving the exported dashboard JSON for reuse

It does **not** focus on:

* Wazuh stack installation
* Wazuh agent deployment
* full rule authoring from scratch
* broader threat intelligence integrations
* case management or response orchestration

Those capabilities are documented in other folders of the main repository.

---

## 📁 Repository Structure

```text
02-soc-mitre-attack-coverage-dashboard/
├── README.md
├── architecture.txt
├── interview_qna.md
├── troubleshooting.md
└── resources/
    ├── SOC – MITRE ATT&CK Coverage Dashboard.ndjson
    └── images
```

---

## 🧭 Implementation Strategy

This dashboard was built around a simple but important SOC design principle:

> **Do not just visualize alerts. Visualize what those alerts mean in attacker-behavior terms.**

### Design Approach

1. Confirm MITRE-mapped alert data exists in Wazuh
2. Filter the dashboard toward meaningful SOC alerts
3. Identify the most useful ATT&CK fields
4. Build focused visualizations for tactics, techniques, IDs, and timeline
5. Combine them into one ATT&CK-centric dashboard
6. Preserve the dashboard in JSON format
7. Document the project for both learning and reuse

---

## 🪜 Step-by-Step Implementation Guide

## Step 1 — Confirm MITRE-Mapped Alert Data Exists

Before building the dashboard, first verify that Wazuh is already generating alerts with MITRE mapping.

Open:

```text
Discover
```

Use the index:

```text
wazuh-alerts-*
```

Review whether the events contain MITRE-related fields such as:

```text
rule.mitre.tactic
rule.mitre.technique
rule.mitre.id
```

If these fields are visible and populated, the data is ready for ATT&CK-based visualization.

---

## Step 2 — Focus on Meaningful SOC Alerts

This dashboard is intended for analyst use, so it is more helpful to focus on medium to high severity detections rather than every possible low-priority event.

Apply the filter:

```text
rule.level between 8 and 15
```

This improves signal quality by reducing:

* low-value informational noise
* benign background activity
* less actionable alert clutter

This makes the dashboard more aligned with practical investigation and monitoring workflows.

---

## Step 3 — Validate MITRE Fields Before Visualization

Before building any charts, confirm that the core ATT&CK fields actually contain values.

In Discover, validate that alerts contain entries like:

```text
Tactic: Initial Access
Technique: Brute Force
Technique ID: T1110
```

Other examples may include tactics such as:

```text
Credential Access
Persistence
Defense Evasion
Command and Control
Privilege Escalation
```

And techniques such as:

```text
Brute Force
Valid Accounts
Account Manipulation
Communication Through Application Layer Protocol
```

This step ensures the dashboard reflects real ATT&CK-based detection data.

---

## Step 4 — Plan the Dashboard Panels

This dashboard was designed using four focused visualizations:

### 1. MITRE – Tactics Distribution

Shows which ATT&CK tactics are most active.

### 2. MITRE – Top Techniques

Shows the most frequently observed ATT&CK techniques.

### 3. MITRE – Technique IDs

Shows the top ATT&CK technique IDs for standardized classification.

### 4. MITRE – Technique Timeline

Shows how observed techniques change over time.

Together, these provide a practical ATT&CK-focused investigation view.

---

## Step 5 — Create the “MITRE – Tactics Distribution” Visualization

Navigate to:

```text
OpenSearch Dashboards → Visualize → Create Visualization
```

Choose:

```text
Pie
```

Data source:

```text
wazuh-alerts-*
```

### Configuration

**Metric**

```text
Aggregation → Count
```

**Bucket**

```text
Split Slices
Aggregation → Terms
Field → rule.mitre.tactic
Order By → Metric Count
Order → Descending
Size → 10
```

### Style / Options

Enable:

```text
Donut Mode
Show labels
Show legend
```

### Save As

```text
MITRE – Tactics Distribution
```

### Description

```text
Displays the distribution of security alerts mapped to MITRE ATT&CK tactics, helping identify which stages of the attack lifecycle are most active.
```

This visualization helps analysts understand the **attack stage distribution** visible in monitored activity.

---

## Step 6 — Create the “MITRE – Top Techniques” Visualization

Navigate to:

```text
Visualize → Create Visualization
```

Choose:

```text
Pie
```

Data source:

```text
wazuh-alerts-*
```

### Configuration

**Metric**

```text
Aggregation → Count
```

**Bucket**

```text
Split Slices
Aggregation → Terms
Field → rule.mitre.technique
Order By → Metric Count
Order → Descending
Size → 10
```

### Save As

```text
MITRE – Top Techniques
```

### Description

```text
Shows the most frequently observed MITRE ATT&CK techniques associated with high-severity alerts, highlighting common attacker methods.
```

This visualization helps analysts see **which adversary methods appear most often**.

---

## Step 7 — Create the “MITRE – Technique IDs” Visualization

Navigate to:

```text
Visualize → Create Visualization
```

Choose:

```text
Pie
```

Data source:

```text
wazuh-alerts-*
```

### Configuration

**Metric**

```text
Aggregation → Count
```

**Bucket**

```text
Split Slices
Aggregation → Terms
Field → rule.mitre.id
Order By → Metric Count
Order → Descending
Size → 10
```

### Save As

```text
MITRE – Technique IDs
```

### Description

```text
Lists detected MITRE ATT&CK technique IDs (Txxxx), enabling standardized threat classification and reporting.
```

This gives analysts a **standardized ATT&CK reference layer** that is useful for reporting, tuning, and investigations.

---

## Step 8 — Create the “MITRE – Technique Timeline” Visualization

Navigate to:

```text
Visualize → Create Visualization
```

Choose:

```text
Line Chart
```

Data source:

```text
wazuh-alerts-*
```

### Configuration

**Y-Axis**

```text
Aggregation → Count
```

**X-Axis**

```text
Aggregation → Date Histogram
Field → timestamp
Interval → Auto
```

**Split Series**

```text
Aggregation → Terms
Field → rule.mitre.technique
Order By → Metric Count
Order → Descending
Size → 5
```

### Save As

```text
MITRE – Technique Timeline
```

### Description

```text
Visualizes MITRE ATT&CK techniques over time to identify attack spikes, persistence activity, and multi-stage attacks.
```

This visualization helps identify:

* technique spikes
* repeated technique activity
* multi-stage attack behavior
* persistence-like patterns over time

---

## Step 9 — Create the Dashboard

Navigate to:

```text
Dashboards → Create Dashboard
```

Name it:

```text
SOC – MITRE ATT&CK Coverage Dashboard
```

Add the following panels:

```text
MITRE – Tactics Distribution
MITRE – Top Techniques
MITRE – Technique IDs
MITRE – Technique Timeline
```

Recommended layout:

```text
Tactics Distribution        Top Techniques

Technique IDs               Technique Timeline
```

This layout provides:

* attack-stage visibility
* technique visibility
* standardized ATT&CK ID reference
* temporal behavior visibility

---

## 🖼️ Dashboard Screenshots

### Visualization Listing View

<div align="center">
<img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/21-dashboards/02-soc-mitre-attack-coverage-dashboard/resources/2.png"/>
</div>

### Full Dashboard View

<div align="center">
<img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/21-dashboards/02-soc-mitre-attack-coverage-dashboard/resources/3.png"/>
</div>

---

## 📈 Dashboard Analysis

Once the dashboard is built, it provides a strong ATT&CK-oriented view for security operations.

### MITRE – Tactics Distribution

This panel shows which ATT&CK tactic stages are currently most visible, such as:

* Initial Access
* Credential Access
* Persistence
* Defense Evasion
* Command and Control
* Privilege Escalation

This helps analysts understand **where detections sit in the attack lifecycle**.

### MITRE – Top Techniques

This panel highlights the most frequent ATT&CK techniques being observed.

Examples may include:

* Brute Force
* Valid Accounts
* Account Manipulation
* Communication Through Application Layer Protocol

This helps identify the **dominant attacker behaviors** in the monitored environment.

### MITRE – Technique IDs

This panel provides ATT&CK IDs like:

```text
T1110
T1078
T1098
T1136
```

This standardization makes detections easier to reference in:

* investigations
* reports
* detections
* ATT&CK coverage discussions

### MITRE – Technique Timeline

This panel shows how ATT&CK technique activity changes across time.

It helps reveal:

* attack spikes
* recurring techniques
* attack progression
* multi-stage activity
* persistence or repeated access attempts

---

## 🔍 Security Insights This Dashboard Supports

This dashboard helps analysts answer practical ATT&CK-centered SOC questions such as:

```text
Which ATT&CK tactics are most active?
Which techniques are showing up repeatedly?
Which standardized technique IDs are being detected?
Is the environment seeing persistence-related or credential-related activity?
How are attacker behaviors changing over time?
```

Without this type of dashboard, analysts would often need to manually inspect many alerts to understand the same behavior patterns.

---

## ✅ Result

This project successfully demonstrates:

* ATT&CK-aligned dashboard engineering in Wazuh
* practical use of MITRE fields inside alert data
* tactic and technique visibility for SOC workflows
* standardized ATT&CK ID reporting visibility
* time-based technique monitoring
* conversion of raw detections into structured adversary-behavior context

The result is a dashboard that helps analysts understand not just **that something happened**, but **what attacker behavior it most likely represents**.

---

## 🌍 Real-World Applications

This type of dashboard is useful for:

* SOC alert triage
* ATT&CK-based threat analysis
* detection engineering review
* adversary behavior reporting
* analyst investigations
* identifying common technique patterns
* monitoring attack progression over time
* communicating detections using ATT&CK terminology

---

## 🌐 Real-World Relevance

Modern SOCs increasingly use the MITRE ATT&CK framework to make security monitoring more structured and more actionable.

This dashboard reflects that reality by showing how ATT&CK mapping can improve:

* analyst understanding
* threat investigation context
* detection visibility
* reporting consistency
* monitoring maturity

Rather than seeing alerts only as isolated events, analysts can understand them through the language of **tactics, techniques, and attacker behavior**.

---

## 🧠 What I Learned

Through this project, I strengthened my understanding of:

* how Wazuh exposes MITRE ATT&CK fields in security alerts
* how ATT&CK mapping improves investigation context
* how tactic- and technique-based visualization supports SOC workflows
* how time-based technique visibility can reveal attack progression
* how to organize ATT&CK-focused dashboards for both learning and practical reuse

---

## 📦 Dashboard Import / Reuse

This project also includes the exported dashboard JSON file:

`
SOC – MITRE ATT&CK Coverage Dashboard.ndjson
`
- or **[click here](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/21-dashboards/02-soc-mitre-attack-coverage-dashboard/resources/SOC%20%E2%80%93%20MITRE%20ATT%26CK%20Coverage%20Dashboard.ndjson)**


This allows the full dashboard to be re-imported later and preserves the same dashboard object structure used in the project.

The JSON file is useful for:

* reproducibility
* backup
* re-import into another Wazuh environment
* preserving dashboard configuration
* portfolio evidence of implementation

Even with the JSON preserved, this README still documents the full process step by step so the project remains useful for hands-on learning.

---

## 🔗 Helpful References

For custom Wazuh dashboard creation guidance, review the [official Wazuh dashboard creation guide](https://documentation.wazuh.com/current/user-manual/wazuh-dashboard/creating-custom-dashboards.html).

For framework-level ATT&CK reference, review the [official MITRE ATT&CK knowledge base](https://attack.mitre.org/).

For Wazuh dashboard usage more broadly, you can also refer to the [Wazuh dashboard user manual](https://documentation.wazuh.com/current/user-manual/wazuh-dashboard/index.html).

---

## 🧾 Conclusion

This project demonstrates how to build a **SOC MITRE ATT&CK Coverage Dashboard in Wazuh** that transforms raw security alerts into structured ATT&CK-based threat visibility.

Instead of only monitoring severity and volume, the dashboard helps analysts understand:

* what attack stage is active
* what techniques are being used
* which ATT&CK IDs are present
* how adversary behavior changes over time

This makes the dashboard a practical tool for:

* SOC monitoring
* ATT&CK-aligned investigation
* threat analysis
* detection engineering context
* structured reporting

It reflects a more mature SOC approach where detections are interpreted not only as alerts, but as **observable attacker behavior**.

---
