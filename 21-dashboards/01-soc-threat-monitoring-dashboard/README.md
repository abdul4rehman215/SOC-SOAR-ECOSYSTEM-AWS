# 🚨 SOC Threat Monitoring Dashboard

## 🌐 Project Overview

This project demonstrates how I built a **SOC Threat Monitoring Dashboard in Wazuh** to improve analyst visibility, speed up triage, and make security activity easier to understand than reviewing raw alerts alone.

In a real SOC environment, analysts often face:

- large volumes of alerts
- repeated noisy events
- difficulty prioritizing important detections
- slow manual investigation from raw logs only
- limited immediate visibility into attacker sources and activity spikes

To address that, this project uses **Wazuh Dashboard / OpenSearch Dashboards visualizations** to create a centralized operational view of security activity.

This dashboard was designed to help answer practical SOC questions such as:

- Which alerts are most severe right now?
- Which alert types are appearing most often?
- Which source IPs are generating suspicious activity?
- Where are attacks coming from geographically?
- When do attack spikes occur over time?

Rather than treating dashboards as just a reporting feature, this project approaches them as a **security operations tool for faster detection, prioritization, and investigation**.

---

## 🖼️ Dashboard Screenshots

### Visualization Listing View

<div align="center">
<img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/21-dashboards/01-soc-threat-monitoring-dashboard/resources/2.png"/>
</div>

### Full Dashboard View

<div align="center">
<img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/21-dashboards/01-soc-threat-monitoring-dashboard/resources/3.png"/>
</div>

### High Severity Attack Timeline

<div align="center">
<img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/21-dashboards/01-soc-threat-monitoring-dashboard/resources/4.png"/>
</div>

### Attack Source Geo Map

<div align="center">
<img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/21-dashboards/01-soc-threat-monitoring-dashboard/resources/5.png"/>
</div>

---

## 🎯 Project Objective

The objective of this project was to design and document a **Wazuh-based threat monitoring dashboard** that helps SOC analysts:

- monitor medium to high severity security alerts
- identify dominant attack patterns
- highlight suspicious source IP addresses
- observe geographic attack sources using GeoIP-based mapping
- detect bursts of attack activity through timeline visualization
- improve triage efficiency through centralized visibility

This project was also created with a **learning-first and reproducible approach**:

- the full dashboard is preserved through an exported `.json` file
- the README explains the dashboard creation process step by step
- the project remains useful for both **import/reuse** and **hands-on learning**

---

## 🛡️ SOC Problem This Dashboard Solves

In real security operations, analysts often do not begin with perfect context. They begin with telemetry, alerts, and uncertainty.

Without a dashboard, analysts may need to:

- manually search the `wazuh-alerts-*` index
- review alerts one by one
- filter different fields repeatedly
- compare alert patterns across multiple views
- spend extra time understanding whether a spike is meaningful

This dashboard improves that workflow by providing a centralized visual view of:

- alert severity distribution
- top alert categories
- most active attacker IPs
- attack-source geographic visibility
- high-severity alert patterns over time

This directly supports:

- faster triage
- quicker prioritization
- improved situational awareness
- better detection understanding
- more efficient daily SOC monitoring

---

## 🧠 Why This Project Matters

This project matters because dashboards make Wazuh data **operationally usable**.

A SOC may already have detections, rules, and indexed events, but that alone is not enough. Analysts also need a way to:

- quickly see what matters
- identify the biggest sources of security activity
- separate signal from noise
- understand patterns visually
- investigate efficiently under time pressure

This threat monitoring dashboard helps bridge the gap between:

**raw alert ingestion**  
and  
**analyst-friendly security monitoring**

It shows how dashboard engineering supports:

- detection engineering
- SOC monitoring workflows
- attack visibility
- triage efficiency
- investigation readiness

---

## 📌 What This Dashboard Helps Analysts See

This project is centered around five core visualizations that answer practical SOC questions.

| SOC Question | Visualization Used |
|---|---|
| What severity alerts exist? | Alerts by Severity |
| Which attack types are most common? | Top Alert Types |
| Which IPs are attacking? | Top Attacker IPs |
| Where are attacks coming from? | Attack Source Geo Map |
| When do attacks spike? | High Severity Attack Timeline |

Together, these panels create a usable **SOC Threat Monitoring Dashboard**.

---

## 🏗️ Architecture Used in This Project

