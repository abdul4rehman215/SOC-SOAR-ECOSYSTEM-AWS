# ✅ SOC Compliance & CIS Benchmark Dashboard

## 🌐 Project Overview

This project demonstrates how I built a **SOC Compliance & CIS Benchmark Dashboard using Wazuh Security Configuration Assessment (SCA)** to monitor system hardening posture, identify misconfigurations, and improve visibility into security baseline compliance across monitored systems.

Unlike threat-monitoring dashboards that focus on **active attacks, suspicious events, and incident triage**, this dashboard focuses on **security posture and configuration hygiene**.

It helps answer practical questions such as:

- Are monitored systems aligned with CIS hardening guidance?
- Which CIS controls fail most often?
- Are configuration issues improving or worsening over time?
- Which misconfigurations should be prioritized first?
- How strong is the current compliance posture across endpoints?

This project turns raw SCA findings into a centralized, visual dashboard that makes compliance and hardening visibility easier for SOC teams, defenders, and security engineers.

---

## 🖼️ Dashboard Screenshots

### Visualization Listing View

<div align="center">
<img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/21-dashboards/03-soc-compliance-cis-benchmark-dashboard/resources/2.png"/>
</div>

### Full Dashboard View

<div align="center">
<img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/21-dashboards/03-soc-compliance-cis-benchmark-dashboard/resources/3.png"/>
</div>

### Top Failed CIS Checks View

<div align="center">
<img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/21-dashboards/03-soc-compliance-cis-benchmark-dashboard/resources/4.png"/>
</div>

---

## 🎯 Project Objective

The objective of this project was to build a **Wazuh-based compliance and CIS benchmark dashboard** that helps security teams:

- visualize system hardening posture across monitored endpoints
- monitor pass/fail distribution of CIS-related checks
- identify the most frequently failing CIS controls
- observe compliance findings over time
- support remediation prioritization
- improve audit readiness and baseline security visibility

This project was also documented with a **learning-first and reusable approach**:

- the dashboard itself is preserved as an exported `.json` file
- the README explains how it was built step by step
- the project remains useful both for **re-import** and for **hands-on learning**

---

## 🛡️ SOC Problem This Dashboard Solves

A SOC does not only monitor active attacks. It must also monitor whether systems are **securely configured in the first place**.

Many security incidents become possible because of weak hardening or poor baseline controls, such as:

- insecure SSH settings
- weak password controls
- missing logging configurations
- dangerous default settings
- poorly hardened remote access controls
- misconfigurations that expand the attack surface

Without a compliance dashboard, analysts or engineers may need to manually inspect thousands of individual SCA findings to understand the current posture.

This dashboard solves that by giving centralized visibility into:

- overall compliance posture
- pass vs fail distribution
- top failed CIS checks
- compliance trends across time

This makes configuration risk easier to understand, prioritize, and communicate.

---

## 🧠 Why This Project Matters

This project matters because **misconfigurations are often easier for attackers to exploit than advanced vulnerabilities**.

A mature SOC needs visibility into both:

1. **active threats**
2. **security posture**

This dashboard supports the second area by helping teams identify where systems are not aligned with secure CIS-oriented configurations.

It is useful for:

- reducing attack surface
- identifying repeat hardening failures
- prioritizing remediation work
- supporting internal reviews and audits
- understanding posture drift across systems
- strengthening security baseline monitoring inside the SOC

This makes the dashboard more than a reporting interface — it becomes part of security hygiene and risk reduction operations.

---

## 📌 What This Dashboard Helps Analysts and Engineers See

This dashboard was designed around practical compliance and hardening questions.

| SOC / Security Question | Visualization Used |
|---|---|
| What is the overall compliance posture? | Compliance – Overall Score |
| How many controls are passed vs failed? | Compliance – Pass vs Fail |
| Which CIS controls fail most often? | Compliance – Top Failed CIS Checks |
| How are compliance findings changing over time? | Compliance – Findings Timeline |

Together, these visualizations create a useful **SOC Compliance & CIS Benchmark Dashboard**.

---

## 🔍 What is Wazuh SCA?

Wazuh SCA stands for:

```text
Security Configuration Assessment
````

It is a Wazuh capability used to evaluate system configuration against security benchmarks and policies.

Examples include:

```text
CIS Benchmarks
PCI-DSS
NIST-aligned policies
Custom security policies
```

For this project, the focus was on **CIS benchmark visibility**.

Example CIS checks include:

```text
Ensure SSH root login is disabled
Ensure password complexity is enforced
Ensure firewall is enabled
Ensure SSH protocol version 2 is used
Ensure insecure authentication settings are disabled
```

Each check can produce results such as:

```text
passed
failed
not applicable
```

These results are the core data source for the dashboard.

---

## 🏗️ Architecture Used in This Project

```text
Endpoint Systems
(Windows / Linux)
        |
        | Wazuh Agent
        |
        v
