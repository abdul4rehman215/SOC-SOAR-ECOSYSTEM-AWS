# 🧪 Wazuh Module Exploration & Learning Projects

## 🌐 Project Overview

This folder contains a set of **learning-focused, hands-on Wazuh module exploration projects** completed as part of my broader **SOC-SOAR-ECOSYSTEM-AWS** environment.

Unlike full deployment or incident-response projects, this folder is focused on **exploration, understanding, analyst thinking, visibility use cases, and practical feature learning**.

The goal of these projects was to go beyond simple installation or clicking around the interface and instead understand:

- what each Wazuh module actually does
- how it supports a SOC analyst or security engineer
- why certain modules are often ignored or underused
- how each feature adds context, visibility, and operational value
- what practical use cases exist in real security workflows
- what I learned by exploring the module directly in the dashboard and related views

This folder is designed as a **special learning-project directory** for Wazuh features and modules that deserve deeper attention.

---

## 🎯 Project Objective

The objective of this folder is to document my **structured exploration of important Wazuh features and modules** from a practical SOC perspective.

This parent folder was created to:

- organize module-level exploration projects in one place
- document how Wazuh provides more than just alerts
- understand overlooked visibility features in Wazuh
- capture learning outcomes from hands-on feature exploration
- explain practical analyst benefits of each module
- show how these modules support investigation, monitoring, posture awareness, and risk reduction
- build a reusable learning portfolio around Wazuh feature exploration

---

## 🛡️ Why This Folder Matters

In many SOC environments, users focus only on:

- triggered alerts
- dashboard summaries
- rules and active incidents

But Wazuh provides many deeper features that help analysts understand:

- endpoint health
- baseline behavior
- software inventory
- process visibility
- network exposure
- service posture
- hidden threat patterns
- pipeline context
- vulnerability posture

These features are often underused because:

- people are trained to react to alerts first
- many teams overlook context-focused modules
- some views feel “operational” rather than “security-related”
- the value becomes clear only after deeper exploration

This folder matters because it documents why these modules should **not** be ignored.

---

## 🧠 Learning Philosophy of This Folder

These are not just “feature notes.”

Each subproject in this folder is treated as a **practical hands-on learning exploration** with the following mindset:

- understand the feature deeply
- view it from a SOC analyst perspective
- connect it to investigation and monitoring workflows
- identify real-world use cases
- document why the feature is useful
- explain what I learned from exploring it
- preserve the learning in structured project format

This makes the folder useful for:

- portfolio presentation
- future revision
- teaching others
- understanding underused Wazuh capabilities
- expanding beyond alert-only workflows

---

## 🏗️ Parent Folder Scope

This parent folder currently includes four exploration subprojects:

1. **IT Hygiene Module Exploration**
2. **Threat Hunting Module Exploration**
3. **Discover Indices / Index Patterns Exploration**
4. **Vulnerability Detection Module Exploration**

These four projects focus on different aspects of Wazuh visibility and capability.

They are connected by one common idea:

> **A mature SOC should not rely only on alerts.  
> It should also understand context, state, inventory, posture, and behavior.**

---

## 📁 Repository Structure

