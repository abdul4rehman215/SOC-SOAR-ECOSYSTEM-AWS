# 🎤 Wazuh Installation – Interview Q&A
### AWS EC2 – All-in-One SOC Deployment

---

## 1️⃣ What components are installed in an all-in-one Wazuh deployment?

An all-in-one deployment installs the Wazuh Manager, Wazuh Indexer (OpenSearch-based), Wazuh Dashboard, and Filebeat on a single server.

---

## 2️⃣ Why did you choose an EC2 instance with 8GB RAM for Wazuh?

The Indexer component is memory intensive. Less than 8GB RAM can cause instability, index corruption, or dashboard failures.

---

## 3️⃣ What is the role of the Wazuh Manager?

The Manager receives agent logs, applies decoders and rules, performs correlation, and generates security alerts.

---

## 4️⃣ What port does Wazuh use for agent communication?

Port 1514 TCP is used for secure agent log transmission, and 1515 TCP is used for agent enrollment.

---

## 5️⃣ Why should port 9200 (Indexer) not be exposed publicly?

Port 9200 provides access to stored logs and alerts. Exposing it publicly can lead to data leakage or unauthorized access.

---

## 6️⃣ What is the purpose of Filebeat in Wazuh architecture?

Filebeat forwards processed alerts and logs from the Manager to the Indexer for storage and visualization.

---

## 7️⃣ How does Wazuh perform vulnerability detection?

It uses integrated providers such as Canonical, Debian, MSU, and NVD feeds to correlate installed packages with known CVEs.

---

## 8️⃣ What is File Integrity Monitoring (FIM) in Wazuh?

FIM monitors changes to critical system files and directories and generates alerts when unauthorized modifications occur.

---

## 9️⃣ What happens if the Indexer service crashes?

The Dashboard becomes inaccessible, alerts stop being indexed, and search functionality fails. Typically caused by low memory or disk issues.

---

## 🔟 How do you validate that Wazuh services are healthy?

By checking:
- systemctl status for services
- Port listening via ss -tulnp
- Reviewing ossec.log
- Accessing dashboard
- Testing API on port 55000

---

## 1️⃣1️⃣ Why is it important to backup ossec.conf before editing?

Syntax errors in ossec.conf can prevent the Manager from starting. A backup allows quick rollback.

---

## 1️⃣2️⃣ What encryption is used in Wazuh communication?

Agent-to-manager communication is encrypted, and Dashboard/API communication is secured using TLS.

---

## 1️⃣3️⃣ What are common causes of agents not connecting?

Blocked ports (1514/1515), incorrect server IP configuration, firewall restrictions, or manager service not running.

---

## 1️⃣4️⃣ How can Wazuh be integrated into a SOC ecosystem?

It can integrate with:
- MISP (Threat Intelligence)
- TheHive (Case Management)
- Cortex (Analyzers)
- AWS CloudTrail
- IDS tools like Suricata and Zeek
- Automation platforms like n8n

---

## 1️⃣5️⃣ What makes Wazuh suitable for a SOC environment?

It provides centralized log collection, detection engineering capabilities, compliance monitoring, vulnerability assessment, and automation support within a single platform.

---

End of Interview Q&A.
