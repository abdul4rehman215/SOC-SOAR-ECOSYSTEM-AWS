# 🛡️ Wazuh + VirusTotal Integration

## Real-Time Malware Detection & Automated Threat Removal (SOC Automation Project)

<p align="center">
  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/wazuh-virustotal.png" width="450"/>
</p>

---

## 🚀 Project Overview

Modern SOC environments require more than simple detection.

They require:

* Real-time file monitoring
* Threat intelligence enrichment
* Contextual alerting
* Noise reduction
* Automated containment
* IR platform visibility

File Integrity Monitoring (FIM) alone detects file changes —
but it **does not determine malicious intent**.

This project integrates:

* **Wazuh (SIEM/XDR)**
* **VirusTotal (Threat Intelligence Enrichment)**
* **Wazuh Active Response (Automated Remediation)**
* **TheHive (Incident Response Platform)**

To build a complete:

> Detect → Enrich → Confirm → Automatically Remove → Notify → Investigate

SOC-grade malware detection and automated containment pipeline.

---

# 🧠 Why This Project Matters

In real-world SOC operations:

* Analysts cannot manually verify every file
* Malware executes in seconds
* Public API limits require intelligent rule tuning
* False positives create fatigue
* Detection without response is incomplete

This project demonstrates:

* Detection engineering
* API-based enrichment
* Noise control
* MITRE mapping
* Automated response
* SOC workflow integration
* IR tool visibility

This is not just integration —
this is **SOC ecosystem engineering.**

---

# 🧩 Project Structure

This project contains two merged phases:

---

## 🔹 PART 1

### Real-Time Malware Detection & Threat Enrichment

* FIM monitoring (Linux + Windows)
* Executable filtering
* VirusTotal API enrichment
* Custom rule tuning
* Noise suppression
* MITRE ATT&CK mapping
* Wazuh dashboard visibility
* TheHive case forwarding

---

## 🔹 PART 2

### Automated Malware Removal Using Wazuh Active Response

* Trigger response only for confirmed malware
* Execute removal script automatically
* Log confirmation alerts
* Maintain audit trail
* Preserve SOC visibility
* Zero manual containment

---

# 🧬 Architecture Overview (Part 1)

<p align="center">
  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/wazuh-virustotal-flow-diagram.png"/>
</p>


### Detection Pipeline

```
Endpoint (Ubuntu / Windows)
        ↓
Wazuh Agent (FIM realtime monitoring)
        ↓
Wazuh Manager
        ↓
Custom executable rules
        ↓
VirusTotal API lookup
        ↓
Enriched alert + MITRE mapping
        ↓
Wazuh Dashboard + TheHive
```

---

# 🧬 Architecture Overview (Part 2 – With Active Response)

<p align="center">
  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/wazuh-virustotal-architect.png"/>
</p>

```
Malicious file created
        ↓
FIM detects change
        ↓
VirusTotal confirms malware
        ↓
Rule 87105 triggered
        ↓
Active Response executes
        ↓
remove-threat.sh runs on endpoint
        ↓
File deleted automatically
        ↓
Removal confirmation alert
        ↓
Visible in Dashboard + TheHive
```

---

# 🦠 What is VirusTotal?

VirusTotal is a Google-owned multi-engine malware analysis platform that scans:

* Files
* URLs
* Domains
* IP addresses

Using 70+ antivirus engines and threat intelligence feeds.

In this project, we use the **VirusTotal Public API** to enrich file hashes detected by Wazuh.

### Public API Limits

* 4 requests per minute
* 500 requests per day

Because of this, we engineered:

* Executable-only triggering
* Clean-result suppression
* High-confidence escalation logic

Official documentation reference:

