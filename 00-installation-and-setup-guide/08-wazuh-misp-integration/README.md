# 🔐 Wazuh ↔ MISP Integration

## Real-Time Threat Intelligence Driven Malware Detection

<div align="center">

<img src="https://www.misp-project.org/img/blog/misp-wazuh.png" width="750"/>

</div>

---

## 🧠 What Is This Integration?

This project integrates:

* **Wazuh (SIEM / XDR Platform)**
* **MISP (Threat Intelligence Platform)**

The goal:

> Automatically correlate file hashes detected by Wazuh with threat intelligence stored in MISP.

When a file is created on a monitored endpoint:

1. Wazuh detects the file via File Integrity Monitoring (FIM)
2. Hashes (MD5, SHA1, SHA256) are extracted
3. Custom integration script queries MISP
4. If match is found → enriched alert generated
5. High-confidence malware detection achieved

---

# 📁 Repository Structure

```
08-wazuh-misp-integration/
│
├── README.md
├── commands.sh
├── architecture-notes.txt
├── troubleshooting.md
├── interview_qna.md
│
├── scripts/
│   └── custom-misp-file-hashes.py
│
└── rules/
    └── misp_file_hashes.xml
```

---

# 🎯 Why Integrate Wazuh with MISP?

Without MISP:

* Wazuh detects file creation
* No global intelligence context
* Higher false positives
* Manual investigation required

With MISP:

* File hashes checked against global threat feeds
* Only known malicious hashes trigger high-severity alerts
* Threat context automatically attached
* SOC confidence increases dramatically

---

# 📊 SOC Use Case

### Scenario

- 1️⃣ Malware dropped in `/tmp`
- 2️⃣ Wazuh detects file creation
- 3️⃣ Hash extracted
- 4️⃣ MISP queried via REST API
- 5️⃣ Match found in global intelligence feed
- 6️⃣ Rule 100802 triggered (Hash Match)
- 7️⃣ High-confidence detection created
- 8️⃣ Forwarded to TheHive for case triage

---

# 🏗 Architecture Overview

Integration Flow:

```
Wazuh Agent
↓
Wazuh Manager (Syscheck Event ID 554)
↓
Custom MISP Integration Script
↓
MISP REST API
↓
Enriched Detection in Wazuh
```

Threat intelligence feeds into MISP from:

* MalwareBazaar
* CIRCL OSINT
* BOTVRIJ.EU
* Community intelligence

---

# 📚 Official References & Technical Foundations

This implementation aligns with official guidance and reference material published by the MISP Project.
The following authoritative resources were used during architecture design and validation:

---

### 🔹 MISP Official Blog – Wazuh Integration Architecture

