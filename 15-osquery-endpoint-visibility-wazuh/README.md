# 🖥️ Osquery Exploration and Endpoint Visibility using Wazuh SIEM

<p align="center">
<img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/osquery%20logo.png" width="180">
&nbsp;&nbsp;&nbsp;&nbsp;
<img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/wazuh.png" width="180">
</p>

---

# 📌 Project Overview

Modern **Security Operations Centers (SOC)** require deep visibility into endpoint activity in order to detect suspicious behavior, investigate incidents, and perform threat hunting.

Traditional monitoring methods depend heavily on **system logs generated after events occur**. While logs are useful, they often provide **limited insight into the real-time state of a system**.

This project explores **Osquery**, an open-source endpoint instrumentation framework that turns an operating system into a **queryable relational database**.

Instead of manually checking multiple tools like:

- `ps`
- `netstat`
- `who`
- `lsof`
- `crontab`

Osquery allows analysts to run **SQL queries directly against system telemetry**.

This enables security teams to inspect:

- running processes
- network connections
- open ports
- installed packages
- scheduled tasks
- logged-in users
- kernel modules
- system configuration

To make this telemetry actionable for security monitoring, Osquery was **integrated with Wazuh SIEM** in the SOC ecosystem.

Through this integration:

- Endpoint telemetry becomes centralized
- Security events can trigger alerts
- Data becomes searchable inside SIEM dashboards
- Analysts gain deeper endpoint visibility for threat hunting

This project demonstrates **how Osquery can enhance endpoint monitoring inside a cloud-based SOC environment**.

---

# 🏗️ Architecture Diagram

<p align="center">
<img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/Osquery%2C%20Wazuh%2C%20and%20TheHive%20integration%20diagram.png">
</p>

---

# 🎯 Objective of the Project

The objective of this project was to:

1. Explore how **Osquery exposes system telemetry using SQL queries**
2. Understand how Osquery can be used for **security investigations**
3. Deploy Osquery on an endpoint system
4. Query endpoint telemetry through the Osquery CLI
5. Configure scheduled monitoring queries
6. Generate structured telemetry logs
7. Integrate Osquery logs with **Wazuh SIEM**
8. Parse and visualize telemetry in the **Wazuh dashboard**
9. Enable centralized monitoring of endpoint behavior

---

# 🔎 What is Osquery?

Osquery is an open-source operating system instrumentation framework originally developed by Facebook (Meta).

It exposes operating system data as **virtual SQL tables**, allowing analysts to query system information using SQL syntax.

Instead of using multiple Linux commands, analysts can query system data like this:

```

SELECT * FROM processes;

```

Osquery provides access to hundreds of system data sources including:

- running processes
- open network sockets
- installed packages
- system users
- kernel modules
- file integrity changes
- cron jobs
- hardware configuration

Because of this approach, Osquery is widely used for:

- incident response
- threat hunting
- digital forensics
- compliance monitoring
- endpoint visibility

---

# ⚙️ Key Features of Osquery

Osquery provides several advantages for endpoint monitoring.

### 🧠 SQL-Based Monitoring

Security teams can query system state using familiar SQL syntax.

### 🌍 Cross Platform

Osquery works across:

- Linux
- Windows
- macOS

### 👁️ Real-Time System Visibility

Provides insight into system activity beyond traditional logs.

### 📊 Structured JSON Output

All results are logged in structured JSON format, making them easy to ingest into SIEM tools.

### 🚀 Lightweight and Efficient

Minimal performance impact on monitored systems.

### 🔗 Easily Integrates with SIEM Platforms

Osquery logs can be integrated into platforms like:

- Wazuh
- Elastic
- Splunk

---

# 🔐 Why Integrate Osquery with Wazuh?

Running Osquery locally is useful, but integrating it with **Wazuh SIEM** provides powerful advantages.

Integration enables:

### 📡 Centralized Monitoring

All endpoint telemetry can be collected into the SIEM.

### 🚨 Detection Rules

Wazuh rules can trigger alerts when suspicious telemetry is detected.

### 📣 Alerting

Security alerts can be generated from system state queries.

### 📊 Dashboard Visualization

Telemetry becomes visible in Wazuh dashboards.

