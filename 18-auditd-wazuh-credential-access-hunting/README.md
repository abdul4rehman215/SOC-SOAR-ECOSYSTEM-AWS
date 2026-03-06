# 🕵️ Hunting Linux Credential Access Attacks using **Auditd** + **Wazuh SIEM**

<p align="center">
  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/auditd-wazuh.png" alt="Auditd + Wazuh" width="520">
</p>

> In Linux investigations, the question is rarely “Did something happen?”  
> It’s **“Who did what, when, and to which sensitive resource?”**  
> This project adds **kernel-level visibility** to my AWS SOC ecosystem using **Auditd**, then operationalizes it inside **Wazuh** for **real-time alerting + threat hunting + compliance-ready logging**.

---

## 📌 Project Overview

This project demonstrates a **practical SOC workflow** for detecting and investigating Linux credential-access behaviors using:

- **Auditd** (Linux kernel audit framework) to capture **system-call + file access telemetry**
- **Wazuh** (SIEM/XDR) to ingest audit logs and generate **searchable security events**, **custom alerts**, and **SOC-ready investigation views**

### ✅ What this project detects (examples)

- Reading or modifying sensitive credential files:
  - `/etc/shadow`
  - `/etc/passwd`
- SSH key inspection / persistence signals:
  - `~/.ssh/authorized_keys`
- Shell history access / tampering:
  - `~/.bash_history`
- Suspicious command execution patterns (execve telemetry)

---

## 🎯 Objectives

By completing this project, I was able to:

- ✅ Deploy and validate **auditd** logging at kernel level  
- ✅ Build persistent **audit rules** for credential access + exec monitoring  
- ✅ Forward audit logs to **Wazuh Agent** (`audit.log`)  
- ✅ Implement **CDB lists** to classify audit keys and suspicious tools  
- ✅ Write **custom Wazuh rules** that turn raw audit telemetry into alerts  
- ✅ Simulate credential access behaviors and verify detections in Wazuh  
- ✅ Use **Threat Hunting** + **Discover** views for analyst investigations  

---

## 🧠 What is Auditd?

**Auditd** (Linux Audit Daemon) is the userspace component of the Linux Audit Framework that hooks into the kernel audit subsystem.  
It records **security-relevant events** such as:

- system calls like `execve`, `open`, `chmod`
- file access/permission changes for watched files
- attribution via **AUID** (original login user), even after `sudo`

This makes auditd excellent for:
- 🕵️ forensic investigations
- ✅ compliance logging
- 🚨 high-fidelity detections (low noise, strong context)

---

## 🤝 Why integrate Auditd with Wazuh?

Auditd logs are powerful but:
- stored locally
- not easy to correlate at scale
- hard to search without SIEM indexing

Wazuh adds:
- Centralized collection across endpoints
- Real-time alerting and correlation
- Threat hunting workflows
- Dashboards/Discover views
- MITRE mapping capability
- Active response potential (optional)

