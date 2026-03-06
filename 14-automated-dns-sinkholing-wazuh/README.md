# 🛡️ Automated DNS Sinkholing using Wazuh Active Response, DNS-Stats, and AlienVault OTX

---

## 🔗 IMPORTANT PREREQUISITE

This project EXTENDS the DNS-Stats + AlienVault OTX detection pipeline.

You MUST complete the previous DNS threat hunting project first:

👉 **Complete the DNS-Stats + AlienVault OTX Detection Pipeline First**

[Guide-to-it](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS)

This sinkholing project builds directly on top of:

* Sysmon DNS telemetry (Event ID 22)
* DNS-Stats enrichment
* AlienVault OTX validation
* Custom Wazuh rules

---

## 📐 Architecture Reference

<p align="center">
  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/Automated-dns-sinkholing-architecture-in-soc.png">
</p>

---

# 1️⃣ Project Overview

Previously we had:

- ✔ DNS detection
- ✔ Rare domain detection (DNS-Stats)
- ✔ IOC validation (AlienVault OTX)
- ✔ SOC alert visibility

But:

❌ No automated containment

Now we extend it into:

- ✔ Automated DNS sinkholing
- ✔ Endpoint-level domain blocking
- ✔ Active Response automation
- ✔ Detection → Validation → Enforcement lifecycle

---

# 2️⃣ What is DNS Sinkholing?

DNS Sinkholing is a defensive technique where malicious domains are deliberately redirected to a safe IP address (usually localhost).

Instead of:

```
acmetoy.com → 204.16.169.54
```

It becomes:

```
acmetoy.com → 127.0.0.1
```

The endpoint never reaches attacker infrastructure.

This is endpoint-level containment.

---

# 3️⃣ Full Detection → Response Flow

1. Windows endpoint queries domain
2. Sysmon logs Event ID 22
3. Wazuh ingests DNS log
4. DNS-Stats checks rarity
5. AlienVault OTX validates IOC
6. High-severity rule fires (Rule 100080)
7. Wazuh Active Response triggers
8. PowerShell sinkhole script executes
9. Domain added to HOSTS file
10. Domain permanently resolves to 127.0.0.1

---

# 4️⃣ Environment Requirements

## Wazuh Manager (Linux)

* Ubuntu 22.04
* DNS-Stats running
* AlienVault OTX integration working
* Internet access

## Windows Endpoint

* Windows 10/11
* Sysmon installed
* Wazuh Agent installed
* PowerShell 7 installed

---

# 5️⃣ STEP-BY-STEP IMPLEMENTATION

We start from Active Response extension.

---

# 🔵 PART 1 – Windows Endpoint Configuration

---

## STEP 1 – Create DNS Sinkhole PowerShell Script

Location:

```
C:\Windows\PowerShell\malicious_domains.ps1
```

Open PowerShell as Administrator:

```powershell
notepad C:\Windows\PowerShell\malicious_domains.ps1
```

Paste FULL script:

```powershell
#############################################
# Wazuh Automated DNS Sinkhole Script
#############################################

$log = "C:\Windows\Temp\sinkhole.log"

"---------------------------------------" | Out-File -Append $log
"Execution Time: $(Get-Date)" | Out-File -Append $log

# Read JSON input from Wazuh
$INPUT_JSON = Read-Host
$INPUT_ARRAY = $INPUT_JSON | ConvertFrom-Json
$INPUT_ARRAY = $INPUT_ARRAY | ConvertFrom-Json

# Extract malicious domain from OTX alert
$malicious_domain = $INPUT_ARRAY.parameters.alert.data.base_indicator.indicator

if (-not $malicious_domain) {
    "No malicious domain found in alert" | Out-File -Append $log
    exit 0
}

"Malicious domain detected: $malicious_domain" | Out-File -Append $log

# Hosts file location
$hosts_file = "$env:windir\System32\drivers\etc\hosts"

# Prevent duplicate entries
if (Select-String -Path $hosts_file -Pattern $malicious_domain -Quiet) {
    "Domain already sinkholed" | Out-File -Append $log
    exit 0
}

# Add sinkhole entry
Add-Content -Path $hosts_file -Value "`n127.0.0.1`t$malicious_domain" -Force

"Domain sinkholed successfully" | Out-File -Append $log
```

Save.

---

## STEP 2 – Create Active Response CMD Wrapper

Location:

```
C:\Program Files (x86)\ossec-agent\active-response\bin\domains.cmd
```

Open as Administrator:

```cmd
notepad "C:\Program Files (x86)\ossec-agent\active-response\bin\domains.cmd"
```

Paste:

