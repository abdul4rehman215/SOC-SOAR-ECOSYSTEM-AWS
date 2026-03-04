# 🎤 interview Q&A — Snort IDS Exploration + Wazuh SIEM Integration

## 1) 🐷 What is Snort in one line?
Snort is a network intrusion detection system (NIDS) that inspects live traffic and triggers alerts based on rules.

## 2) 🌐 What new visibility does Snort add to a SOC?
It adds **network-layer visibility**—scans, probes, and suspicious traffic on the wire—beyond endpoint logs.

## 3) 🧠 What’s the difference between Snort “sniffer” mode and IDS mode?
Sniffer mode shows packets, while IDS mode applies rules/signatures to detect suspicious traffic and generate alerts.

## 4) 🧾 Where are Snort’s main config and custom rules stored on Ubuntu?
`/etc/snort/snort.conf` (config) and `/etc/snort/rules/local.rules` (custom rules).

## 5) ✅ Why is `snort -T` important before running IDS mode?
It validates configuration and rule syntax so Snort won’t fail during live monitoring.

## 6) 🧩 What is `$HOME_NET` and why does it matter?
It defines your protected network range, so rules can detect traffic targeting your internal systems.

## 7) 🧪 What was the first custom rule you tested in this project?
A simple ICMP rule to detect ping traffic, then improved into Echo Request vs Echo Reply rules.

## 8) 🔁 Why split ICMP rules into Echo Request and Echo Reply?
It helps understand direction and traffic flow—outbound requests vs inbound replies—more accurately.

## 9) 🧰 What is Snorpy and why did you use it?
Snorpy is a GUI-based Snort rule generator that helps create rules visually and reduce syntax mistakes.

## 10) 🧨 What attacker simulation did you perform from Kali?
An FTP connection attempt to the Snort-monitored host to trigger a custom TCP detection rule.

## 11) 🧾 Which Snort log file did you ingest into Wazuh?
`/var/log/snort/snort.alert.fast` (fast alert log output).

## 12) 🔗 How does Wazuh ingest Snort alerts?
The Wazuh agent monitors the Snort log using `<localfile>` and forwards alerts to the Wazuh manager.

## 13) 🧠 Why is Snort + Wazuh stronger than Snort alone?
Because alerts become centralized, searchable, and correlatable with endpoint security events inside the SIEM.

## 14) 🛡️ What are common challenges when using Snort in real environments?
False positives and performance impact—rules require tuning and traffic-heavy environments need careful optimization.

## 15) 🎯 What’s a real SOC use case where this integration helps immediately?
Detecting early-stage reconnaissance (like scans and service probing) and correlating it with endpoint activity for faster incident triage.