```text
Attacker Machine (Kali Linux EC2)
        |
        | Attack Simulation
        |
Target / Monitored Endpoint
(Ubuntu / Windows with Wazuh Agent)
        |
        | Security Logs / Alert Data
        |
Wazuh Manager + Indexer
        |
        | Alert Processing / Rule Matching / Indexing
        |
Wazuh Dashboard (OpenSearch Dashboards GUI)
        |
        | Visualization Layer
        |
SOC Threat Monitoring Dashboard
        |
        | Analyst Triage / Monitoring / Investigation
        |
SOC Analyst
````

This project only focuses on the **dashboard engineering and visualization layer**.
Wazuh deployment and Wazuh agent installation are documented separately in other folders of the repository, so they are intentionally not repeated here.

---

## 🧰 Technologies Used

```text
Wazuh SIEM
Wazuh Dashboard / OpenSearch Dashboards
AWS EC2
Kali Linux (attack simulation)
Ubuntu / Windows monitored endpoints
GeoIP enrichment / geolocation visibility
Wazuh alert rules
MITRE ATT&CK-mapped alerts
```

---

## 📋 Prerequisites

Before reproducing or understanding this project, the following prerequisites are useful.

### Technical Knowledge

* Basic understanding of Wazuh alerts and rule levels
* Basic understanding of SOC workflows
* Familiarity with security alert triage
* Basic understanding of OpenSearch / Wazuh dashboard interface
* Basic awareness of brute-force and authentication attack patterns

### Environment Prerequisites

* Wazuh environment already deployed
* Wazuh dashboard accessible
* At least one monitored endpoint sending logs
* Alert data available in `wazuh-alerts-*`
* GeoIP/geolocation visibility available for source IP mapping
* Security events generated from realistic activity or attack simulation

For official platform guidance on dashboard building, refer to the [Wazuh custom dashboard creation guide](https://documentation.wazuh.com/current/user-manual/wazuh-dashboard/creating-custom-dashboards.html).

---

## 🖥️ Environment Context

This dashboard project was built as part of an **AWS-based SOC ecosystem**.

### Environment Summary

* **Project Type:** Self-performed SOC engineering / monitoring project
* **Primary Platform:** AWS EC2
* **SIEM Layer:** Wazuh
* **Visualization Layer:** Wazuh Dashboard / OpenSearch Dashboards
* **Attack Simulation Source:** Kali Linux EC2
* **Monitored Systems:** Wazuh-connected endpoint(s)
* **Primary Use Case:** SOC threat visibility and alert triage

---

## 🔎 Project Scope

This project focuses specifically on creating a **SOC Threat Monitoring Dashboard** inside Wazuh.

It does **not** cover:

* Wazuh server installation
* Wazuh agent deployment
* deep rule authoring from scratch
* response automation
* alert forwarding integrations
* external SOAR workflows

Those are covered elsewhere in the broader repository.

This project focuses on:

* using already available Wazuh data
* selecting the right alert fields for monitoring
* creating threat-focused visualizations
* organizing panels into a practical dashboard
* documenting the full process clearly
* preserving the exported dashboard for import/reuse

---

## 📁 Repository Structure

```text
01-soc-threat-monitoring-dashboard/
├── README.md
├── architecture.txt
├── interview_qna.md
├── troubleshooting.md
└── resources/
    ├── SOC – Wazuh Threat Monitoring Dashboard.ndjson
    └── images
```

---

## 🧭 Implementation Strategy

The dashboard was designed around practical SOC questions rather than random charts.

### Design Approach

1. Identify the threat monitoring problem
2. Confirm that relevant Wazuh alerts are visible in `wazuh-alerts-*`
3. Select the most useful fields for analyst visibility
4. Build visualizations that support triage and investigation
5. Combine those visualizations into one dashboard
6. Preserve the full dashboard as JSON
7. Document the entire process for reproducibility and learning

---

## 🪜 Step-by-Step Implementation Guide

## Step 1 — Confirm Alert Data Is Available

Before building any visualization, confirm that Wazuh is already ingesting alerts into the dashboard.

Open the Wazuh dashboard and navigate to:

```text
Discover
```

Use the index pattern:

```text
wazuh-alerts-*
```

Review alert fields such as:

```text
timestamp
agent.name
agent.ip
data.srcip
data.srcuser
rule.id
rule.description
rule.level
rule.firedtimes
```

This step confirms that the dashboard has enough underlying security data for visualization.

---

## Step 2 — Identify Relevant Threat Monitoring Signals

For this dashboard, the main focus is on **medium to high severity security activity**.

The most useful signals for this use case were:

* alert severity (`rule.level`)
* alert description (`rule.description`)
* source IP (`data.srcip`)
* timestamp (`timestamp`)
* geographic source visibility (GeoIP-enriched source fields where available)

This lets the dashboard surface:

* severity distribution
* dominant alert categories
* likely attacker IPs
* attack-source regions
* spikes in attack activity

---

## Step 3 — Define the Severity Window

Wazuh rule levels range broadly from informational to critical.

For this threat-monitoring dashboard, the focus is on:

```text
rule.level between 8 and 15
```

This provides a cleaner operational view by emphasizing alerts more relevant to security investigation rather than lower-signal informational noise.

This severity filter is especially important for:

* top attacker IPs
* geo map visibility
* high severity attack timeline

---

## Step 4 — Plan the Dashboard Panels

The dashboard was intentionally built with five panels:

### 1. SOC – Alerts by Severity

Shows how alerts are distributed by severity level.

### 2. SOC – Top Alert Types

Shows the most common alert categories.

### 3. SOC – Top Attacker IPs

Shows which source IPs are generating the most high-severity alerts.

### 4. SOC – Attack Source Geo Map

Shows where suspicious activity is coming from geographically.

### 5. SOC – High Severity Attack Timeline

Shows when higher-severity activity spikes over time.

These panels together create a compact but practical dashboard for daily SOC monitoring.

---

## Step 5 — Create the “SOC – Alerts by Severity” Visualization

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
Field → rule.level
Order By → Metric: Count
Order → Descending
Size → 10
```