### 🕵️ Threat Hunting

SOC analysts can query and analyze endpoint telemetry across systems.

---

# 📚 Official Documentation

The official Wazuh documentation for Osquery integration can be accessed through  
[the official Wazuh Osquery integration documentation](https://documentation.wazuh.com/current/user-manual/capabilities/system-inventory/osquery.html).

This guide explains how the **Osquery Wazuh module works and how telemetry is parsed inside Wazuh**.

---

# 🧪 Lab Environment

The project was performed using the following environment.

| Component | Technology |
|----------|-------------|
| SIEM | Wazuh |
| Endpoint Monitoring | Osquery |
| Operating System | Ubuntu Linux |
| Dashboard | OpenSearch (Wazuh Dashboard) |
| Cloud Infrastructure | AWS EC2 |

---

# 📋 Prerequisites

Before performing this project, the following knowledge areas are recommended.

- Linux command line basics
- Basic SQL syntax
- Understanding of SIEM platforms
- Familiarity with endpoint security monitoring
- Wazuh agent deployment

---

# 📁 Repository Structure

```

15-osquery-endpoint-visibility-wazuh/
│
├── README.md
├── commands.sh
├── architecture.txt
├── interview_qna.md
├── troubleshooting.md
│
├── wazuh-agent/
│   └── snippet-ossec.conf
|
├── configs
│   ├── osquery.conf
│   └── osquery_rules.xml
│
└── docs
    └── Osquery Exploration and Wazuh Integration Project.pdf

```

The detailed PDF documentation with screenshots can be accessed through  
[the complete step-by-step PDF project guide]((https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/15-osquery-endpoint-visibility-wazuh/docs/Osquery%20Exploration%20and%20Wazuh%20Integration%20Project.pdf)).

---

# ⚙️ Implementation Workflow

The project implementation followed a structured workflow.

---

# 🛠️ Step 1 — Installing Osquery

Osquery was installed on the endpoint system using the official package repository.

The repository key was imported and the package was installed through `apt`.

This ensures the latest stable version is installed.

---

# ✅ Step 2 — Verifying Osquery Installation

After installation, the Osquery CLI shell was launched using:

```

osqueryi

```

This interactive shell allows analysts to run SQL queries against system telemetry.

---

# 🔍 Step 3 — Exploring Osquery Schema

The schema command was used to list all available virtual tables.

```

.schema

```

Examples include:

- processes
- users
- listening_ports
- deb_packages
- cron
- kernel_modules

These tables represent system telemetry.

---

# 👤 Step 4 — Querying System Users

```

SELECT * FROM users;

```

### Security Use Case

Helps detect:

- unauthorized accounts
- privilege escalation
- rogue account creation

---

# 🌐 Step 5 — Inspecting Listening Ports

```

SELECT pid, port, protocol, address FROM listening_ports;

```

### Security Use Case

Detect suspicious services or malware listening for connections.

---

# 📦 Step 6 — Inspecting Installed Packages

```

SELECT name, version FROM deb_packages LIMIT 10;

```

### Security Use Case

Helps identify:

- vulnerable software
- unauthorized applications
- outdated packages

---

# 🌍 Step 7 — Inspecting Open Network Connections

```

SELECT pid, local_address, remote_address, remote_port
FROM process_open_sockets;

```

### Security Use Case

Detect:

- suspicious outbound traffic
- lateral movement
- command-and-control connections

---

# ⏰ Step 8 — Inspecting Scheduled Tasks

```

SELECT * FROM crontab;

```

### Security Use Case

Attackers often create cron jobs for persistence.

---

# ⚙️ Step 9 — Configuring Osquery

Configuration files define **scheduled queries and telemetry collection policies**.

### Create the configuration file if not.

```bash
sudo mkdir -p /etc/osquery
sudo nano /etc/osquery/osquery.conf
```

### add configuration:

```json
{
  "options": {
    "config_plugin": "filesystem",
    "logger_plugin": "filesystem",
    "logger_path": "/var/log/osquery",
    "log_result_events": "true",
    "log_status": "true",
    "schedule_splay_percent": "10",
    "utc": "true"
  },

  "schedule": {
    "system_info": {
      "query": "SELECT hostname, cpu_brand, physical_memory FROM system_info;",
      "interval": 3600
    },

    "high_load_average": {
      "query": "SELECT period, average FROM load_average WHERE period = '15m' AND average > '0.7';",
      "interval": 900
    }
  }
}
```

### Purpose:

* Automate telemetry collection
* Run scheduled queries
* Generate JSON logs

---

### Restart Osquery

Restart the Osquery daemon.

```bash
sudo systemctl restart osqueryd
```

Check service status.

```bash
sudo systemctl status osqueryd
```

---

# 📄 Step 10 — Generating Osquery Logs

Osquery writes telemetry results to structured JSON logs located at:

```

/var/log/osquery/osqueryd.results.log

```

View logs.

```bash
sudo tail -f /var/log/osquery/osqueryd.results.log
```

Output will be JSON telemetry.

---

# 🔗 Step 11 — Integrating Osquery with Wazuh

The Wazuh agent configuration was modified to enable the Osquery module.

### Edit the Wazuh agent configuration.

```bash
sudo nano /var/ossec/etc/ossec.conf
```

### Add the Osquery module.

```xml
<wodle name="osquery">
  <disabled>no</disabled>
  <run_daemon>no</run_daemon>
  <log_path>/var/log/osquery/osqueryd.results.log</log_path>
  <config_path>/etc/osquery/osquery.conf</config_path>
  <add_labels>yes</add_labels>
</wodle>
```

### Restart the agent.

```bash
sudo systemctl restart wazuh-agent
```

Once enabled, the agent forwards Osquery telemetry to the Wazuh manager.

---

# 🧠 Step 12 — Configuring Wazuh Rules

Custom Wazuh rules were added to parse Osquery telemetry and convert it into security alerts.

### Create rule file.

```bash
sudo nano /var/ossec/etc/rules/osquery_rules.xml
```

### add rules:

```xml
<group name="osquery">

<rule id="200220" level="1">
  <if_sid>1002</if_sid>
  <decoded_as>json</decoded_as>
  <description>Osquery messages grouped</description>
</rule>

<rule id="200221" level="3">
  <decoded_as>json</decoded_as>
  <field name="name">bpf_socket_events</field>
  <description>Osquery socket event detected</description>
</rule>

</group>
```

### Restart Wazuh manager.

```bash
sudo systemctl restart wazuh-manager
```



---

# 📊 Step 13 — Visualizing Data in Wazuh Dashboard

Osquery telemetry becomes searchable in the Wazuh dashboard.

SOC analysts can view endpoint telemetry through:

- Discover queries
- Security alerts
- Dashboard visualizations

---

# 👨‍💻 Analyst Benefits

By integrating Osquery with Wazuh, SOC analysts gain the ability to monitor:

- running processes
- network connections
- listening ports
- installed software
- scheduled tasks
- system configuration changes

All telemetry becomes **centralized inside the SIEM platform**.

---

# 🧠 Skills Gained

This project helped develop several important SOC engineering skills.

- Endpoint telemetry monitoring
- SQL-based system inspection
- Threat hunting techniques
- SIEM integration
- Log parsing and normalization
- Detection engineering
- SOC investigation workflows

---

# 🌍 Real-World Applications

This integration is commonly used by security teams for:

- endpoint monitoring
- threat hunting
- digital forensics
- incident response
- compliance monitoring

Many enterprise SOC environments use Osquery to gain deeper endpoint visibility.

---

# 🚨 Why This Matters

Traditional logging captures events **after they occur**.

Osquery provides visibility into **the current state of the system**, allowing analysts to investigate systems more effectively.

When combined with Wazuh SIEM, it creates a powerful platform for:

- centralized endpoint monitoring
- threat detection
- incident investigation

---

# 📌 Conclusion

This project demonstrates how Osquery enhances endpoint security monitoring when integrated with Wazuh SIEM.

By combining **SQL-based system telemetry with centralized SIEM monitoring**, SOC teams gain deep visibility into endpoint activity and improve their ability to detect suspicious behavior.

This integration provides a powerful foundation for:

- threat hunting
- incident investigation
- detection engineering
- endpoint security monitoring

---
