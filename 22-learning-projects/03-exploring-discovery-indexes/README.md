# 🧭 Wazuh Discover Indices Exploration

## 🌐 Project Overview

This project documents my hands-on exploration of the **different Wazuh Discover indices / index patterns** that most people rarely use in daily SOC work.

In many environments, analysts spend almost all their time inside:

```text
wazuh-alerts-*
````

That is understandable, because alerts are where most incident handling begins.

But while exploring Wazuh Discover more deeply, I noticed that Wazuh stores much more than just alert data. It also stores operational, monitoring, statistical, archive, and inventory/state data through additional index patterns such as:

* `wazuh-monitoring-*`
* `wazuh-statistics-*`
* `wazuh-archives-*`
* `wazuh-states-*`
* `wazuh-states-inventory-*`

This exploration was about understanding a very important SOC question:

> **If alerts tell us what happened, what do the other indices tell us?**

The answer is powerful:

* alerts show the security event
* the other indices often show the **system state, telemetry health, endpoint inventory, infrastructure behavior, and context behind the event**

That makes these indices extremely important for:

* investigation context
* root cause analysis
* pipeline validation
* threat hunting
* detection tuning
* inventory-based analysis
* baseline understanding
* troubleshooting data gaps

This project focused on learning why these indices exist, why they are often ignored, and why they should actually be used much more by SOC analysts, defenders, and detection engineers.

---

## 🎯 Project Objective

The objective of this exploration was to understand the **practical value of Wazuh Discover index patterns beyond `wazuh-alerts-*`** and document how they support stronger security operations.

This exploration was performed to:

* understand the purpose of Wazuh’s additional indices
* learn what each index family stores
* explore why these indices are often ignored in SOC workflows
* understand how they support deeper investigation and operational visibility
* identify how they help with root cause analysis, threat hunting, and telemetry validation
* document their value from a practical analyst and engineering perspective

---

## 🛡️ Why This Exploration Matters

A SOC that only looks at alerts is often seeing only the **final visible symptom** of a much larger story.

The full story may include:

* whether the agent was healthy
* whether the telemetry pipeline was dropping events
* what packages were installed on the endpoint
* what processes were running
* what services existed
* what ports were open
* what the endpoint state looked like at that point in time
* whether archived raw logs contained clues that did not trigger rules

This means that if analysts ignore other indices, they may miss:

* the reason an alert happened
* the reason an alert did **not** happen
* host baseline context
* evidence for threat hunting
* pipeline health issues
* endpoint inventory details
* missed detections or false negatives

This is why exploring these indices matters.

---

## ❗ Why These Indices Are Often Ignored

These index families are often ignored because:

* most analysts live inside alert views
* alerts are easier to act on immediately
* inventory/state data feels less urgent
* monitoring/statistics data looks operational rather than security-focused
* raw archives can be large and noisy
* many teams are never trained to use them in investigations

Another reason is simple workflow bias:

* alerts give conclusions
* these other indices give context

And in busy SOC operations, people often prioritize conclusions first.

But context is exactly what makes investigations stronger.

---

## 💡 Why These Indices Should Not Be Ignored

These indices should not be ignored because they help answer high-value questions such as:

* Was the agent online and reporting during the incident window?
* Did the pipeline drop any events?
* Was there host inventory evidence that explains the alert?
* What packages, processes, ports, or services existed on the endpoint?
* Did raw logs contain evidence that rules missed?
* Was this alert caused by host state, pipeline issues, or actual malicious activity?

That means these indices are extremely useful for:

* SOC investigations
* threat hunting
* root cause analysis
* telemetry validation
* alert gap analysis
* inventory-led security review
* host baseline comparison
* detection engineering feedback

---

## 🧠 The Most Important Learning from This Exploration

One of the strongest takeaways from this project was this:

> **Alerts tell you that something happened.
> State, archive, monitoring, and statistics indices help explain why it happened — or why you may have missed it.**

That is a very important mindset shift.

If someone is building:

* detections
* anomaly models
* root cause workflows
* investigation playbooks
* telemetry validation checks
* hunting logic

then these indices are not optional — they are foundational.

---

## 🏗️ Role of Discover Indices in the Wazuh SOC Ecosystem

These index families sit behind and around the normal alert-driven Wazuh workflow.

They complement:

* alert monitoring
* threat hunting
* IT hygiene visibility
* vulnerability visibility
* detection engineering
* compliance visibility
* incident response workflows

Instead of replacing alerts, they make analysts better at understanding:

* agent health
* data availability
* raw event coverage
* endpoint state
* inventory posture
* system-level evidence
* why something may or may not have been detected

---

## 🔍 Main Index Families Explored

During this exploration, I focused on the most important non-default index families that analysts often overlook.

---

## 1. 🚨 `wazuh-alerts-*`

This is the primary security incident index pattern used in daily SOC work.

It stores:

* alerts generated by Wazuh
* rule matches
* decoded and enriched security events that triggered rules

### Why it matters

This is the main incident-facing view.

### Why it is not enough alone

It shows the detection outcome, but not always the full operational, inventory, or raw-data context behind the event.

---

## 2. 📦 `wazuh-archives-*`

This is one of the most powerful and often ignored index families.

It stores:

* raw logs
* events that may not have triggered alerts
* broader event history beyond rule-triggered detections

### Why it matters

Archives help analysts investigate activity that never triggered rules.

### Strong use cases

* deep forensics
* false-negative checking
* rule tuning
* compliance-related log retention
* searching pre-alert activity
* investigating attacker probing that stayed below alert thresholds

### Why it is often ignored

Because it can be large, noisy, and is not as immediately actionable as alerts.

### Why it should be used more

Because it provides visibility into what the SIEM received, not only what it alerted on.

---

## 3. 🩺 `wazuh-monitoring-*`

This index tracks Wazuh agent and monitoring health over time.

It stores visibility such as:

* agent availability
* connection state
* version information
* status data
* keepalive information
* manager relationship context

### Why it matters

This index helps answer whether an endpoint was:

* online
* connected
* synced
* properly reporting
* available during an incident window

### Strong use cases

* agent availability history
* confirming endpoint reporting during a security event
* verifying telemetry continuity
* troubleshooting disconnect patterns
* validating monitoring coverage

### Why it is often ignored

Because many analysts focus on threats, not telemetry-health visibility.

### Why it should be used more

Because an investigation is weaker if you do not know whether the endpoint was actually reporting correctly.

---

## 4. 📊 `wazuh-statistics-*`

This index records performance and operational metrics of the Wazuh server and pipeline itself.

It can include metrics related to:

* events received
* events processed
* events dropped
* alerts written
* queues
* internal service behavior
* ingestion and processing pressure

### Why it matters

This index helps analysts and engineers understand whether the security pipeline is healthy.

### Strong use cases

* identifying event drops
* pipeline troubleshooting
* performance tuning
* capacity planning
* validating ingestion pressure
* explaining missing detections caused by system stress

### Why it is often ignored

Because many analysts do not initially think of pipeline health as part of security visibility.

### Why it should be used more

Because dropped events or stressed queues can create dangerous blind spots.

---

## 5. 🧩 `wazuh-states-*` / `wazuh-states-inventory-*`

These indices store current or point-in-time endpoint state and inventory data rather than only event streams.

Examples include data related to:

* vulnerabilities
* hardware
* interfaces
* networks
* packages
* ports
* processes
* protocols
* system details
* services
* users
* groups
* browser extensions
* Windows hotfixes

### Why they matter

These indices help analysts see what the endpoint **looked like**, not just what event occurred.

### Strong use cases

* current risk posture visibility
* asset and software inventory analysis
* open-port validation
* process review
* service review
* package-based hunting
* endpoint baseline definition
* root cause enrichment

### Why they are often ignored

Because many teams consume this data through modules and dashboards rather than in raw Discover views.

### Why they should be used more

Because raw Discover exploration gives deeper flexibility for custom investigations and targeted searches.

---

## 🔬 What I Practically Explored

In this hands-on exploration, I examined how different Discover indices provide different perspectives.

I explored:

* agent status history in `wazuh-monitoring-*`
* internal pipeline and metrics visibility in `wazuh-statistics-*`
* inventory and current endpoint state through `wazuh-states-inventory-*`
* installed package visibility in `wazuh-states-inventory-packages-*`
* network port visibility in `wazuh-states-inventory-ports-*`
* process visibility in `wazuh-states-inventory-processes-*`
* services visibility in `wazuh-states-inventory-services-*`

This showed me that different index families answer very different analyst questions.

---

## 🚀 SOC Use Cases of These Discover Indices

These indices support strong SOC and security engineering use cases.

### 🔹 Root Cause Analysis

Understand what system state or operational context made an alert possible.

### 🔹 Threat Hunting

Look for host state, packages, processes, ports, and services that support deeper investigation.

### 🔹 Pipeline Validation

Check whether events were dropped, delayed, or impacted by performance issues.

### 🔹 Agent Health Review

Confirm whether a host was online and sending data during a given period.

### 🔹 Detection Engineering

Use raw and contextual data to improve rule logic and validate coverage.

### 🔹 False Negative Investigation

Use archives or inventory/state data to find evidence not captured in alerts.

### 🔹 Endpoint Baseline Review

Use inventory/process/service data to define what is normal on a system.

### 🔹 Incident Evidence Enrichment

Support investigations with telemetry outside standard alert data.

---

## 📈 Benefits of Exploring These Indices

The practical benefits include:

* better investigation context
* stronger root cause analysis
* better pipeline awareness
* improved false-negative checking
* stronger host-state understanding
* better inventory-led investigation
* more confidence in telemetry health
* better detection validation
* reduced blind spots
* stronger SOC maturity

---

## 🌍 Real-World Relevance

In real SOC environments, analysts often need to ask questions like:

* Was this agent online at the time?
* Did the pipeline drop events?
* Was this software already installed before the alert?
* Which service or process created this exposure?
* Was this port listening before the incident?
* Did raw logs contain clues before the alert fired?
* Are we missing detections because of telemetry gaps?

These are real-world investigation questions.

That is why these indices are valuable not only for:

* SOC analysts
* threat hunters
* incident responders

but also for:

* detection engineers
* platform engineers
* security engineers
* telemetry owners

---

## 📚 Why Wazuh Index Diversity Matters

Wazuh uses different index patterns because not all security data serve the same purpose. The official Wazuh indexer index documentation explains that Wazuh stores alerts, archives, monitoring information, statistics, vulnerability data, and many inventory/state datasets using distinct index patterns. This separation makes it possible to investigate incidents, review endpoint state, check infrastructure health, and query specialized datasets more effectively. ([documentation.wazuh.com](https://documentation.wazuh.com/current/user-manual/wazuh-indexer/wazuh-indexer-indices.html))

That means index diversity is not clutter.

It is **capability**.

---

## 🖼️ Knowledge / Learning Reference Placeholders

### Discover Index Concept Reference 1

> **Place concept/knowledge image here**

```text
[IMAGE PLACEHOLDER: discover-indices-knowledge-01]
Suggested file name: images/discover-indices-knowledge-01.png
```

Use this section to reinforce the idea that alerts are only one part of the Wazuh data ecosystem and that monitoring, statistics, archives, and state indices all serve different investigation purposes.

---

### Discover Index Concept Reference 2

> **Place concept/knowledge image here**

```text id="4jx6od"
[IMAGE PLACEHOLDER: discover-indices-knowledge-02]
Suggested file name: images/discover-indices-knowledge-02.png
```

Use this section to explain the role of archives, monitoring, statistics, and state indices, including why they are often ignored and why they are still valuable.

---

### Discover Index Concept Reference 3

> **Place concept/knowledge image here**

```text id="ynv6db"
[IMAGE PLACEHOLDER: discover-indices-knowledge-03]
Suggested file name: images/discover-indices-knowledge-03.png
```

Use this section to show practical use cases for statistics, monitoring, and state/inventory indices in operations, troubleshooting, and investigation.

---

### Discover Index Concept Reference 4

> **Place concept/knowledge image here**

```text id="jlwmj0"
[IMAGE PLACEHOLDER: discover-indices-knowledge-04]
Suggested file name: images/discover-indices-knowledge-04.png
```

Use this section to summarize index patterns and their best-use scenarios in a simple analyst-friendly way.

---

### Discover Index Concept Reference 5

> **Place concept/knowledge image here**

```text id="2dtt55"
[IMAGE PLACEHOLDER: discover-indices-knowledge-05]
Suggested file name: images/discover-indices-knowledge-05.png
```

Use this section to support understanding of the official Wazuh index pattern naming scheme and what each family stores.

---

### Discover Index Concept Reference 6

> **Place concept/knowledge image here**

```text id="575e7f"
[IMAGE PLACEHOLDER: discover-indices-knowledge-06]
Suggested file name: images/discover-indices-knowledge-06.png
```

Use this section to explain that custom index patterns can also be created, which helps analysts and engineers extend visibility beyond defaults when needed.

---

## 🖼️ Practical Exploration Screenshots

### `wazuh-monitoring-*` Exploration

> **Place monitoring index screenshot here**

```text id="k2vk4v"
[IMAGE PLACEHOLDER: discover-monitoring-index]
Suggested file name: images/discover-monitoring-index.png
```

This exploration shows agent-health and telemetry status visibility such as:

* OS version
* agent version
* manager relationship
* sync state
* keepalive timing
* reporting continuity

This is useful for validating whether a monitored endpoint was actually healthy and connected during a security event.

---

### `wazuh-statistics-*` Exploration

> **Place statistics index screenshot here**

```text id="2f0vpi"
[IMAGE PLACEHOLDER: discover-statistics-index]
Suggested file name: images/discover-statistics-index.png
```

This view shows internal Wazuh processing metrics such as:

* total events decoded
* events processed
* events received
* events dropped
* alerts written
* queue and subsystem metrics

This is important for identifying ingestion issues, pipeline health problems, and detection blind spots caused by system stress.

---

### `wazuh-states-inventory-*` Exploration

> **Place states inventory overview screenshot here**

```text id="sm0elq"
[IMAGE PLACEHOLDER: discover-states-inventory-overview]
Suggested file name: images/discover-states-inventory-overview.png
```

This view demonstrates point-in-time endpoint state data, including:

* hardware context
* memory usage
* interface state
* network details
* inventory-related fields

This is useful for understanding host baseline and contextual system state during investigations.

---

### `wazuh-states-inventory-packages-*` Exploration

> **Place packages index screenshot here**

```text id="9z9bf8"
[IMAGE PLACEHOLDER: discover-states-packages-index]
Suggested file name: images/discover-states-packages-index.png
```

This view is useful for investigating:

* package names
* versions
* architecture
* vendor details
* package sizes
* installed software inventory

This helps with software review, inventory-based hunting, and validating whether risky or unusual packages exist on an endpoint.

---

### `wazuh-states-inventory-ports-*` Exploration

> **Place ports index screenshot here**

```text id="7286uk"
[IMAGE PLACEHOLDER: discover-states-ports-index]
Suggested file name: images/discover-states-ports-index.png
```

This view helps analysts inspect:

* destination IPs
* destination ports
* transport protocols
* process names
* PIDs
* listening state

This is important for identifying exposed services, confirming port state, and reviewing network-facing attack surface.

---

### `wazuh-states-inventory-processes-*` Exploration

> **Place processes index screenshot here**

```text id="m0yv0b"
[IMAGE PLACEHOLDER: discover-states-processes-index]
Suggested file name: images/discover-states-processes-index.png
```

This view provides visibility into:

* process names
* command lines
* parent PIDs
* process start times
* process IDs

This is valuable for investigations, threat hunting, persistence review, and host baseline analysis.

---

### `wazuh-states-inventory-services-*` Exploration

> **Place services index screenshot here**

```text id="xccs0m"
[IMAGE PLACEHOLDER: discover-states-services-index]
Suggested file name: images/discover-states-services-index.png
```

This section is useful for reviewing:

* service names
* service state
* start type
* service description
* process executable context
* enabled/disabled state

This helps analysts identify persistence-relevant service behavior and understand endpoint service posture.

---

## 🧪 What I Learned

Through this exploration, I learned that Wazuh Discover is much more powerful when analysts move beyond only `wazuh-alerts-*`.

I strengthened my understanding of:

* why index families exist
* how different indices support different investigation goals
* how monitoring and statistics indices improve telemetry confidence
* how state and inventory indices improve host context
* how raw and supporting indices help explain alerts and missed detections
* why these “ignored” indices are actually essential for mature SOC operations

---

## 🔗 Further Reading & Official References

For official documentation and index reference details, review the [Wazuh index patterns / indices documentation](https://documentation.wazuh.com/current/user-manual/wazuh-indexer/wazuh-indexer-indices.html).

This reference is useful for understanding:

* official Wazuh index families
* what each index pattern stores
* how Wazuh separates alerts, archives, monitoring, statistics, and state/inventory data
* how index patterns support different investigation and operational workflows

---

## 🧾 Conclusion

This project documents my practical exploration of the **different Wazuh Discover indices / index patterns** that many analysts often ignore.

The exploration showed that these indices are not background clutter.

They are important visibility layers for:

* monitoring health
* pipeline health
* archive searching
* endpoint inventory
* process context
* package visibility
* port and service analysis
* root cause analysis
* hunting and validation

That means analysts should not treat Discover as a place for alerts only.

Used properly, these index families make Wazuh much more powerful for investigations, telemetry assurance, host-state analysis, and mature security operations.

---