### Style / Options

Enable:

```text
Donut
Show labels
Show values
Show tooltip
```

### Save As

```text
SOC – Alerts by Severity
```

### Description

```text
Displays distribution of security alerts based on Wazuh rule severity levels to help SOC analysts quickly identify high-risk events.
```

---

## Step 6 — Create the “SOC – Top Alert Types” Visualization

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
Field → rule.description
Order By → Metric: Count
Order → Descending
Size → 10
```

This shows the top alert categories seen in Wazuh.

### Save As

```text
SOC – Top Alert Types
```

### Description

```text
Highlights the most frequent security alert types detected by Wazuh, helping analysts identify dominant attack patterns and potential noisy alerts.
```

---

## Step 7 — Create the “SOC – Top Attacker IPs” Visualization

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

Before building the chart, apply a filter:

```text
rule.level is between 8 and 15
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
Field → data.srcip
Order By → Metric: Count
Order → Descending
Size → 10
```

This helps identify the most active suspicious source IP addresses.

### Save As

```text
SOC – Top Attacker IPs
```

### Description

```text
Identifies external IP addresses responsible for high-severity alerts, helping analysts detect brute-force attacks and intrusion attempts.
```

---

## Step 8 — Create the “SOC – Attack Source Geo Map” Visualization

Navigate to:

```text
Visualize → Create Visualization
```

Choose:

```text
Maps
```

Data source:

```text
wazuh-alerts-*
```

### Configuration Concept

* Add a document-based layer
* Use the source-IP-related geolocation field available in the environment
* Filter for `rule.level` between `8` and `15`
* Display count-based attack-source visibility

> Note: The exact geolocation field may vary depending on your Wazuh/OpenSearch enrichment pipeline and field availability. The dashboard JSON included in this project preserves the working dashboard state used in this environment.

### Save As

```text
SOC – Attack Source Geo Map
```

### Description

```text
Maps geographic origin of high-severity security alerts using GeoIP enrichment, enabling analysts to identify regional attack patterns.
```

---

## Step 9 — Create the “SOC – High Severity Attack Timeline” Visualization

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

Apply filter:

```text
rule.level between 8 and 15
```

### Configuration

**Metric**

```text
Aggregation → Count
```

**X-Axis**

```text
Aggregation → Date Histogram
Field → timestamp
Interval → Auto
```

This provides a timeline of higher-severity alert activity.

### Save As

```text
SOC – High Severity Attack Timeline
```

### Description

```text
Displays high-severity security alerts over time, helping analysts detect attack spikes, persistence activity, and brute-force attempts.
```

---

## Step 10 — Create the Dashboard

Navigate to:

```text
Dashboards → Create Dashboard
```

Name it:

```text
SOC – Wazuh Threat Monitoring Dashboard
```

Add the following panels:

```text
SOC – Alerts by Severity
SOC – Top Alert Types
SOC – Top Attacker IPs
SOC – Attack Source Geo Map
SOC – High Severity Attack Timeline
```

Recommended layout:

```text
Alerts by Severity        Top Alert Types

Top Attacker IPs          Attack Source Geo Map