```text
22-learning-projects/
├── README.md
├── 01-it-hygiene-module-exploration/
│   ├── README.md
│   ├── architecture-notes.txt
│   └── interview_qna.md
├── 02-threat-hunting-module-exploration/
│   ├── README.md
│   ├── architecture-notes.txt
│   └── interview_qna.md
├── 03-wazuh-discover-indices-exploration/
│   ├── README.md
│   ├── architecture-notes.txt
│   └── interview_qna.md
└── 04-vulnerability-detection-module-exploration/
    ├── README.md
    ├── architecture-notes.txt
    └── interview_qna.md
````

> This folder may be extended later with more Wazuh module and feature explorations as the learning portfolio grows.

---

## 🔍 Modules Covered in This Folder

---

## 1. 🧼 IT Hygiene Module Exploration

This subproject focuses on the **Wazuh IT Hygiene module**, which provides a centralized, real-time view of endpoint state and inventory.

The exploration covered practical visibility such as:

* operating system and hardware context
* CPU and memory usage
* installed software/packages
* running processes
* network activity and listening ports
* active services and service state
* user/account and host inventory awareness

### Why this matters

IT Hygiene is often ignored because it does not look like a traditional alert module.

But in reality, it is extremely valuable for:

* baseline understanding
* endpoint context
* misconfiguration visibility
* suspicious service review
* software hygiene visibility
* SOC investigation support

This exploration showed that before asking “Is this malicious?”, analysts often first need to understand:

> **What is normal on this endpoint?**

---

## 2. 🕵️ Threat Hunting Module Exploration

This subproject focuses on the **Wazuh Threat Hunting module** and how it helps analysts investigate behavior proactively instead of waiting only for high-severity alerts.

The exploration included practical understanding of:

* event baselining
* behavioral review over time
* agent-based analysis
* low-level signal correlation
* event-level investigation
* MITRE ATT&CK context
* pattern analysis outside alert-driven workflows

### Why this matters

Threat hunting is often underused because many teams stay inside alert queues and incident lists.

But real attackers often rely on:

* normal-looking behavior
* quiet activity
* repeated low-level patterns
* small anomalies over time

This exploration showed that threat hunting helps analysts find:

* what alerts missed
* what patterns do not yet look critical
* what behaviors need deeper attention

---

## 3. 🧭 Wazuh Discover Indices Exploration

This subproject focuses on the **different Wazuh Discover indices / index patterns** that many analysts rarely use beyond `wazuh-alerts-*`.

The exploration covered index families such as:

* `wazuh-alerts-*`
* `wazuh-archives-*`
* `wazuh-monitoring-*`
* `wazuh-statistics-*`
* `wazuh-states-*`
* `wazuh-states-inventory-*`

### Why this matters

Alerts tell analysts that something happened.

But these other indices help explain:

* whether the agent was healthy
* whether the pipeline dropped events
* what packages existed
* what processes were running
* what services and ports were present
* what raw events existed before or outside alerting

This exploration showed that these “ignored” indices are actually essential for:

* root cause analysis
* telemetry validation
* false negative investigation
* threat hunting
* host context
* detection engineering

---

## 4. 🧱 Vulnerability Detection Module Exploration

This subproject focuses on the **Wazuh Vulnerability Detection module** and how it supports continuous, inventory-driven vulnerability visibility.

The exploration included practical understanding of:

* Syscollector inventory collection
* package-to-CVE correlation
* dashboard summary views
* inventory tab analysis
* event tab review
* active vs solved findings
* CVSS and severity context
* vulnerability detail views
* CTI / reference links
* remediation confirmation

### Why this matters

This module is often underestimated because many people compare it directly with active network scanners.

But this exploration showed its real value in:

* endpoint-based vulnerability visibility
* package-level risk understanding
* remediation tracking
* asset-specific prioritization
* ongoing posture awareness

This makes it useful not just for vulnerability teams, but also for:

* SOC analysts
* blue teams
* security engineers
* patch validation workflows

---

## ⚙️ What This Parent Folder Demonstrates

This folder demonstrates practical learning and exploration in areas such as:

* Wazuh feature exploration
* analyst-focused visibility thinking
* inventory and posture awareness
* proactive investigation mindset
* dashboard and Discover-based analysis
* endpoint context enrichment
* telemetry trust validation
* vulnerability understanding
* module-level operational value assessment

---

## 🧰 Prerequisites

Before working through or understanding these module explorations, the following background is helpful:

### Technical Prerequisites

* Basic understanding of Wazuh architecture
* Familiarity with Wazuh agents and manager concepts
* Basic SOC monitoring knowledge
* Familiarity with dashboard and Discover workflows
* Basic understanding of alerts, telemetry, and endpoint context
* General understanding of security operations concepts

### Environment Prerequisites

* Functional Wazuh deployment
* Wazuh Dashboard access
* Monitored endpoints / agents
* Enough telemetry or host data for meaningful exploration
* Curiosity to study context, not just alerts

---

## 🖥️ Environment Context

These explorations were performed in the context of my **AWS-based SOC ecosystem**, where Wazuh acts as a central SIEM / XDR / visibility platform.

### Environment Summary

* **Platform:** AWS-based SOC lab / project environment
* **Primary Security Platform:** Wazuh
* **Focus:** Feature exploration, learning, analyst visibility, and module understanding
* **Project Style:** Self-performed, hands-on, exploration-based learning
* **Purpose:** Practical learning, structured documentation, and portfolio building

---

## 🚀 Real-World Applications

The features explored in this folder have strong real-world applications across security teams.

### IT Hygiene helps with:

* endpoint context review
* suspicious service discovery
* software inventory review
* host baseline understanding
* early hygiene problem identification

### Threat Hunting helps with:

* proactive investigation
* low-level signal analysis
* suspicious behavior review
* attacker pattern analysis
* discovering what alerts missed

### Discover Indices help with:

* root cause analysis
* monitoring validation
* pipeline troubleshooting
* archive-based review
* state and inventory investigation

### Vulnerability Detection helps with:

* package-level exposure visibility
* remediation validation
* risk prioritization
* asset-specific vulnerability awareness
* continuous posture monitoring

---

## 🌍 Real-World Relevance

In real SOC operations, analysts often need more than just “a list of alerts.”

They also need to understand:

* Is the host healthy?
* What is normal on this endpoint?
* Are we missing data?
* Did this package exist before the alert?
* Was the service running?
* Are vulnerabilities still active or already solved?
* Was the telemetry complete?
* Is this just noise, or part of a larger pattern?

This folder reflects that reality by focusing on **visibility, context, and deeper operational understanding**.

---

## 📚 Official References Used for Learning

These explorations were supported by a mix of practical hands-on use and official Wazuh documentation/resources.

Useful references include:

* [Wazuh IT Hygiene documentation / use case references](https://documentation.wazuh.com/current/getting-started/use-cases/it-hygiene.html)
* [Wazuh Threat Hunting documentation / use case references](https://documentation.wazuh.com/current/getting-started/use-cases/threat-hunting.html)
* [Wazuh Indexer indices documentation](https://documentation.wazuh.com/current/user-manual/wazuh-indexer/wazuh-indexer-indices.html)
* [Wazuh Vulnerability Detection documentation](https://documentation.wazuh.com/current/user-manual/capabilities/vulnerability-detection/index.html)

These references helped reinforce the technical understanding behind the hands-on module exploration.

---

## 🧠 What I Learned

Through this parent folder and its subprojects, I strengthened my understanding that Wazuh is much more than:

* alerting
* dashboard summaries
* simple event monitoring

I learned that mature use of Wazuh also involves:

* understanding endpoint context
* studying behavior over time
* using hidden or ignored data sources
* validating telemetry trust
* analyzing inventory and host state
* connecting vulnerability information to actual risk
* thinking like an analyst, not only like an alert responder

---

## 📌 Result

By completing these four exploration subprojects:

* I documented underused Wazuh modules and features in a structured way
* I preserved practical learning from direct hands-on exploration
* I built reusable learning-oriented subprojects for future review
* I strengthened my SOC understanding beyond alert-only workflows
* I created a strong portfolio section focused on visibility, context, and module capability analysis

---

## 🧾 Conclusion

This folder represents the **Wazuh learning, exploration, and feature-understanding layer** of my SOC portfolio.

Instead of focusing only on major deployments or active incidents, this folder captures an equally important part of SOC growth:

* understanding the platform deeply
* exploring overlooked features
* learning how modules support analysts
* identifying why some capabilities are underused
* documenting what operational value they provide

The four current subprojects — **IT Hygiene, Threat Hunting, Discover Indices, and Vulnerability Detection** — together show how Wazuh can support a much richer security workflow when used beyond basic alert review.

This folder may continue to grow later as I explore more Wazuh modules, features, and practical analyst use cases.

---

## 🔗 Included Subprojects

This parent folder currently includes:

* **IT Hygiene Module Exploration**
* **Threat Hunting Module Exploration**
* **Wazuh Discover Indices Exploration**
* **Vulnerability Detection Module Exploration**

Each subproject is documented separately with:

* `README.md`
* `architecture-notes.txt`
* `interview_qna.md`

This keeps the learning organized, reusable, and portfolio-ready.

---
