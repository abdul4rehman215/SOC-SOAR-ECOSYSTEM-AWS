# 💬 Interview Q&A — Auditd + Wazuh (Linux Credential Access Hunting)

> Short, practical interview questions based on what was implemented in this project (Auditd rules, Wazuh ingestion, CDB lists, custom detections, validation).

---

## 1) What problem does auditd solve that normal Linux logs don’t?
Auditd captures **kernel-level events** (syscalls + file access) with strong attribution, while normal logs may miss or abstract actions and are easier to bypass.

---

## 2) What is the most important advantage of auditd for investigations?
Auditd answers **“who did what and when”** with rich context like **AUID/EUID, syscall, command arguments, target file, timestamp, success/failure**.

---

## 3) What is the difference between AUID and EUID, and why does SOC care?
- **AUID** = original logged-in user (tracks identity across `sudo`)
- **EUID** = effective user (e.g., root after privilege escalation)  
SOC cares because AUID helps identify the **real actor** behind privileged actions.

---

## 4) Why did you monitor `/etc/shadow` and `/etc/passwd` specifically?
Because they are **high-value credential targets**:
- `/etc/shadow` → password hashes (credential dumping risk)
- `/etc/passwd` → user enumeration and identity recon

---

## 5) What does the `execve` audit rule give you in detection engineering?
It provides **command execution telemetry** including the executed binary + arguments, which is crucial for detecting suspicious tools and credential hunting behavior.

---

## 6) What is an audit “key” and how did you use it in Wazuh?
An audit key (e.g., `shadow_access`) tags events from a rule.  
In Wazuh, I used CDB lists to map keys into categories like **shadow/passwd/ssh/history/command** for cleaner detections.

---

## 7) Why integrate auditd with Wazuh instead of monitoring audit.log locally?
Wazuh enables:
- central visibility across endpoints
- real-time alerting
- threat hunting search/pivots
- correlation with other telemetry (SSH, sysmon, IDS, etc.)

---

## 8) What is a Wazuh CDB list and why is it useful here?
A CDB list is a fast lookup database used in rules for enrichment/classification.  
Here it helped classify:
- audit keys → credential categories
- suspicious programs → severity labels

---

## 9) Give an example of a SOC alert produced by this project.
If `/etc/shadow` is accessed (key mapped to **shadow**), Wazuh triggers a higher-severity alert indicating **possible credential access activity**.

---

## 10) How did you validate that auditd rules were actually working before SIEM integration?
I:
- generated test activity (`cat /etc/shadow`, `grep login /etc/passwd`)
- verified locally using:
  - `auditctl -l`
  - `ausearch -k shadow_access`
  - `tail -f /var/log/audit/audit.log`

---

## 11) Where did you configure Wazuh to ingest auditd logs?
On the endpoint Wazuh agent:
- `/var/ossec/etc/ossec.conf` using:
  - `<log_format>audit</log_format>`
  - `<location>/var/log/audit/audit.log</location>`

---

## 12) What Wazuh views are best for SOC validation and investigation?
- **Threat Hunting** → fast searching/filtering and pivots  
- **Discover** → deep event inspection (full JSON, fields, attribution)

---

## 13) What are common false-positive risks with auditd-based detections?
Legitimate admin activity can access sensitive files.  
That’s why context matters:
- which user (AUID)
- which process executed it
- whether it’s repeated patterns
- correlation with other alerts (SSH brute force, privilege changes)

---

## 14) How does this project map to real-world SOC use?
It provides:
- early indicators of credential access/recon
- forensic-grade evidence trails
- compliance-ready monitoring for privileged and sensitive operations

---

## 15) What improvement would you add next to make detections stronger?
Correlation rules such as:
- multiple `/etc/shadow` reads in a short time window
- credential access + suspicious tool execution
- credential access following SSH brute force activity