High Severity Attack Timeline
```

This layout balances:

* overview
* source identification
* geographic context
* time-based monitoring

---

## 📈 Dashboard Analysis

Once built, this dashboard gives analysts immediate operational visibility.

### Alerts by Severity

This panel helps analysts quickly see whether the environment is dominated by:

* informational alerts
* medium severity noise
* higher-severity detections that need urgent review

### Top Alert Types

This panel helps identify:

* the most common alert categories
* repetitive security patterns
* potentially noisy detections
* brute-force or authentication-heavy activity

### Top Attacker IPs

This panel highlights the most active suspicious IP addresses and supports:

* quick triage
* blocking decisions
* investigation starting points
* identifying repeat external sources

### Attack Source Geo Map

This panel adds geographic context and helps reveal:

* regional source patterns
* repeated foreign-origin activity
* broad attack-source visibility
* useful reporting context for analyst summaries

### High Severity Attack Timeline

This panel highlights time-based attack behavior such as:

* spikes in suspicious activity
* repeated attack bursts
* likely brute-force periods
* persistence-style repeated activity

---

## 🔍 Security Insights This Dashboard Supports

With this dashboard, analysts can quickly answer questions like:

```text
Where are attacks coming from?
What attack type appears most often?
Which IP is generating the most suspicious traffic?
Are high-severity alerts increasing?
When did attack activity spike?
Which events should be prioritized first?
```

Without a dashboard, these answers would require repeated manual searching in raw event data.

---

## ✅ Result

This project successfully demonstrates:

* Wazuh-based threat visibility engineering
* practical dashboard creation for SOC use
* alert severity monitoring
* attack-source analysis
* geolocation-based visualization
* time-based security trend visibility
* analyst-focused triage improvement

The resulting dashboard provides a centralized operational security view that helps SOC analysts move faster from **alert visibility** to **investigation and prioritization**.

---

## 🌍 Real-World Applications

This type of dashboard is useful for:

* daily SOC monitoring
* brute-force detection visibility
* attack trend analysis
* alert prioritization
* suspicious IP analysis
* reporting security activity to operational teams
* identifying noisy detections for tuning
* monitoring threat patterns across time

---

## 🌐 Real-World Relevance

In real SOC environments, dashboards like this are used to reduce the gap between:

* raw alert generation
* real analyst action

They help turn security data into something practical and immediately usable.

A dashboard like this is especially relevant for:

* Tier 1 / Tier 2 analyst triage
* blue team operations
* shift handoff visibility
* threat monitoring review
* detection engineering feedback loops
* incident investigation starting points

---

## 🧠 What I Learned

Through this project, I strengthened my understanding of:

* how Wazuh alerts can be transformed into analyst-friendly monitoring panels
* how severity filtering improves operational focus
* how source IP and alert-category views help with faster triage
* how geolocation and timeline views improve investigation context
* how dashboard engineering supports real SOC workflows beyond simple reporting

---

## 📦 Dashboard Import / Reuse

This project also includes the exported dashboard JSON file:

```text
SOC – Wazuh Threat Monitoring Dashboard.ndjson
```

- or **[click here](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/21-dashboards/01-soc-threat-monitoring-dashboard/resources/SOC%20%E2%80%93%20Wazuh%20Threat%20Monitoring%20Dashboard.ndjson)**

This makes it possible to preserve and re-import the same dashboard layout and visualization structure later.

The JSON file is useful for:

* reproducibility
* backup
* sharing the dashboard design
* quickly rebuilding the same dashboard in another Wazuh environment

Even with the JSON preserved, this README intentionally includes the full dashboard-building guide for learning and hands-on understanding.

---

## 🔗 Helpful References

For platform-level dashboard creation guidance, you can review the [official Wazuh documentation for creating custom dashboards](https://documentation.wazuh.com/current/user-manual/wazuh-dashboard/creating-custom-dashboards.html).

For broader Wazuh dashboard usage and navigation, you can also explore the [Wazuh dashboard user manual](https://documentation.wazuh.com/current/user-manual/wazuh-dashboard/index.html).

---

## 🧾 Conclusion

This project demonstrates how to build a **practical SOC Threat Monitoring Dashboard in Wazuh** that supports analyst workflows through visualization, filtering, and operational context.

Instead of relying only on raw alerts, the dashboard provides a centralized monitoring view that helps analysts:

* understand severity distribution
* identify dominant attack types
* investigate suspicious source IPs
* observe global attack-source patterns
* detect spikes in attack activity over time

This makes the dashboard not just a visualization exercise, but a meaningful part of **SOC operations, detection visibility, and faster security triage**.

---

## 🌐 Project Post on LinkedIn

I also shared this project on LinkedIn with a concise portfolio summary, key highlights, and implementation context.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-View%20Project%20Post-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/posts/abdul4rehman215_socanalyst-handsonlearning-wazuh-activity-7416924504947380224-i3TI?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEuho14BQnjOksWA5iihN6dnsE3C-o3yBUU)

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
