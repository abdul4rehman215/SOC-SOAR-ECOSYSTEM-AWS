# 🎤 interview Q&A — Zeek Network Security Monitoring + Wazuh SIEM Integration

## 1) 👁️ What is Zeek in simple terms?
Zeek is a passive network security monitoring tool that turns raw traffic into detailed, structured logs describing network behavior.

## 2) 🚨 How is Zeek different from Snort?
Snort is mainly signature/rule alerting (alarm), while Zeek provides deep context logs (surveillance + forensics) about what actually happened on the network.

## 3) 🧠 What kind of “network story” does Zeek provide?
It shows who talked to whom, on which ports/protocols, what DNS was queried, what TLS cert was used, and how the connection ended.

## 4) 📄 Why did you enable JSON logging in Zeek?
JSON makes Zeek logs structured and easier for Wazuh to parse, index, and search inside the SIEM dashboard.

## 5) 🧩 What is the purpose of `networks.cfg` in Zeek?
It defines internal/private networks so Zeek can classify traffic correctly (internal vs external), improving detection accuracy.

## 6) ⚙️ What does `node.cfg` control in Zeek?
It defines the Zeek node type (standalone) and the network interface Zeek should monitor.

## 7) 🧰 What does `zeekctl deploy` do?
It validates configs, generates policies, and starts Zeek services so logging begins in the current logs directory.

## 8) 📂 Where are Zeek logs stored by default in this setup?
`/opt/zeek/logs/current/` (examples: `conn.log`, `dns.log`, `ssl.log`).

## 9) 🔗 How does Wazuh ingest Zeek logs?
The Wazuh agent monitors Zeek log files using `<localfile>` and forwards them to the Wazuh manager for decoding and alerting.

## 10) 🧠 Why did you build custom decoders and rules for Zeek?
To convert raw Zeek JSON data into structured fields and SOC-ready alerts (DNS, scan behavior, TLS anomalies).

## 11) 🌐 What DNS test did you run to generate Zeek events?
I used `dig` queries like `dig wazuh.com` and `dig virustotal.com` to populate Zeek `dns.log`.

## 12) 🕵️ How did you simulate reconnaissance/port scanning?
From Kali, I used `nc -zv` across multiple ports to generate rejected connections and scan-like patterns in Zeek logs.

## 13) 🔐 How did you test TLS anomaly detections?
I used `curl -k` against known bad certificate sites (self-signed / expired) to generate `ssl.log` anomalies.

## 14) 📊 Why are dashboards important in NSM projects?
Dashboards provide quick situational awareness (trends, top talkers, spikes) so analysts don’t rely only on raw alerts.

## 15) 🎯 What’s the biggest SOC benefit of Zeek + Wazuh?
It enables centralized network visibility and investigation context in the SIEM—moving beyond “alerts” into real network behavior understanding.