```cmd
@echo off

"C:\Program Files\PowerShell\7\pwsh.exe" -ExecutionPolicy Bypass -File "C:\Windows\PowerShell\malicious_domains.ps1"

exit
```

Save.

---

## STEP 3 – Restart Wazuh Agent

```cmd
net stop wazuh-agent
net start wazuh-agent
```

---

# 🔵 PART 2 – Wazuh Manager Configuration

---

## STEP 4 – Edit ossec.conf

On Wazuh Manager:

```bash
sudo nano /var/ossec/etc/ossec.conf
```

---

## Add Command Block

```xml
<command>
  <name>malicious_domains</name>
  <executable>domains.cmd</executable>
  <timeout_allowed>no</timeout_allowed>
</command>
```

---

## Add Active Response Block

Use your AlienVault rule ID:

Rule ID: 100080

Add:

```xml
<active-response>
  <disabled>no</disabled>
  <command>malicious_domains</command>
  <location>local</location>
  <rules_id>100080</rules_id>
</active-response>
```

Save file.

---

## STEP 5 – Restart Wazuh Manager

```bash
sudo systemctl restart wazuh-manager
```

---

# 🔵 PART 3 – Full Pipeline Testing

---

## STEP 6 – Trigger Malicious DNS Query

On Windows endpoint:

```powershell
ping acmetoy.com
```

---

## STEP 7 – Validate Pre-Response DNS Resolution

In Sysmon Event Viewer:

Event ID 22 shows:

```
QueryName: acmetoy.com
QueryResults: 204.16.169.54
```

This confirms malicious resolution BEFORE response.

---

## STEP 8 – Observe Wazuh Alert Chain

Dashboard should show:

- 1️⃣ Sysmon DNS Query Detected
- 2️⃣ DNS-Stats – Domain Queried for First Time
- 3️⃣ AlienVault OTX – Indicator(s) Found

Rule ID 100080 fires.

---

## STEP 9 – Automatic Active Response Executes

Without manual action:

* domains.cmd executed
* malicious_domains.ps1 runs
* HOSTS file modified

---

## STEP 10 – Re-Test Domain

```powershell
ping acmetoy.com
```

Now:

```
Reply from 127.0.0.1
```

Domain successfully sinkholed.

---

## STEP 11 – Validate Sysmon After Sinkholing

Event ID 22 now shows:

```
QueryResults: ::ffff:127.0.0.1
```

No external IP.

---

## STEP 12 – Confirm HOSTS File

Open:

```
C:\Windows\System32\drivers\etc\hosts
```

You should see:

```
127.0.0.1    acmetoy.com
```

---

## 📂 Repository Structure

```
14-automated-dns-sinkholing-wazuh/
│
├── README.md
├── commands.sh
├── architecture-notes.txt
├── interview_qna.md
├── troubleshooting.md
│
├── manager/
│   └── ossec-active-response-config.xml
│
├── windows-endpoint/
│   ├── malicious_domains.ps1
│   └── domains.cmd
│
└── docs/
    └── Automated DNS Sinkholing using Wazuh Active Response.pdf
```

---

# 6️⃣ What This Enables in Your SOC

* Automated containment
* Domain-level blocking
* Real-time response
* Threat-intel-driven enforcement
* Reduced analyst workload
* Improved MTTR
* Endpoint-level protection

---

# 7️⃣ Enterprise Impact

Before:
Detection only

After:
Detection + Validation + Automated Enforcement

This is detection engineering maturity.

---

# 8️⃣ Skills Demonstrated

* Advanced Wazuh configuration
* Active Response automation
* PowerShell remediation scripting
* DNS containment strategy
* SOC workflow automation
* Threat-intel correlation
* Detection lifecycle extension

---

# 9️⃣ Final Result

You now have:

- ✔ DNS detection
- ✔ IOC validation
- ✔ Automated sinkholing
- ✔ Endpoint-level containment
- ✔ SOC-grade automation

---

# 📄 PDF Guide Reference

For complete visual step-by-step screenshots and terminal walkthrough, refer to the detailed PDF implementation guide included in the repository resources folder. Or click below.

👉 **[Click here to view the complete PDF walkthrough guide](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/14-automated-dns-sinkholing-wazuh/docs/Automated%20DNS%20Sinkholing%20using%20Wazuh%20Active%20Response.pdf)**

---

## 🌐 Project Post on LinkedIn

I also shared this project on LinkedIn with a concise portfolio summary, key highlights, and implementation context.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-View%20Project%20Post-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/posts/abdul4rehman215_automated-dns-sinkholing-using-wazuh-active-activity-7428661928274685952-r09C?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEuho14BQnjOksWA5iihN6dnsE3C-o3yBUU)

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