📌 Official references you can explore:
- 🔗 **SOC use case walkthrough:** [Hunting for Linux credential access attacks with Wazuh](https://wazuh.com/blog/hunting-for-linux-credential-access-attacks-with-wazuh/)
- 🔗 **Wazuh PoC:** [Audit commands run by user](https://documentation.wazuh.com/current/proof-of-concept-guide/audit-commands-run-by-user.html)
- 🔗 **Auditd configuration reference:** [System calls monitoring (audit configuration)](https://documentation.wazuh.com/current/user-manual/capabilities/system-calls-monitoring/audit-configuration.html)

---

## 🏗️ Architecture

<p align="center">
  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/Auditd%20and%20Wazuh%20in%20SOC%20ecosystem.png" alt="Auditd + Wazuh Architecture" width="850">
</p>

```text
Linux Endpoint (auditd enabled)
   |
   |  Kernel audit events -> /var/log/audit/audit.log
   |
Wazuh Agent (localfile audit collector)
   |
   |  forwards audit.log events
   |
Wazuh Manager (rules + decoders + CDB lists)
   |
   |  alerting + correlation + MITRE mapping
   |
Wazuh Dashboard (Threat Hunting / Discover)
   |
SOC Analyst (investigation + detection validation)
````

---

## 🧰 Tools & Technologies Used

* **Linux auditd** + `audispd-plugins`
* **Wazuh Agent**
* **Wazuh Manager**
* **Wazuh Dashboard (OpenSearch Dashboards)**
* Linux utilities: `auditctl`, `augenrules`, `ausearch`, `tail`, `grep`

---

## ✅ Prerequisites

Before running this project, you should have:

* Basic Linux CLI knowledge
* Wazuh Manager already deployed in your SOC ecosystem
* Wazuh Agent installed + enrolled on your Linux endpoint
* Root/sudo access on endpoint + manager

---

## 📁 Repository Structure

```text
18-auditd-wazuh-credential-access-hunting/
├── README.md
├── commands.sh
├── architecture.txt
├── interview_qna.md
├── troubleshooting.md
├── auditd/
│   └── wazuh.rules
├── wazuh/
│   ├── agent/
│   │   └── ossec.conf.snippet
│   └── manager/
│       ├── lists/
│       │   ├── audit-keys
│       │   └── suspicious-programs
│       ├── rules/
│       │   └── local_rules.xml
│       └── ossec.conf.ruleset.snippet.xml
└── docs/
    └── Linux Auditd Wazuh Credential Access Monitoring Project.pdf
```

---

# 🚀 Implementation Guide (Full Step-by-Step)

> 🧠 Design approach:
> **Auditd** captures *kernel-level truth* → **Wazuh** turns it into *SOC-ready alerts*.

---

## Step 1 — Install Auditd on the Linux Endpoint

On the **Linux endpoint**:

```bash
sudo apt update
sudo apt -y install auditd audispd-plugins
sudo systemctl enable --now auditd
sudo systemctl status auditd
```

✅ Expected:

* auditd is **active (running)**

---

## Step 2 — Create Persistent Audit Rules

### 📌 Why we do this

Auditd only logs what you tell it to.
Here we monitor:

* credential file access (`/etc/passwd`, `/etc/shadow`)
* execve command execution telemetry (user activity)
* SSH key persistence areas
* bash history access (recon or cover tracks)

Create a rules file:

```bash
sudo nano /etc/audit/rules.d/wazuh.rules
```

Paste:

```bash
# -------------------------------
# Auditd rules for Wazuh SOC use
# -------------------------------

# Clear old rules
-D

# Buffer tuning (helps under burst activity)
-b 8192
--backlog_wait_time 60000

# 1) Track command execution (execve) for user sessions (AUID tracking)
-a always,exit -F arch=b64 -S execve -F auid>=1000 -F auid!=-1 -k audit-wazuh-c
-a always,exit -F arch=b32 -S execve -F auid>=1000 -F auid!=-1 -k audit-wazuh-c

# 2) Credential access monitoring
-w /etc/passwd -p wa -k passwd_access
-w /etc/shadow -p wa -k shadow_access

# 3) SSH persistence / key access monitoring
-w /home -p wa -k user_home_changes
-w /root -p wa -k root_home_changes
-w /etc/ssh/sshd_config -p wa -k ssh_config_changes

# 4) Bash history monitoring
-w /home -p wa -k bash_history
-w /root/.bash_history -p wa -k bash_history
```

Save and exit.

---

## Step 3 — Load Rules & Verify They Are Active

Load rules:

```bash
sudo augenrules --load
sudo systemctl restart auditd
```

Verify loaded rules:

```bash
sudo auditctl -l
```

✅ Expected:

* you see watch rules for `/etc/shadow`, `/etc/passwd`, `/home`
* you see execve rules with `-k audit-wazuh-c`

---

## Step 4 — Generate Test Events (Credential Access Simulation)

Run on endpoint:

```bash
cat /etc/shadow
cat /etc/passwd
cat ~/.ssh/authorized_keys
cat ~/.bash_history
```

You can also simulate credential searching:

```bash
grep -i login /etc/passwd
grep -i password /etc/passwd
```

---

## Step 5 — Validate Audit Logs Locally (Before SIEM)

Tail audit log:

```bash
sudo tail -f /var/log/audit/audit.log
```

Search by key:

```bash
sudo ausearch -k shadow_access
sudo ausearch -k passwd_access
sudo ausearch -k bash_history
sudo ausearch -k audit-wazuh-c
```

✅ Expected:

* audit events appear with rich context (uids, syscall metadata, file paths)

---

# 🧩 Wazuh Integration

## Step 6 — Configure Wazuh Agent to Read `audit.log`

On endpoint edit:

```bash
sudo nano /var/ossec/etc/ossec.conf
```

Add:

```xml
<localfile>
  <log_format>audit</log_format>
  <location>/var/log/audit/audit.log</location>
</localfile>
```

Restart agent:

```bash
sudo systemctl restart wazuh-agent
sudo systemctl status wazuh-agent
```

✅ Expected:

* agent is running
* audit logs will be forwarded

---

## Step 7 — Create CDB Lists on Wazuh Manager

CDB lists are used to **classify + enrich** audit events.

### 7.1 Create `audit-keys` list

On Wazuh Manager:

```bash
sudo nano /var/ossec/etc/lists/audit-keys
```

Paste:

```text
passwd_access:passwd
shadow_access:shadow
history_access:history
ssh_access:ssh
audit-wazuh-c:command
bash_history:bash
user_home_changes:home
root_home_changes:home
ssh_config_changes:ssh
```

### 7.2 Create `suspicious-programs` list

```bash
sudo nano /var/ossec/etc/lists/suspicious-programs
```

Paste:

```text
nc:yellow
ncat:yellow
netcat:yellow
tcpdump:orange
strace:orange
gdb:red
```

---

## Step 8 — Register Lists in Wazuh Manager Configuration

Edit Wazuh Manager config:

```bash
sudo nano /var/ossec/etc/ossec.conf
```

Inside `<ruleset>` add:

```xml
<list>etc/lists/audit-keys</list>
<list>etc/lists/suspicious-programs</list>
```

Compile lists:

```bash
sudo /var/ossec/bin/wazuh-makelists
```

Restart manager:

```bash
sudo systemctl restart wazuh-manager
```

✅ Expected:

* `.cdb` files are generated successfully

---

## Step 9 — Create Custom Detection Rules (Wazuh Manager)

Edit:

```bash
sudo nano /var/ossec/etc/rules/local_rules.xml
```

Add:

```xml
<group name="cred_access,">

  <!-- Detect /etc/passwd access category -->
  <rule id="100110" level="7">
    <if_group>audit</if_group>
    <list field="audit.key" lookup="match_key_value" check_value="passwd">etc/lists/audit-keys</list>
    <description>File access detected: $(audit.file.name) accessed (passwd category)</description>
  </rule>

  <!-- Detect /etc/shadow access category (higher severity) -->
  <rule id="100120" level="10">
    <if_group>audit</if_group>
    <list field="audit.key" lookup="match_key_value" check_value="shadow">etc/lists/audit-keys</list>
    <description>Possible credential access: $(audit.file.name) accessed (shadow category)</description>
    <mitre>
      <id>T1003.008</id>
    </mitre>
  </rule>

</group>

<group name="audit_command,">

  <!-- High severity: suspicious program marked red -->
  <rule id="100210" level="12">
    <if_group>audit</if_group>
    <list field="audit.command" lookup="match_key_value" check_value="red">etc/lists/suspicious-programs</list>
    <description>Audit: HIGH risk command executed: $(audit.command)</description>
  </rule>

</group>
```

Restart manager:

```bash
sudo systemctl restart wazuh-manager
```

---

# 🧪 Detection Validation

## Step 10 — Attack Simulation (Endpoint)

Run:

```bash
cat /etc/shadow
cat /etc/passwd
cat ~/.ssh/authorized_keys
cat ~/.bash_history
grep -i login /etc/passwd
```

If you want to trigger suspicious tool classification:

```bash
gdb --help
tcpdump --help
```

---

## Step 11 — Verify Alerts on the Wazuh Manager

Check alerts:

```bash
sudo tail -f /var/ossec/logs/alerts/alerts.log
```

✅ Expected:

* alerts with rule IDs like `100110`, `100120`, `100210`

---

## Step 12 — Verify Alerts in Wazuh Dashboard

### ✅ Threat Hunting view

* Go to **Threat Hunting**
* Search examples:

```text
data.audit.execve.a1 : "/etc/shadow"
```

```text
data.audit.command : "cat"
```

```text
rule.id : 100120
```

### ✅ Analyst view (Discover)

* Go to **Discover**
* Validate event includes:

  * `agent.name`
  * `data.audit.auid`, `data.audit.euid`
  * `data.audit.exe`
  * `data.audit.execve.a0/a1`
  * `data.audit.key`
  * rule description / level

---

## ✅ Results

By the end of this project:

* ✅ auditd installed and collecting kernel-level telemetry
* ✅ persistent audit rules created and verified
* ✅ audit logs forwarded to Wazuh via agent
* ✅ CDB lists created for audit keys + suspicious programs
* ✅ custom Wazuh rules detect credential access activity
* ✅ alerts validated in Wazuh Threat Hunting + Discover views

---

## 🧠 What I Learned

* Kernel-level audit telemetry provides **forensic-grade truth**
* “Credential access” is often a chain of small actions that become high-signal when monitored correctly
* Wazuh becomes much stronger when paired with a **high-fidelity data source** like auditd
* CDB lists are powerful for fast enrichment and classification in detections

---

## 🌍 Why This Matters

In real SOC environments, credential access is often the turning point between:

* Recon → Persistence → Lateral Movement

Monitoring actions like:

* reading `/etc/shadow`
* scanning `/etc/passwd`
* SSH key inspection
* …creates early warning indicators before a bigger incident happens.

---

## 🧩 Real-World Applications

* ✅ Compliance logging (PCI-DSS, NIST-aligned auditing)
* ✅ Insider threat monitoring
* ✅ Privilege escalation investigations
* ✅ Credential dumping detection validation
* ✅ Incident response evidence collection (“who did what and when”)

---

## 🔮 Future Enhancements

* Add rule correlation (multiple credential actions in timeframe)
* Add active response (block user / isolate host based on key events)
* Expand suspicious-programs list for SOC tooling patterns
* MITRE mapping for additional audit-driven detections

---

## 📎 PDF Guide

For the full step-by-step PDF with screenshots and validation, see:

📄 **[Auditd + Wazuh kernal monitoring, auditing PDF Guide](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/18-auditd-wazuh-credential-access-hunting/docs/Linux%20Auditd%20Wazuh%20Credential%20Access%20Monitoring%20Project.pdf)**

---

## 📚 References (Official)

* 🔗 [Wazuh blog: hunting Linux credential access attacks with Wazuh](https://wazuh.com/blog/hunting-for-linux-credential-access-attacks-with-wazuh/)
* 🔗 [Wazuh PoC: audit commands run by user](https://documentation.wazuh.com/current/proof-of-concept-guide/audit-commands-run-by-user.html)
* 🔗 [Wazuh docs: audit configuration and system calls monitoring](https://documentation.wazuh.com/current/user-manual/capabilities/system-calls-monitoring/audit-configuration.html)

---

## 🌐 Project Post on LinkedIn

I also shared this project on LinkedIn with a concise portfolio summary, key highlights, and implementation context.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-View%20Project%20Post-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/posts/abdul4rehman215_linux-auditd-wazuh-credential-access-monitoring-activity-7432812968255553536-IgLI?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEuho14BQnjOksWA5iihN6dnsE3C-o3yBUU)

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