👉 **[Official Wazuh VirusTotal Integration Guide](https://documentation.wazuh.com/current/user-manual/capabilities/malware-detection/virus-total-integration.html)**

👉 **[Wazuh Malware Detection Blog (Emotet Case Study)](https://wazuh.com/blog/emotet-malware-detection/)**

---

# 🔐 VirusTotal Account Setup

1. Navigate to VirusTotal website
2. Create a free account
3. Go to Profile → API Key
4. Copy your public API key

This API key will be added to Wazuh Manager configuration.

---

# ⚙️ PART 1 — Implementation Guide

---

## 1️⃣ Enable VirusTotal Integration on Wazuh Manager

Edit:

```
/var/ossec/etc/ossec.conf
```

Add inside `<ossec_config>`:

```xml
<integration>
  <name>virustotal</name>
  <api_key>YOUR_API_KEY_HERE</api_key>
  <rule_id>100027,100028</rule_id>
  <alert_format>json</alert_format>
</integration>
```

### Why rule_id matters?

It ensures:

* Only executable files trigger API lookups
* API usage remains controlled
* Public rate limits are respected

Restart:

```bash
sudo systemctl restart wazuh-manager
```

---

## 2️⃣ Custom Rules – Noise Control & High Confidence Escalation

Edit:

```
/var/ossec/etc/rules/local_rules.xml
```

Add:

```xml
<group name="syscheck,malware,virustotal">

  <!-- New executable -->
  <rule id="100027" level="12">
    <if_sid>550</if_sid>
    <match>\.(exe|elf|sh|py|js|ps1|bat)$</match>
    <description>Executable file added - allowed for VirusTotal scan</description>
  </rule>

  <!-- Modified executable -->
  <rule id="100028" level="12">
    <if_sid>554</if_sid>
    <match>\.(exe|elf|sh|py|js|ps1|bat)$</match>
    <description>Executable file modified - allowed for VirusTotal scan</description>
  </rule>

  <!-- Suppress clean -->
  <rule id="100029" level="0">
    <if_sid>87104</if_sid>
    <field name="data.virustotal.positives">^0$</field>
    <description>VirusTotal clean result - suppressed</description>
    <options>no_log</options>
  </rule>

  <!-- High confidence -->
  <rule id="100030" level="15">
    <if_sid>87105</if_sid>
    <field name="data.virustotal.positives">^[5-9]|[1-9][0-9]+$</field>
    <description>High confidence malware detected by VirusTotal</description>
    <mitre>T1059</mitre>
  </rule>

</group>
```

Restart manager.

---

## 3️⃣ Configure FIM on Ubuntu Agent

```
/var/ossec/etc/ossec.conf
```

```xml
<syscheck>
  <disabled>no</disabled>
  <directories check_all="yes" realtime="yes">/media/user/software</directories>
</syscheck>
```

Restart agent.

---

## 4️⃣ Configure FIM on Windows Agent

```
C:\Program Files (x86)\ossec-agent\ossec.conf
```

```xml
<directories realtime="yes">C:\Users\Public\Downloads</directories>
```

Restart Wazuh Agent service.

---

## 5️⃣ Malware Simulation Test

Download EICAR:

```bash
sudo curl -Lo /media/user/software/bad.exe https://secure.eicar.org/eicar.com
```

Expected chain:

* FIM detects
* Rule triggers
* VirusTotal lookup
* Alert enriched
* MITRE mapping added
* Dashboard alert visible
* Forwarded to TheHive

---

## 6️⃣ Dashboard Verification

Filter:

```
rule.groups: virustotal
```

Observe:

* File path
* MD5, SHA1, SHA256
* VirusTotal positives count
* Permalink
* MITRE mapping (T1059)
* Rule escalation level

---

## 7️⃣ TheHive Case Visibility

TheHive receives:

* Malware detection alert
* VirusTotal enrichment
* MITRE mapping
* File hash intelligence
* Description summary

SOC analyst can:

* Convert alert to case
* Assign investigator
* Track timeline

---

# ✅ PART 1 Outcomes

- ✔ Real-time executable detection
- ✔ VirusTotal enrichment
- ✔ Clean result suppression
- ✔ MITRE ATT&CK alignment
- ✔ Controlled API usage
- ✔ Reduced alert fatigue
- ✔ SOC-ready alerting

---

# ⚙️ PART 2 — Automated Malware Removal

Official reference used:

👉 **[Wazuh Active Response Malware Removal Guide](https://documentation.wazuh.com/current/proof-of-concept-guide/detect-remove-malware-virustotal.html)**

---

## 1️⃣ Active Response Configuration (Manager)

Edit:

```
/var/ossec/etc/ossec.conf
```

Add:

```xml
<command>
  <name>remove-threat</name>
  <executable>remove-threat.sh</executable>
  <timeout_allowed>no</timeout_allowed>
</command>

<active-response>
  <disabled>no</disabled>
  <command>remove-threat</command>
  <location>local</location>
  <rules_id>87105</rules_id>
</active-response>
```

Explanation:

* Only confirmed malicious files trigger response
* Execution happens on affected endpoint
* No manual intervention required

---

## 2️⃣ Custom Rules for Active Response Logging

```xml
<group name="virustotal,active_response">

  <rule id="100092" level="12">
    <if_sid>657</if_sid>
    <match>Successfully removed threat</match>
    <description>Active Response removed malware: $(parameters.alert.data.virustotal.source.file)</description>
  </rule>

  <rule id="100093" level="12">
    <if_sid>657</if_sid>
    <match>Error removing threat</match>
    <description>Active Response failed to remove malware: $(parameters.alert.data.virustotal.source.file)</description>
  </rule>

</group>
```

Restart manager.

---

## 3️⃣ Place Removal Script on Agent

Path:

```
/var/ossec/active-response/bin/remove-threat.sh
```

Script must:

* Parse JSON input
* Extract malicious file path
* Delete file
* Log result

Set permissions:

```bash
sudo chmod 750 /var/ossec/active-response/bin/remove-threat.sh
sudo chown root:wazuh /var/ossec/active-response/bin/remove-threat.sh
```

---

## 4️⃣ Malware Simulation (Automated Removal)

Download EICAR again.

Expected:

* File created
* VirusTotal confirms
* Rule 87105 fires
* Script executes
* File deleted
* Active response alert generated
* Dashboard + TheHive updated

---

## 5️⃣ Endpoint Verification

```
ls /media/user/software/bad.exe
```

Expected:

```
No such file or directory
```

Check:

```
cat /var/ossec/logs/active-responses.log
```

---

# 🎯 Final Automated Pipeline

```
File Created
↓
Wazuh Detects
↓
VirusTotal Enriches
↓
Confirmed Malicious
↓
Active Response Executes
↓
File Deleted
↓
Removal Logged
↓
SOC Notified
```

---

# 🏁 Final Project Outcomes

- ✔ Real-time malware detection
- ✔ Threat intelligence enrichment
- ✔ Noise control engineering
- ✔ MITRE ATT&CK mapping
- ✔ Automated containment
- ✔ SOC dashboard visibility
- ✔ IR platform case creation
- ✔ Zero manual removal required

---

# 🧠 Skills Demonstrated

* Wazuh SIEM engineering
* FIM tuning
* Threat intelligence integration
* Detection engineering
* Active response automation
* SOC workflow design
* MITRE ATT&CK alignment
* Endpoint security hardening
* IR tool integration

---

# 📂 Repository Structure

```
09-wazuh-virustotal-integration/
│
├── README.md
├── commands.sh
├── architecture-notes.txt
├── interview_qna.md
├── troubleshooting.md
│
├── scripts/
│   ├── virustotal
│   └── virustotal.py
|
├── manager/
│   ├── ossec.conf.snippet
│   └── local_rules.xml
│
├── agent/
│   ├── ubuntu_fim.conf
│   ├── windows_fim.conf
│   └── remove-threat.sh
│
└── resources/
    ├── Wazuh VirusTotal Integration Malware Detection Project.pdf
    └── Wazuh VirusTotal Active Response Automated Malware Removal.pdf
```

---

# 📎 Full PDF Guide

For full implementation screenshots and validation proof:

👉 **[Click here to view the complete PDF implementation guide Part 1](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/09-wazuh-virustotal-integration/docs/Wazuh%20VirusTotal%20Integration%20Malware%20Detection%20Project.pdf)**

👉 **[Click here to view the complete PDF implementation guide Part 2](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/09-wazuh-virustotal-integration/docs/Wazuhh%20VirusTotal%20Active%20Response%20Automated%20Malware%20Removal.pdf)**

---

# 🔐 Conclusion

This project demonstrates a production-ready SOC automation pipeline.

Instead of:

> Detect → Wait → Investigate → Manually Delete

We now have:

> Detect → Enrich → Confirm → Automatically Remove → Notify

This aligns with:

* Modern XDR strategy
* SOAR methodology
* Automated containment frameworks
* Enterprise SOC operations

---
