# 🛡️ Web Application Protection & Automated IP Blocking  
## ModSecurity + Fail2Ban + Wazuh SIEM (Active Response Security Architecture)

---

# 1️⃣ Project Overview

**Automated Web Attack Detection, Containment & SOC Visibility using NGINX, ModSecurity (WAF), Fail2Ban, and Wazuh SIEM**

<p align="center">
  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/fail2ban-automatic-blocking-intro.png">
</p>

---

## 🎯 Project Objective

This project extends a previously deployed:

- NGINX Web Server
- ModSecurity v3 (WAF)
- OWASP Core Rule Set (CRS)
- Wazuh SIEM Monitoring Stack

Previously, the system was capable of:

- ✔ Detecting web application attacks  
- ✔ Blocking malicious payloads with HTTP 403  
- ✔ Logging and visualizing alerts in Wazuh  

However — attackers could continue attempting attacks repeatedly.

### 🚨 The Problem

WAF blocks payloads — not attackers.

An attacker can:

- Send 100+ malicious requests
- Trigger 403 responses
- Continue attacking indefinitely

---

## 🚀 The Enhancement (This Project)

We upgraded the architecture to introduce:

- ✔ Automatic IP Blocking  
- ✔ Host-Level Containment  
- ✔ Firewall Enforcement  
- ✔ SOC Alert Correlation  
- ✔ Full Attack → Detection → Response Visibility  

Now the lifecycle becomes:

```

Attack → WAF Detection → Fail2Ban Ban → SIEM Alert → SOC Case

```

This transforms the architecture from **passive monitoring** to **active defense automation**.

---

## 🖼️ Architecture Preview

<p align="center">
 <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/fail2ban-automatic-blocking-architecture.png">
</p>
  
---

# 2️⃣ Why This Project Matters

Modern web servers face:

- SQL Injection
- Cross-Site Scripting (XSS)
- Local File Inclusion (LFI)
- Remote Code Execution (RCE)
- Automated bot scanning
- Reconnaissance attempts

Blocking at HTTP level is not enough.

We need:

✔ Detection  
✔ Prevention  
✔ Containment  
✔ Visibility  
✔ Correlation  
✔ Automation  

This project delivers all six.

---

# 3️⃣ What Each Component Does

---

## 🔹 NGINX (Web Server Layer)

NGINX is:

- High-performance
- Event-driven
- Reverse proxy capable
- Widely used in cloud & enterprise environments
- Low memory footprint
- Ideal for high concurrency

Role in this project:

- Hosts the web application
- Acts as inspection entry point
- Forwards logs to monitoring layer

---

## 🔹 ModSecurity v3 (Web Application Firewall)

ModSecurity is:

- Open-source WAF engine
- Rule-based detection
- Uses OWASP CRS
- Inspects HTTP traffic in real time

Capabilities:

✔ Blocks SQLi  
✔ Blocks XSS  
✔ Detects payload patterns  
✔ Performs virtual patching  
✔ Logs full attack metadata  

BUT:

It blocks request — not attacker IP permanently.

---

## 🔹 OWASP Core Rule Set (CRS)

CRS provides:

- Predefined rules for OWASP Top 10
- Injection detection
- Protocol enforcement
- Anomaly scoring
- Severity classification

It gives structure to WAF detection logic.

---

## 🔹 Fail2Ban (Intrusion Prevention System)

Fail2Ban is:

- Log-based intrusion prevention system
- Reads application logs
- Detects repeated malicious patterns
- Automatically bans IP using firewall (iptables/nftables)

In this project:

- Reads ModSecurity audit logs
- Extracts attacker IP
- Enforces firewall rule
- Blocks attacker at host level

This converts detection into containment.

---

## 🔹 Wazuh SIEM (Monitoring & Correlation)

Wazuh provides:

✔ Log ingestion  
✔ Decoding  
✔ Rule matching  
✔ Alert generation  
✔ MITRE ATT&CK mapping  
✔ Dashboard visualization  
✔ Integration with TheHive  

In this project Wazuh collects:

- NGINX logs
- ModSecurity logs
- Fail2Ban logs

So analysts see:

- Attack detected
- IP banned
- Full event metadata
- Correlation across layers

---

## 🔹 TheHive (Case Management)

TheHive provides:

- Incident creation
- Alert-to-case conversion
- Analyst workflow
- Evidence tracking

Now analysts see:

- Attack payload
- Source IP
- Ban action
- Time of containment

---

# 4️⃣ Full Attack Lifecycle

```

Attacker (Kali Linux)
↓
Malicious HTTP Request
↓
NGINX Web Server
↓
ModSecurity (OWASP CRS)
↓
HTTP 403 Response
↓
ModSecurity Audit Log
↓
Fail2Ban Reads Log
↓
IP Extracted
↓
Firewall Ban (iptables)
↓
Fail2Ban Log Entry
↓
Wazuh Agent Collects Logs
↓
Wazuh Manager Decodes & Correlates
↓
Alert Generated
↓
TheHive Case Created

````

---

# 5️⃣ Security Benefits of This Extension

Before Enhancement:

- Detection only
- HTTP blocking only
- Attacker persistence possible

After Enhancement:

✔ Automatic IP banning  
✔ Reduced attack repetition  
✔ Reduced log noise  
✔ Reduced alert fatigue  
✔ Faster containment  
✔ Stronger SOC maturity  
✔ Defense-in-depth  

---

# 6️⃣ Implementation Guide (Fail2Ban Extension)

---

## Step 1 – Install Fail2Ban

```bash
sudo apt update
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
sudo systemctl status fail2ban
````