[Official technical article published by the MISP Project detailing the Wazuh integration workflow, API interaction model, and architectural considerations](https://www.misp-project.org/2025/10/06/wazuh-integration.html/)

This article explains:

* How Wazuh queries MISP using the REST API
* Expected integration flow
* Security considerations
* Real-world deployment guidance

---

### 🔹 MISP GitHub – Official Wazuh Integration Repository

[Official MISP-maintained integration scripts and reference implementation hosted on GitHub](https://github.com/MISP/wazuh-integration)

This repository provides:

* Reference Python integration scripts
* Example configurations
* Rule definitions
* Production-grade implementation patterns

---

## 📌 Why These References Matter

Using official MISP resources ensures:

* Architectural correctness
* API compatibility
* Alignment with supported deployment models
* Security best practices
* Enterprise-ready implementation

This project adapts the official model into a real-world AWS SOC lab deployment with structured rule engineering and alert refinement.

---

# 🖥 Environment Used

| Component        | Deployment            |
| ---------------- | --------------------- |
| Wazuh Manager    | AWS EC2               |
| Wazuh Agent      | Ubuntu + Windows      |
| MISP             | AWS EC2               |
| Integration      | Custom Python Script  |
| Detection Method | File Hash Correlation |

---

# ⚙️ Step 1 – Integration Script

## 📍 Script Location in Repository

You can directly download the integration script from:

👉 **Script (Repository Link)**
[Click here.](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/00-installation-and-setup-guide/08-wazuh-misp-integration/scripts/custom-misp-file-hashes.py)

---

## 📍 Script Path on Wazuh Manager

```
/var/ossec/integrations/custom-misp-file-hashes.py
```

Create the script:

```bash
cd /var/ossec/integrations/
nano custom-misp-file-hashes.py
```

Paste the script from the repository link above.

---

## 🔐 Set Permissions

```bash
chmod 750 /var/ossec/integrations/custom-misp-file-hashes.py
chown root:wazuh /var/ossec/integrations/custom-misp-file-hashes.py
```

---

# ⚙️ Step 2 – Configure Directory Monitoring (FIM)

## 🔹 Linux Agent

File:

```
/var/ossec/etc/ossec.conf
```

Add:

```xml
<directories check_all="yes" realtime="yes">/tmp</directories>
<directories check_all="yes" realtime="yes">/usr/bin</directories>
<directories check_all="yes" realtime="yes">/usr/local/bin</directories>
```

Restart agent:

```bash
systemctl restart wazuh-agent
```

---

## 🔹 Windows Agent

Add:

```xml
<directories check_all="yes" realtime="yes">C:\Users</directories>
<directories check_all="yes" realtime="yes">C:\Windows\Temp</directories>
<directories check_all="yes" realtime="yes">C:\ProgramData</directories>
```

Restart service:

```powershell
Restart-Service wazuh
```

---

# ⚙️ Step 3 – Wazuh Manager Integration Block

Edit:

```
/var/ossec/etc/ossec.conf
```

```xml
<integration>
  <name>custom-misp-file-hashes.py</name>
  <hook_url>https://YOUR_MISP_IP</hook_url>
  <api_key>YOUR_MISP_AUTHKEY</api_key>
  <group>syscheck</group>
  <rule_id>554</rule_id>
  <alert_format>json</alert_format>
</integration>
```

Validate before restart:

```bash
/var/ossec/bin/wazuh-analysisd -t
```

Restart:

```bash
systemctl restart wazuh-manager
```

---

# ⚙️ Step 4 – Create Custom Rules

## 📍 Rules File in Repository

👉 **Rules File (Repository Link)**
[Click here.](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/00-installation-and-setup-guide/08-wazuh-misp-integration/rules/misp_file_hashes.xml)

---

## 📍 Path on Wazuh Manager

```
/var/ossec/etc/rules/misp_file_hashes.xml
```

Create file:

```bash
cd /var/ossec/etc/rules/
nano misp_file_hashes.xml
```

Paste content from repository link above.

Validate:

```bash
/var/ossec/bin/wazuh-analysisd -t
```

Restart:

```bash
systemctl restart wazuh-manager
```

---

# 🧪 Step 5 – End-to-End Testing (EICAR)

### Add Hash to MISP

MD5:

```
44d88612fea8a8f36de82e1278abb02f
```

---

### Download Test File (Linux)

```bash
curl -Lo /tmp/eicar.exe https://secure.eicar.org/eicar.com
```

---

### Expected Result in Wazuh UI

You should see:

* Rule 554 (File creation)
* Rule 100800 (MISP integration)
* Rule 100802 (Hash match – Level 12)

This confirms:

- ✔ Script working
- ✔ API authentication valid
- ✔ Hash correlation successful
- ✔ Detection pipeline active

---

# 📈 Benefits of This Integration

### 1️⃣ Intelligence-Driven Detection

Alerts are backed by global threat intelligence.

### 2️⃣ Reduced False Positives

Only confirmed malicious hashes escalate.

### 3️⃣ Faster Investigation

SOC analysts receive enriched metadata:

* MISP Event UUID
* Attribute UUID
* Direct permalink
* IOC type

### 4️⃣ Clean Alert Pipeline

High-confidence alerts only.

### 5️⃣ Production-Ready SOC Design

Mirrors real enterprise SOC architectures.

---

# 🔐 Security Considerations

* Use dedicated MISP integration user
* Restrict API key by IP
* Rotate API keys periodically
* Use HTTPS (avoid self-signed certs in production)
* Monitor integrations.log

---

# 📊 SOC Impact

Before Integration:

* File creation alerts noisy
* Manual hash lookups
* Slow investigation
* Lower SOC confidence

After Integration:

* Automated hash reputation lookup
* Immediate malicious classification
* Reduced triage time
* High-confidence malware detection
* Intelligence feedback loop

---

# 🧩 SOC-SOAR Ecosystem Impact

You now have:

Wazuh → MISP → TheHive

Detection → Intelligence Correlation → Incident Response

This forms a complete SOC pipeline:

* Detection Layer (Wazuh)
* Intelligence Layer (MISP)
* Response Layer (TheHive)

---

## 📎 PDF Guide

For the full step-by-step PDF with screenshots and validation, see:

📄 **[Auditd + Wazuh kernal monitoring, auditing PDF Guide](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/tree/main/18-auditd-wazuh-credential-access-hunting/docs)**

---

# 🚀 Conclusion

This integration transforms Wazuh from a log monitoring platform into an:

> Intelligence-Aware Detection Engine.

Instead of detecting every file event blindly,
Wazuh now detects threats validated by global intelligence feeds.

This dramatically improves:

* MTTR
* SOC analyst confidence
* Detection quality
* Incident response efficiency

It represents a real-world SOC-grade deployment model used in modern security operations centers.

---
