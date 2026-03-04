# 📊 Zeek SOC Dashboard (Importable)

> This directory contains the **exported Wazuh/OpenSearch dashboard** I built for:

✅ **Zeek Network Security Monitoring & Threat Hunting**  
Integrated with **Wazuh SIEM** for SOC-ready visibility.

If you import this file into your Wazuh Dashboard, you will get the **same dashboard layout and panels** I created in this project.

---

## 📁 Contents

- **`Zeek - Network Security Monitoring & Threat Hunting.ndjson`**
  - Exported dashboard + its saved objects (visualizations/searches)
  - Importable directly into Wazuh Dashboard/OpenSearch Dashboards

- **`zeek-soc-dashboard-build-guide.md`**
  - Step-by-step guide for building the dashboard manually (if you want to recreate/tune)

---

## 🎯 What This Dashboard Provides

This dashboard is designed for **SOC visibility + threat hunting** using Zeek logs, including:

- ✅ Total network events
- ✅ Network activity over time (trend)
- ✅ Protocol distribution
- ✅ Top source IPs (top talkers)
- ✅ Top destination IPs
- ✅ Rejected connection trends (possible recon/scans)
- ✅ Port scan activity visibility (based on repeated REJ patterns)
- ✅ SSL/TLS certificate anomaly visibility
- ✅ Raw events table for investigation pivots

---

## 🧩 Requirements

Before importing, ensure:

- Zeek is generating logs in:  
  `/opt/zeek/logs/current/`

- Wazuh agent is ingesting Zeek logs:

```xml
<localfile>
  <log_format>json</log_format>
  <location>/opt/zeek/logs/current/*.log</location>
</localfile>
````

* Zeek rules are enabled in Wazuh so events contain `rule.groups: zeek`
  (This dashboard is designed to work best when filtering Zeek events.)

---

## 📥 How to Import the Dashboard (Recommended)

### ✅ Method A — Import via Wazuh Dashboard UI

1. Open **Wazuh Dashboard**
2. Go to: **Stack Management → Saved Objects**
3. Click: **Import**
4. Select the file:

📌 `Zeek - Network Security Monitoring & Threat Hunting.ndjson`

5. Enable:

   * ✅ **Automatically overwrite conflicts** (recommended if re-importing)
6. Click **Import**
7. Open **Dashboards**, search:

   * `Zeek - Network Security Monitoring & Threat Hunting`

---

## ⚠️ Common Import Notes

### 1) Index Pattern Differences

If your environment uses a different index pattern than `wazuh-alerts-*`, some visuals might show “No results”.

✅ Fix:

* Open the visualization → update index pattern
* Or create the index pattern your Wazuh uses.

### 2) Field Name Differences

Depending on your Zeek decoder/rule setup, some fields might appear as:

* `srcip` vs `data.srcip`
* `protocol` vs `data.protocol`
* `dstip` vs `data.dstip`

✅ Fix:

* Adjust the visualization field mappings as needed.

---

## ✅ Validation Checklist After Import

After importing:

1. Generate Zeek DNS traffic:

```bash
dig wazuh.com
```

2. Go to Wazuh Dashboard → **Discover**
3. Filter:

* `rule.groups: zeek`

4. Open the dashboard and confirm:

* Network trend graph populates
* DNS / conn / SSL events appear in raw table
* Top talkers populate after some traffic

---

## 🧠 Why This Matters

Instead of only relying on raw logs or individual alerts, this dashboard gives:

- ✅ fast situational awareness
- ✅ real-time hunting visibility
- ✅ analyst-friendly pivots for investigation

It makes Zeek operational in a SOC environment.

---