---

## Step 2 – Create Jail for ModSecurity

```bash
sudo nano /etc/fail2ban/jail.d/modsecurity.conf
```

Add:

```ini
[modsecurity]
enabled  = true
filter   = modsecurity
logpath  = /var/log/modsec_audit.log
backend  = polling
maxretry = 5
findtime = 300
bantime  = 3600
```

---

## Step 3 – Create Filter for ModSecurity

```bash
sudo nano /etc/fail2ban/filter.d/modsecurity.conf
```

```ini
[Definition]
failregex = ^.*ModSecurity: Access denied with code 403.*hostname "<HOST>".*$
ignoreregex =
```

---

## Step 4 – Test Filter

```bash
sudo fail2ban-regex /var/log/modsec_audit.log /etc/fail2ban/filter.d/modsecurity.conf
```

Ensure matches detected.

---

## Step 5 – Restart Fail2Ban

```bash
sudo systemctl restart fail2ban
sudo fail2ban-client status modsecurity
```

---

## Step 6 – Send Fail2Ban Logs to Wazuh

Edit:

```bash
sudo nano /var/ossec/etc/ossec.conf
```

Add:

```xml
<localfile>
  <log_format>syslog</log_format>
  <location>/var/log/fail2ban.log</location>
</localfile>
```

Restart agent:

```bash
sudo systemctl restart wazuh-agent
```

---

## Step 7 – Create Wazuh Decoder

On Wazuh Manager:

```bash
sudo nano /var/ossec/etc/decoders/local_decoder.xml
```

```xml
<decoder name="fail2ban">
  <program_name>fail2ban</program_name>
</decoder>
```

---

## Step 8 – Create Custom Wazuh Rules

```bash
sudo nano /var/ossec/etc/rules/local_rules.xml
```

```xml
<group name="fail2ban,security">

  <rule id="100200" level="10">
    <match>Ban</match>
    <description>Fail2Ban blocked an IP address</description>
  </rule>

  <rule id="100201" level="5">
    <match>Unban</match>
    <description>Fail2Ban unblocked an IP address</description>
  </rule>

</group>
```

Restart:

```bash
sudo systemctl restart wazuh-manager
```

---

## Step 9 – Simulate Attack

From Kali:

```bash
for i in {1..6}; do
  curl "http://SERVER_IP/?test=<script>alert(1)</script>"
done
```

---

## Step 10 – Verify Ban

```bash
sudo fail2ban-client status modsecurity
sudo iptables -L -n
```

Attacker IP should appear banned.

---

## Step 11 – Verify Wazuh Alerts

Search in dashboard:

```
rule.id:100200
```

You should see:

* Fail2Ban blocked IP
* ModSecurity alert
* Correlation chain

---

## Step 12 – Verify in TheHive

Open alert → convert to case → confirm:

- ✔ IP banned
- ✔ Attack payload visible
- ✔ Rule ID
- ✔ Ban duration

---

# 7️⃣ SOC Use Cases Enabled

* Automated web attack containment
* IP reputation tracking
* Attack frequency monitoring
* Ban/unban trend analysis
* Correlation between detection & response
* SOC case documentation
* MITRE ATT&CK visibility
* Analyst workflow improvement

---

# 8️⃣ Skills Demonstrated

* WAF configuration
* Log engineering
* Fail2Ban jail creation
* Regex filter design
* Firewall validation
* SIEM rule creation
* Custom decoder writing
* SOC alert correlation
* Attack simulation
* Defense automation

---

# 9️⃣ Real-World Relevance

This mirrors enterprise architecture where:

* WAF blocks payload
* IPS blocks attacker
* SIEM correlates
* SOAR / case system manages incident

This is not a lab demo —
This is real SOC automation architecture.

---

# 🔟 Repository Structure

```
12-fail2ban-modsecurity-ip-block/
|
├── README.md
├── commands.sh
├── architecture.txt
├── interview_qna.md
├── troubleshooting.md
|
├── configs/
|   ├── fail2ban/
│       ├── jail_modsecurity.conf
│       ├── filter_modsecurity.conf
│
├── wazuh/
│   ├── decoder_fail2ban.xml
│   ├── rules_fail2ban.xml
│
├── docs/
│   ├── 
```

---

# 🏁 Final Conclusion

This project upgrades a monitored web server into an automated active defense system.

- ✔ Detects web attacks
- ✔ Blocks malicious payloads
- ✔ Bans attacker IP
- ✔ Logs containment
- ✔ Visualizes alerts
- ✔ Enables SOC investigation

Attack → Detect → Block → Contain → Monitor → Investigate

That is security maturity.

---