Wazuh Manager
(Log collection + SCA scans)
        |
        | Indexed SCA findings
        v
Wazuh Indexer (OpenSearch)
        |
        v
Wazuh Dashboard
(SOC Compliance Visualization)
        |
        v
SOC Compliance & CIS Benchmark Dashboard
        |
        v
SOC Analyst / Security Engineer / Auditor / Blue Team
```

This project focuses only on the **dashboard engineering and visualization layer**.

Wazuh deployment and Wazuh agent setup are already documented separately elsewhere in the repository, so they are intentionally not repeated here.

---

## 🧰 Technologies Used

```text
Wazuh SIEM
Wazuh SCA (Security Configuration Assessment)
Wazuh Dashboard / OpenSearch Dashboards
CIS benchmark policy checks
AWS EC2
Ubuntu and Windows monitored systems
OpenSearch visualizations
```

---

## 📋 Prerequisites

Before reproducing or understanding this project, the following prerequisites are useful.

### Technical Knowledge

* Basic understanding of Wazuh alerts and modules
* Basic understanding of CIS benchmarks
* Basic awareness of secure configuration and hardening
* Familiarity with Wazuh Dashboard / Discover / Visualize sections
* Basic understanding of compliance and posture monitoring concepts

### Environment Prerequisites

* A working Wazuh environment already deployed
* Wazuh agents already connected
* SCA data being generated and indexed
* Compliance findings visible in `wazuh-alerts-*`
* Linux and/or Windows endpoints with SCA policy evaluation enabled

For official dashboard-building guidance, refer to the [Wazuh custom dashboard creation documentation](https://documentation.wazuh.com/current/user-manual/wazuh-dashboard/creating-custom-dashboards.html).

For broader Wazuh SCA guidance, refer to the [Wazuh Security Configuration Assessment documentation](https://documentation.wazuh.com/current/user-manual/capabilities/sec-config-assessment/index.html).

---

## 🖥️ Environment Context

This dashboard project was built as part of an **AWS-based SOC ecosystem** using Wazuh as the central monitoring and visibility platform.

### Environment Summary

* **Project Type:** Self-performed SOC engineering / compliance visibility project
* **Primary SIEM:** Wazuh
* **Compliance Data Source:** Wazuh SCA findings
* **Visualization Layer:** Wazuh Dashboard / OpenSearch Dashboards
* **Monitored Endpoints:** Ubuntu Linux and Windows systems
* **Infrastructure:** AWS EC2
* **Primary Goal:** Transform raw CIS benchmark findings into a practical posture dashboard

---

## 🔎 Project Scope

This project focuses specifically on building a **SOC Compliance & CIS Benchmark Dashboard** using Wazuh SCA data.

It focuses on:

* isolating compliance-related events
* validating useful SCA fields
* building posture-oriented visualizations
* creating a centralized compliance dashboard
* documenting the process clearly
* preserving the dashboard JSON for re-import and reuse

It does **not** focus on:

* Wazuh installation
* Wazuh agent deployment
* initial onboarding of endpoints
* non-SCA event sources
* attack simulation
* response orchestration

Those topics are documented in other parts of the main repository.

---

## 📁 Repository Structure

```text
03-soc-compliance-cis-benchmark-dashboard/
├── README.md
├── architecture.txt
├── troubleshooting.md
├── interview_qna.md
└── resources/
    ├── SOC – Compliance & CIS Benchmark Dashboard.ndjson
    └── images
