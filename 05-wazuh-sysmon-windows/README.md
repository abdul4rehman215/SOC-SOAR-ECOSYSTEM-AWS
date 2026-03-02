# 🛡️ Wazuh + Sysmon Advanced Windows Monitoring

## 📌 Project Overview

This project demonstrates a full endpoint security monitoring pipeline using:

* Windows 10/11 Endpoint
* Sysmon (System Monitor)
* Wazuh Windows Agent
* Wazuh Manager (Linux)
* Wazuh Dashboard
* APTSimulator (attack simulation)

The objective:

* Install and configure Sysmon properly
* Integrate Sysmon logs into Wazuh
* Build custom detection rules
* Detect encoded PowerShell, DNS C2, LOLBins, LSASS access
* Tune noisy events
* Validate detection end-to-end

---

# 🏗️ Architecture

<div align="center">

<img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/Wazuh%20and%20Sysmon%20threat%20detection%20architecture.png" width="800"/>

</div>

```
Windows Endpoint
   ├── Sysmon (Event Channel Logging)
   ├── Wazuh Agent
        ↓
Secure Connection (1514/1515)
        ↓
Wazuh Manager (Linux)
        ↓
Wazuh Dashboard (Threat Hunting / Discover)
```

---

# ❓ Why Use Sysmon Instead of Default Wazuh Windows Logging?

## 🔹 Default Wazuh Windows Logging

By default, Wazuh collects:

* Security Event Log
* System Log
* Application Log

Limitations:

* No detailed process command-line visibility
* No DNS telemetry
* Limited registry monitoring
* No hash logging
* No parent-child process tracking

---

## 🔥 Sysmon Advantages

Sysmon provides:

| Feature                    | Default Windows | Sysmon   |
| -------------------------- | --------------- | -------- |
| Full command line logging  | ❌               | ✅        |
| DNS Query logging          | ❌               | ✅        |
| Registry monitoring        | Limited         | Advanced |
| File hash logging          | ❌               | ✅        |
| Parent process tracking    | Partial         | Full     |
| Network connection details | Basic           | Detailed |

Sysmon enables:

* C2 detection
* Encoded PowerShell detection
* Persistence detection
* Credential dumping detection
* LOLBins detection

This is why SOC teams deploy Sysmon.

---

# 🖥️ PART 1 – Install Wazuh Agent on Windows

Download Windows Agent from:

[installation-guide_wazuh-agent](https://documentation.wazuh.com/current/installation-guide/wazuh-agent/)

Install.

Edit:

```
C:\Program Files (x86)\ossec-agent\ossec.conf
```

Add:

```xml
<localfile>
  <location>Microsoft-Windows-Sysmon/Operational</location>
  <log_format>eventchannel</log_format>
</localfile>
```

Restart Agent:

```powershell
Restart-Service Wazuh
```

---

# 🖥️ PART 2 – Install Sysmon on Windows

Download Sysmon:

[downloads_sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon)

Extract to:

```
C:\Sysmon\
```

---

## Example sysmon_config.xml (stored in /sysmon folder)

```xml
<Sysmon schemaversion="4.50">
  <EventFiltering>

    <ProcessCreate onmatch="include" />
    <NetworkConnect onmatch="include" />
    <RegistryEvent onmatch="include" />

    <DnsQuery onmatch="include">
      <QueryName condition="contains">.</QueryName>
    </DnsQuery>

  </EventFiltering>
</Sysmon>
```

---

Install Sysmon:

```powershell
cd C:\Sysmon
.\Sysmon64.exe -accepteula -i sysmon_config.xml
```

Verify in:

Event Viewer → Microsoft → Windows → Sysmon → Operational

---

# 🧩 PART 3 – Custom Wazuh Rules

Location on Manager:

```
/var/ossec/etc/rules/
```

Place:

```
sysmon_custom_v2.xml
```

Restart:

```bash
systemctl restart wazuh-manager
```

---

# 🔐 Detection Use Cases Implemented

## ✅ Encoded PowerShell

MITRE: T1059.001

Detect:

```
powershell.exe -EncodedCommand
```

---

## ✅ Suspicious DNS from PowerShell

MITRE: T1071.004

Detect:

* powershell.exe performing DNS queries
* cmd.exe performing DNS queries

---

## ✅ LSASS Access Attempt

MITRE: T1003

Detect:

* Process accessing lsass.exe

---

## ✅ LOLBins Execution

MITRE: T1218

Detect:

* certutil.exe
* rundll32.exe
* mshta.exe

---

# 🧪 Attack Simulation

Use:

[APTSimulator](https://github.com/NextronSystems/APTSimulator)

Run:

```
APTSimulator.bat
Select: Command and Control
```

---

# 📊 Validation

In Wazuh Dashboard:

Filter:

```
rule.groups: sysmon
```

Expected:

* Event ID 1
* Event ID 22
* Encoded PowerShell alert
* Suspicious DNS alert

---

# 📁 Repository Structure

```
wazuh-sysmon-windows/
│
├── README.md
├── commands.sh
├── architecture-notes.txt
├── interview_qna.md
├── troubleshooting.md
│
├── rules/
│   ├── sysmon_custom_v1.xml
│   ├── sysmon_custom_v2.xml
│
├── images/

```

---

# 📁 Screenshots Folder Guide

Place screenshots inside `/images`

Example:

```
images/
  01-architecture.png
  02-sysmon-install.png
  03-agent-connected.png
  04-dns-event22.png
  05-encoded-powershell.png
  06-lsass-detection.png
```

Reference in README like:

```markdown
![Sysmon Installed](images/02-sysmon-install.png)
```

---

# 🧠 What This Project Demonstrates

* Endpoint telemetry engineering
* Log pipeline troubleshooting
* Detection engineering
* MITRE ATT&CK mapping
* Noise reduction strategies
* SOC-level monitoring design

---

# 🏁 Final Outcome

This project simulates:

* Real SOC telemetry ingestion
* Advanced Windows logging
* Attack simulation
* Detection validation
* Rule tuning workflow

---
