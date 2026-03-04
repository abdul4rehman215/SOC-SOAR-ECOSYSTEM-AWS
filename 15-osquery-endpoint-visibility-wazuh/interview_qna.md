# 🧠 Interview Questions & Answers — Osquery + Wazuh Endpoint Telemetry Monitoring

This section contains interview-style questions related to **Osquery, endpoint telemetry, SIEM integration, and detection engineering** based on the implementation performed in this project.

These questions are commonly discussed in **SOC Analyst, Detection Engineer, and Security Monitoring roles**.

---

# 🔎 Osquery Fundamentals

### Q1: What is Osquery?

Osquery is an open-source endpoint instrumentation and monitoring framework that allows security teams to query operating system data using **SQL queries**.  
It exposes system internals such as processes, network connections, installed software, and user accounts as **virtual SQL tables**.

---

### Q2: How does Osquery collect system information?

Osquery collects system information by mapping operating system APIs to **virtual database tables**.  
Security analysts can run SQL queries against these tables to retrieve real-time system state.

Examples of tables include:

- `processes`
- `users`
- `listening_ports`
- `cron`
- `deb_packages`
- `kernel_modules`

---

### Q3: What is the difference between Osquery logs and traditional system logs?

Traditional logs record **events after they occur**, such as login attempts or application errors.

Osquery provides **real-time system state visibility**, allowing analysts to inspect:

- currently running processes
- open network sockets
- active users
- installed packages
- scheduled tasks

This provides deeper visibility for threat hunting.

---

# ⚙️ Osquery Architecture

### Q4: What are the two main components of Osquery?

Osquery consists of two primary components:

1. **osqueryi**

   Interactive command-line shell used for running SQL queries manually.

2. **osqueryd**

   The background daemon that runs scheduled queries and logs results.

---

### Q5: Where does Osquery store its telemetry logs?

Osquery logs results in JSON format at the following location:

```

/var/log/osquery/osqueryd.results.log

```

These logs can then be ingested into SIEM platforms such as Wazuh.

---

### Q6: What is the purpose of scheduled queries in Osquery?

Scheduled queries allow Osquery to **automatically collect system telemetry at defined intervals**.

This enables continuous monitoring without manual queries.

Example scheduled query:

```

SELECT hostname, cpu_brand, physical_memory FROM system_info;

```

---

# 🔗 Osquery + Wazuh Integration

### Q7: Why integrate Osquery with Wazuh SIEM?

Integrating Osquery with Wazuh enables:

- centralized endpoint monitoring
- telemetry ingestion into SIEM
- detection rule application
- security alert generation
- dashboard visualization

This transforms raw endpoint telemetry into **actionable security intelligence**.

---

### Q8: How does Wazuh collect Osquery telemetry?

Wazuh collects Osquery data through the **Osquery Wodle module** in the Wazuh agent configuration.

The agent reads the Osquery log file and forwards events to the Wazuh manager.

Example configuration:

```

<wodle name="osquery">
  <disabled>no</disabled>
  <run_daemon>no</run_daemon>
  <log_path>/var/log/osquery/osqueryd.results.log</log_path>
  <config_path>/etc/osquery/osquery.conf</config_path>
  <add_labels>yes</add_labels>
</wodle>
```

---

### Q9: What type of data does Wazuh receive from Osquery?

Wazuh receives structured JSON telemetry containing information such as:

* running processes
* open ports
* network connections
* installed software
* system users
* scheduled tasks

This telemetry is then parsed and indexed in OpenSearch.

---

# 🕵️ Threat Hunting with Osquery

### Q10: How can Osquery be used for threat hunting?

Osquery allows analysts to run SQL queries to investigate suspicious system activity.

Examples include:

Detect suspicious processes:

```
SELECT name, pid, path FROM processes;
```

Detect open ports:

```
SELECT pid, port, protocol FROM listening_ports;
```

Detect suspicious cron jobs:

```
SELECT * FROM crontab;
```

---

### Q11: How can Osquery detect suspicious outbound connections?

Analysts can query the `process_open_sockets` table to identify network connections.

Example query:

```
SELECT pid, local_address, remote_address, remote_port
FROM process_open_sockets;
```

This helps detect:

* command-and-control communication
* data exfiltration
* lateral movement

---

# 🛡️ Security Monitoring Use Cases

### Q12: What security use cases does Osquery support?

Osquery supports many security monitoring use cases, including:

* endpoint monitoring
* threat hunting
* incident response
* compliance monitoring
* digital forensics
* vulnerability detection

---

### Q13: How can Osquery help detect persistence mechanisms?

Attackers often create scheduled tasks or cron jobs to maintain persistence.

Analysts can query:

```
SELECT * FROM crontab;
```

to detect unauthorized scheduled tasks.

---

### Q14: How does Osquery help in incident response?

During an incident, analysts can quickly inspect:

* running processes
* network connections
* logged-in users
* active services

This helps determine whether a system has been compromised.

---

# 🚨 Detection Engineering

### Q15: How can Osquery telemetry be used in detection engineering?

Detection engineers can create SIEM rules that trigger alerts when certain telemetry conditions occur.

Examples include:

* unexpected processes running
* suspicious network connections
* unauthorized user accounts
* abnormal system configuration changes

When Osquery telemetry is ingested into Wazuh, rules can automatically detect these behaviors.

---

# 📊 SOC Operations Perspective

### Q16: What benefits does Osquery provide to SOC teams?

Osquery enables SOC teams to:

* gain deep endpoint visibility
* perform proactive threat hunting
* investigate incidents faster
* detect suspicious system activity
* correlate endpoint telemetry with other SIEM alerts

---

### Q17: What are some limitations of Osquery?

Some limitations include:

* requires SQL knowledge
* does not generate alerts on its own
* requires integration with SIEM tools for detection
* poorly written queries can impact performance

---

# 🎯 Key Takeaway

Osquery turns endpoints into **queryable data sources**, while Wazuh transforms that telemetry into **actionable security intelligence**.

Together they enable powerful capabilities for:

* endpoint monitoring
* threat detection
* threat hunting
* incident investigation

---
