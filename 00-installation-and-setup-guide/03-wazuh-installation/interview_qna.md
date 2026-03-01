# 🎤 Interview Q&A — Project 03: Wazuh All-in-One Installation (AWS EC2)

---

## 1) What is included in a Wazuh “All-in-One” installation?
It installs the Wazuh Manager, Wazuh Indexer, Wazuh Dashboard, and Filebeat on the same server for fast deployment and testing.

---

## 2) Why did you use the official `wazuh-install.sh -a` method?
It provides the quickest reliable installation using Wazuh’s supported installer and sets up certificates and services automatically.

---

## 3) Why do you recommend 8GB RAM minimum for Wazuh All-in-One?
The indexer and dashboard are memory-intensive; below 8GB can cause swap pressure, dashboard instability, or indexer crashes.

---

## 4) What is the purpose of port 443 in Wazuh?
Port 443 is used for the Wazuh Dashboard web UI (HTTPS access).

---

## 5) Which ports are required for agent communication and enrollment?
1514/TCP is used for agent event communication, and 1515/TCP is used for agent enrollment (authd service).

---

## 6) What is the role of Filebeat in Wazuh?
Filebeat ships alerts and events from the Wazuh Manager to the Wazuh Indexer using secure TLS communication.

---

## 7) What does the Wazuh Indexer do?
It stores and indexes security events and alerts, allowing fast searching and dashboard visualizations.

---

## 8) Why is JSON output enabled in your configuration?
JSON logs make parsing and integration easier, improve consistency, and support automation, correlation, and downstream analysis.

---

## 9) What is Syscollector and why enable it?
Syscollector collects system inventory like installed packages, running services, users, and network info to improve asset visibility and investigations.

---

## 10) What is SCA and why enable it?
SCA (Security Configuration Assessment) checks system configuration against compliance/security benchmarks like CIS and detects posture gaps.

---

## 11) What does Wazuh Vulnerability Detection provide?
It correlates installed software inventory with vulnerability feeds (Canonical/Debian/NVD) to identify known vulnerabilities on monitored systems.

---

## 12) Why did you configure Rootcheck and Syscheck (FIM)?
Rootcheck helps detect rootkit indicators and risky configurations, while Syscheck monitors file integrity changes in critical directories.

---

## 13) Why do you backup `ossec.conf` before editing?
To ensure quick rollback if a configuration mistake breaks service startup or causes unexpected behavior.

---

## 14) Why restart only `wazuh-manager` after editing `ossec.conf`?
`ossec.conf` controls manager behavior. Restarting only wazuh-manager applies changes without unnecessarily impacting other components.

---

## 15) What is the most common cause of “Dashboard down” in AWS?
Security Group inbound rules missing TCP 443 or restricting it incorrectly, preventing browser access to the dashboard.

---