```

---

## 🧭 Implementation Strategy

This dashboard was built around a simple idea:

> **Security posture should be visualized as clearly as active threats.**

### Design Approach

1. Confirm SCA data is present in Wazuh
2. Filter only compliance-related events
3. Identify the most useful SCA fields
4. Build visualizations for score, status distribution, failed checks, and trends
5. Combine them into one dashboard
6. Preserve the dashboard as JSON
7. Document the full workflow for reuse and learning

---

## 🪜 Step-by-Step Implementation Guide

## Step 1 — Confirm SCA Data Is Available

Before building any dashboard panels, first confirm that Wazuh is already receiving and indexing SCA findings.

Open:

```text
Discover
```

Use the index pattern:

```text
wazuh-alerts-*
```

Then apply this filter:

```text
rule.groups is sca
```

This isolates only **Security Configuration Assessment events** and removes unrelated security alerts such as authentication, FIM, or network detections.

---

## Step 2 — Validate Important SCA Fields

Before creating visualizations, confirm that the required fields exist in the data.

Important fields for this project include:

```text
rule.groups
data.sca.check.title
data.sca.check.result
data.sca.policy
timestamp
```

Field meaning:

```text
rule.groups              → identifies SCA events
data.sca.check.title     → CIS control / check name
data.sca.check.result    → passed / failed / not applicable
data.sca.policy          → policy name such as CIS Ubuntu or CIS Windows
timestamp                → when the finding was recorded
```

If these fields are present, the data is ready for compliance dashboard visualization.

---

## Step 3 — Understand the Dashboard Design

This dashboard contains four main visualizations:

### 1. Compliance – Overall Score

Provides a high-level posture view.

### 2. Compliance – Pass vs Fail

Shows the overall distribution of SCA result states.

### 3. Compliance – Top Failed CIS Checks

Highlights which CIS checks fail most often.

### 4. Compliance – Findings Timeline

Shows how compliance findings change over time.

These panels together help security teams understand both **current posture** and **remediation priorities**.

---

## Step 4 — Create the “Compliance – Pass vs Fail” Visualization

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

Apply the filter:

```text
rule.groups is sca
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
Field → data.sca.check.result
Order By → Metric Count
Order → Descending
Size → 5
```

Expected values include:

```text
passed
failed
not applicable
```

### Style / Options

Enable:

```text
Donut Mode
Show Legend
Show Labels
```

### Save As

```text
Compliance – Pass vs Fail
```

### Description

```text
Shows the distribution of CIS benchmark checks by result (passed, failed, not applicable), providing a quick overview of system configuration health.
```

---

## Step 5 — Create the “Compliance – Top Failed CIS Checks” Visualization

Navigate to:

```text
Visualize → Create Visualization
```

Choose:

```text
Horizontal Bar
```

Data source:

```text
wazuh-alerts-*
```

Apply the base filter:

```text
rule.groups is sca
```

Then add an additional filter:

```text
data.sca.check.result is failed
```

### Configuration

**Metric**

```text
Aggregation → Count
```

**Y-Axis**

```text
Aggregation → Terms
Field → data.sca.check.title
Order By → Metric Count
Order → Descending
Size → 10
```

**Split Series**

```text
Aggregation → Terms
Field → data.sca.policy
Size → 5
```

This separates repeated failed controls by benchmark/policy source.

### Save As

```text
Compliance – Top Failed CIS Checks
```

### Description

```text
Highlights the most frequently failing CIS benchmark controls across monitored systems, enabling prioritization of high-impact security misconfigurations.
```

---

## Step 6 — Create the “Compliance – Findings Timeline” Visualization

Navigate to:

```text
Visualize → Create Visualization
```

Choose:

```text
Area Chart
```

Data source:

```text
wazuh-alerts-*
```

Apply the filter:

```text
rule.groups is sca
```

### Configuration

**Metric**

```text
Aggregation → Count
```

**Chart Style**

```text
Area
Mode: Stacked
Line Mode: Straight
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
Field → data.sca.check.result
Size → 5
```

This helps show how pass/fail findings evolve over time.

### Panel Settings

Recommended:

```text
Legend Position: Right
Show Tooltip: Enabled
Current Time Marker: Disabled
```

### Save As

```text
Compliance – Findings Timeline
```

### Description

```text
Visualizes how CIS compliance findings change over time, helping identify trends, spikes, and the impact of remediation activities.
```

---

## Step 7 — Create the “Compliance – Overall Score” Visualization

Navigate to:

```text
Visualize → Create Visualization
```

Choose:

```text
Gauge
```

Data source:

```text
wazuh-alerts-*
```

Apply the filter:

```text
rule.groups is sca
```

### Configuration

**Metric**

```text
Aggregation → Count
```

### Gauge Ranges

Configure ranges such as:

```text
0 – 50
50 – 75
75 – 100
```

Recommended color logic:

```text
Green → healthier posture
Yellow → moderate concern
Red → weaker posture / attention needed
```

Enable:

```text
Show Legend
Show Scale
```

> Note: Gauge interpretation may vary depending on how the environment models total findings versus posture percentage. The exported dashboard JSON preserves the working state used in this project.

### Save As

```text
Compliance – Overall Score
```

### Description

```text
Displays the overall CIS compliance posture across monitored systems, enabling quick assessment of security baseline adherence.
```

---

## Step 8 — Create the Dashboard

Navigate to:

```text
Dashboards → Create Dashboard
```

Name it:

```text
SOC – Compliance & CIS Benchmark Dashboard
```

Add the following panels:

```text
Compliance – Overall Score
Compliance – Pass vs Fail
Compliance – Top Failed CIS Checks
Compliance – Findings Timeline
```

Recommended layout:

```text
Overall Score Gauges

Pass vs Fail             Findings Timeline

