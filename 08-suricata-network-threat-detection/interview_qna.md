# 🎯 Suricata + Wazuh SOC Project  
## Interview Questions & Answers

> This document covers technical and scenario-based interview questions based on this project.

---

# 🔹 SECTION 1 — Architecture & Design

---

### 1️⃣ Can you explain the architecture of your Suricata + Wazuh integration?

Yes.

The architecture consists of:

- Kali Linux (attack simulation)
- Ubuntu endpoint running Suricata IDS + Wazuh Agent
- Wazuh Manager (decoding, rule engine, correlation)
- OpenSearch (alert indexing)
- Wazuh Dashboard (visualization)
- TheHive (incident response)

Data flow:

Attack → Suricata detects → eve.json → Wazuh Agent → Wazuh Manager → OpenSearch → Dashboard → TheHive.

This ensures network-layer detection is centralized and enriched for SOC use.

---

### 2️⃣ Why integrate Suricata with Wazuh instead of using Suricata alone?

Suricata alone provides detection but lacks:

- Centralized correlation
- MITRE ATT&CK mapping
- Structured alert enrichment
- Dashboard analytics
- Case management integration

Wazuh provides:

- JSON decoding
- Rule correlation
- Alert normalization
- MITRE enrichment
- SOC dashboarding
- IR workflow integration

Together they provide defense-in-depth.

---

### 3️⃣ What problem does this project solve in a SOC?

It solves:

- Alert noise
- Lack of structured field extraction
- Limited detection context
- Mixed endpoint + network telemetry
- Slow triage

It transforms raw alerts into structured, enriched, SOC-ready intelligence.

---

# 🔹 SECTION 2 — Suricata

---

### 4️⃣ What is Suricata?

Suricata is an open-source Network Intrusion Detection System (NIDS) capable of:

- Deep packet inspection
- Protocol parsing (HTTP, DNS, TLS)
- Signature-based detection
- JSON logging (EVE format)

It analyzes live traffic and matches it against detection rules.

---

### 5️⃣ What is eve.json?

`eve.json` is Suricata’s structured JSON log output.

It contains:

- Source IP
- Destination IP
- Ports
- Protocol
- Signature
- Severity
- HTTP/DNS/TLS metadata

This structured format allows SIEM tools to parse logs efficiently.

---

### 6️⃣ How did you validate Suricata detection?

I simulated attacks using Kali Linux:

- Nmap SYN scans
- Vulnerability scans
- Service-specific port scans

Then validated:

- Suricata logged events in eve.json
- Wazuh parsed them correctly
- Custom rules triggered
- MITRE mapping appeared in dashboard

---

# 🔹 SECTION 3 — Detection Engineering

---

### 7️⃣ Why did you create custom decoders?

Default parsing buried important fields inside `full_log`.

Custom decoders allowed:

- Clean field extraction (src_ip, dst_ip, signature)
- Structured rule matching
- Better dashboard filtering
- Cleaner alert correlation

This improves detection quality.

---

### 8️⃣ What is detection engineering?

Detection engineering is the process of:

- Building structured detection logic
- Reducing false positives
- Improving signal-to-noise ratio
- Mapping alerts to threat frameworks (MITRE)
- Continuously validating detections

It goes beyond tool installation.

---

### 9️⃣ How did you reduce alert noise?

I implemented:

- Suppression rules for low-value alerts
- Severity normalization rules
- High-confidence rule grouping
- Context-based filtering

Noise reduction was done without losing telemetry visibility.

---

### 🔟 Why is noise reduction important?

Because:

- Alert fatigue reduces analyst effectiveness
- Too many false positives delay real incident detection
- SOC efficiency depends on signal clarity

Noise reduction improves triage speed.

---

# 🔹 SECTION 4 — MITRE ATT&CK

---

### 1️⃣1️⃣ Why did you map detections to MITRE ATT&CK?

MITRE mapping provides:

- Threat context
- Attack lifecycle visibility
- Standardized detection classification
- Easier reporting

Example:
Nmap detection → T1595 (Active Scanning) → Reconnaissance tactic.

---

### 1️⃣2️⃣ What is T1595?

T1595 is MITRE ATT&CK technique for:

Active Scanning under Reconnaissance.

It includes:

- Port scanning
- Service enumeration
- Vulnerability scanning

---

# 🔹 SECTION 5 — Wazuh

---

### 1️⃣3️⃣ What is the role of Wazuh Manager?

Wazuh Manager:

- Decodes JSON logs
- Applies custom rules
- Performs correlation
- Generates alerts
- Adds MITRE enrichment
- Indexes alerts into OpenSearch

It is the detection brain of the system.

---

### 1️⃣4️⃣ Why use agent groups?

Agent groups allow:

- Centralized configuration
- Policy-based deployment
- Separation of network vs endpoint telemetry
- Scalability

This reflects production SOC design.

---

# 🔹 SECTION 6 — Dashboard & SOC Workflow

---

### 1️⃣5️⃣ Why create a dedicated Suricata dashboard?

Because:

- Mixing host + network alerts reduces clarity
- SOC analysts need focused views
- Network threats require specific triage workflow

The dashboard included:

- Top signatures
- MITRE tactic distribution
- Alert trends
- Top attacking IPs
- Severity breakdown

---

### 1️⃣6️⃣ How does this improve triage speed?

Analysts can:

1. See attack spikes immediately
2. Identify dominant signatures
3. View MITRE tactic
4. Identify top attacking IP
5. Escalate quickly

Detection → Visualization → Investigation → Response

---

# 🔹 SECTION 7 — Scenario-Based Questions

---

### 1️⃣7️⃣ An alert spike appears at 02:30 AM. What do you do?

1. Open Suricata dashboard
2. Check alert trend panel
3. Identify signature causing spike
4. Check source IP
5. Verify MITRE tactic
6. Drill down in Discover
7. Escalate to TheHive if malicious

---

### 1️⃣8️⃣ How would you scale this architecture?

- Deploy multiple Suricata sensors
- Add them to Suricata agent group
- Centralized rule management
- Use load-balanced Wazuh cluster
- Add automated response scripts

---

### 1️⃣9️⃣ What makes this project different from a basic lab?

It includes:

- Custom decoder engineering
- Noise reduction strategy
- MITRE enrichment
- High-confidence detection rules
- SOC dashboard optimization
- IR platform integration
- Agent group scalability

It reflects real-world SOC engineering.

---

# 🔹 SECTION 8 — Key Takeaways

---

This project demonstrates:

- Network-layer detection
- SIEM integration
- Detection engineering
- Noise reduction
- MITRE alignment
- SOC workflow optimization
- Production-style architecture thinking

---

# 🏁 Final Interview Summary

If asked to summarize this project in one sentence:

“I implemented a full network detection engineering pipeline by integrating Suricata IDS with Wazuh SIEM, reducing alert noise, enriching detections with MITRE ATT&CK mapping, and building a SOC-ready dashboard and workflow for faster triage.”
