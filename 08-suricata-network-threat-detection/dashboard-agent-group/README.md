# 🧩 Part 3 – SOC Operationalization  
## Suricata Agent Group + Dedicated SOC Dashboard

This section represents the transition from:

Detection Engineering  
→ Operational SOC Deployment  

After implementing:

✔ Suricata IDS  
✔ Wazuh Integration  
✔ Custom Decoders  
✔ Custom Rules  
✔ MITRE Mapping  
✔ Noise Reduction  

We now optimize for:

✔ Scalability  
✔ Structured monitoring  
✔ Faster triage  
✔ Operational clarity  

---

# 🎯 Why Part 3 Matters

In real SOC environments:

- You do not mix endpoint logs with network IDS logs
- You do not manually configure every sensor
- You do not rely on generic dashboards

You build:

- Agent-based policy control
- Dedicated dashboards
- Structured triage workflows
- Scalable monitoring architecture

---

# 🏗️ Architecture Enhancement

Data Flow:

Suricata Sensor  
→ Wazuh Agent  
→ Wazuh Manager  
→ OpenSearch  
→ Dedicated Suricata Dashboard  
→ Analyst Investigation  

---

# 🔹 Step 1 – Create Suricata Agent Group

On Wazuh Manager:

```bash
sudo /var/ossec/bin/agent_groups -a -g Suricata -q
````

Add agent:

```bash
sudo /var/ossec/bin/agent_groups -a -i 002 -g Suricata -q
```

Verify:

```bash
sudo /var/ossec/bin/agent_groups -l
```

---

# 🔹 Step 2 – Apply Group-Level Configuration

Edit:

```
/var/ossec/etc/shared/Suricata/agent.conf
```

Add:

```xml
<agent_config>
  <localfile>
    <log_format>json</log_format>
    <location>/var/log/suricata/eve.json</location>
  </localfile>
</agent_config>
```

Restart:

```bash
sudo systemctl restart wazuh-manager
sudo systemctl restart wazuh-agent
```

Now any agent added to the Suricata group automatically inherits this configuration.

This is scalable architecture.

---

# 📊 Step 3 – Build Dedicated Suricata Dashboard

This dashboard isolates network IDS alerts from endpoint telemetry.

You created the following panels:

1️⃣ Top Suricata Signatures
2️⃣ MITRE Tactic Distribution
3️⃣ MITRE Technique Frequency
4️⃣ Alerts Over Time
5️⃣ Top Source IPs
6️⃣ Alerts by Severity

Dashboard export file:

🔗 **[Suricata Dashboard JSON Export](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/08-suricata-network-threat-detection/dashboard-agent-group/Suricata%20Network%20Threat%20Detection%20Dashboard.ndjson)**

---

# 🧠 SOC Workflow Improvement

Before:

* Mixed logs
* Hard triage
* No attacker ranking
* No MITRE visibility

After:

✔ Dedicated network threat dashboard
✔ Attack spike visibility
✔ Top attacker IP ranking
✔ MITRE lifecycle overview
✔ Faster triage decisions
✔ Structured investigation workflow

---

# ⚡ Analyst Triage Workflow

1. Open Suricata Dashboard
2. Check Alert Trend
3. Identify dominant signature
4. Check Source IP
5. Review MITRE tactic
6. Drill down in Discover
7. Escalate to TheHive

Detection → Visualization → Investigation → Response

---

# 🏆 Operational Benefits

- ✔ Cleaner separation of telemetry
- ✔ Reduced dashboard clutter
- ✔ Scalable agent configuration
- ✔ Faster incident validation
- ✔ Production-style SOC deployment

---

# 🔚 Conclusion

Part 3 transforms this project from:

A detection lab
→ A SOC-operational environment

It demonstrates:

* Structured monitoring
* Scalable configuration
* Dashboard engineering
* Analyst workflow optimization

This reflects real-world SOC operational maturity.

---