Top Failed CIS Checks
```

This layout gives:

* quick posture awareness
* result distribution
* time-based trend visibility
* remediation-focused findings visibility

---

## 📈 Dashboard Analysis

Once built, this dashboard provides strong visibility into configuration posture.

### Compliance – Overall Score

This gives a quick posture summary that can be useful for:

* high-level posture review
* quick health checks
* management-style visibility
* baseline adherence tracking

### Compliance – Pass vs Fail

This panel shows whether the environment is dominated by:

* passed checks
* failed checks
* non-applicable checks

This quickly communicates the overall compliance distribution.

### Compliance – Top Failed CIS Checks

This is one of the most useful remediation-focused panels. It highlights:

* repeated hardening failures
* the most common misconfigurations
* which controls should be fixed first
* whether the same controls fail across multiple policy scopes

### Compliance – Findings Timeline

This panel provides time-based posture context, such as:

* when findings increased
* when remediation reduced failures
* whether failed findings are recurring
* whether pass/fail ratios are improving

---

## 🔍 Security Insights This Dashboard Supports

This dashboard helps teams answer questions such as:

```text
Are systems meeting CIS baseline expectations?
Which hardening controls fail most often?
Are failed findings increasing or decreasing?
Which controls should be prioritized first?
Is the environment drifting away from secure baseline posture?
```

Without this type of dashboard, answering those questions would require repeated manual review of large volumes of individual SCA findings.

---

## ✅ Result

This project successfully demonstrates:

* Wazuh SCA-based posture visibility
* CIS benchmark dashboard engineering
* pass/fail compliance visualization
* failed-control prioritization
* trend analysis for compliance findings
* transformation of raw SCA data into usable SOC posture visibility

The resulting dashboard gives security teams a practical way to monitor baseline hardening and configuration risk using Wazuh.

---

## 🌍 Real-World Applications

This type of dashboard is useful for:

* CIS benchmark monitoring
* security baseline reviews
* remediation prioritization
* hardening validation
* internal compliance tracking
* blue team posture monitoring
* audit preparation support
* operational hygiene improvement

---

## 🌐 Real-World Relevance

In real environments, many compromises become easier because of:

* weak default settings
* incomplete hardening
* insecure services
* poor remote access configuration
* repeated configuration drift

This dashboard helps reduce that risk by making posture issues easier to see, communicate, and prioritize.

It is especially relevant for:

* SOC teams
* security engineers
* hardening teams
* audit/support functions
* enterprise baseline monitoring

---

## 🧠 What I Learned

Through this project, I strengthened my understanding of:

* how Wazuh SCA data can be used for posture dashboards
* how CIS benchmark findings can be visualized for remediation value
* how pass/fail and failed-control trends improve prioritization
* how compliance dashboards complement threat dashboards in a SOC
* how to structure reusable posture-visibility projects for learning and portfolio use

---

## 📦 Dashboard Import / Reuse

This project also includes the exported dashboard JSON file:

`
SOC – Compliance & CIS Benchmark Dashboard.ndjson
`

- or [click here](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/21-dashboards/03-soc-compliance-cis-benchmark-dashboard/resources/SOC%20%E2%80%93%20Compliance%20%26%20CIS%20Benchmark%20Dashboard.ndjson)

This makes it possible to preserve and re-import the same dashboard layout later.

The JSON file is useful for:

* reproducibility
* backup
* dashboard restoration
* portfolio evidence
* re-import into another Wazuh environment

Even with the JSON preserved, this README still includes the full process for learning and hands-on understanding.

---

## 🔗 Helpful References

For official dashboard-building guidance, review the [Wazuh custom dashboard creation guide](https://documentation.wazuh.com/current/user-manual/wazuh-dashboard/creating-custom-dashboards.html).

For official SCA capability details, review the [Wazuh Security Configuration Assessment documentation](https://documentation.wazuh.com/current/user-manual/capabilities/sec-config-assessment/index.html).

For CIS benchmark background, you can also review the [Center for Internet Security benchmarks overview](https://www.cisecurity.org/cis-benchmarks).

---

## 🧾 Conclusion

This project demonstrates how to build a **SOC Compliance & CIS Benchmark Dashboard in Wazuh** that transforms raw SCA findings into clear security posture visibility.

Instead of reviewing compliance findings one by one, the dashboard helps teams understand:

* where hardening is weakest
* which controls fail most often
* how posture changes over time
* which remediation efforts matter most

This makes the dashboard a practical part of **security posture monitoring, baseline enforcement, and attack-surface reduction** inside a SOC ecosystem.

---

## 🌐 Project Post on LinkedIn

I also shared this project on LinkedIn with a concise portfolio summary, key highlights, and implementation context.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-View%20Project%20Post-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/posts/abdul4rehman215_soc-socanalyst-mitreattack-activity-7417071722383855616-WVBF?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEuho14BQnjOksWA5iihN6dnsE3C-o3yBUU)

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
