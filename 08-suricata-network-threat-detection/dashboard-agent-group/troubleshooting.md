# 🛠 Suricata SOC Operationalization – Troubleshooting Guide  
## Agent Groups, Dashboard & Scalability Debugging

This document focuses on troubleshooting issues specific to:

- Agent groups
- Shared configuration
- Dashboard visibility
- Index filtering
- SOC triage workflows

Part 3 reflects operational maturity — this section shows real debugging methodology.

---

# 🔹 SECTION 1 — Agent Group Issues

---

## 1️⃣ Agent Not Showing in Suricata Group

### 🔎 Symptoms

- Suricata group created
- Agent not listed under group
- Logs not segregated

### 🧪 Diagnose

```bash
sudo /var/ossec/bin/agent_groups -l
````

### ⚠️ Common Causes

* Wrong agent ID used
* Agent not registered
* Manager restart required

### ✅ Fix

List agents:

```bash id="f7xq8j"
sudo /var/ossec/bin/manage_agents -l
```

Add correct ID:

```bash id="p7wz3k"
sudo /var/ossec/bin/agent_groups -a -i <AGENT_ID> -g Suricata -q
```

Restart manager:

```bash id="mjz92c"
sudo systemctl restart wazuh-manager
```

---

## 2️⃣ Group Configuration Not Applying

### 🔎 Symptoms

* Agent belongs to group
* Suricata logs still not ingested
* agent.conf not taking effect

### 🧪 Diagnose

Verify file exists:

```bash id="rdk6ms"
/var/ossec/etc/shared/Suricata/agent.conf
```

Check syntax correctness.

### ⚠️ Common Causes

* Incorrect XML structure
* Missing <agent_config> root
* Manager not restarted

### ✅ Correct Format

```xml id="m38vle"
<agent_config>
  <localfile>
    <log_format>json</log_format>
    <location>/var/log/suricata/eve.json</location>
  </localfile>
</agent_config>
```

Restart both:

```bash id="5ovm8a"
sudo systemctl restart wazuh-manager
sudo systemctl restart wazuh-agent
```

---

# 🔹 SECTION 2 — Dashboard Issues

---

## 3️⃣ Suricata Dashboard Shows No Data

### 🔎 Symptoms

* Panels empty
* Discover shows alerts
* Dashboard shows zero count

### ⚠️ Common Causes

* Wrong filter applied
* Wrong index pattern
* Incorrect field mapping

### ✅ Fix

Ensure data view is:

```text
wazuh-alerts-*
```

Ensure filter:

```text
rule.groups: suricata
```

Verify alerts exist in Discover first.

---

## 4️⃣ MITRE Panels Not Displaying Data

### 🔎 Symptoms

* Signature panel works
* MITRE tactic/technique panel empty

### ⚠️ Cause

Custom rules missing `<mitre>` block.

### ✅ Fix

Ensure rule contains:

```xml
<mitre>
  <id>T1595</id>
</mitre>
```

Re-index by restarting manager if needed.

---

## 5️⃣ Top Source IP Panel Empty

### 🔎 Symptoms

* Alerts visible
* No IP aggregation

### ⚠️ Cause

Field mismatch.

Correct field should be:

```text
data.src_ip
```

Not:

```text
srcip
```

Always confirm field names in Discover.

---

# 🔹 SECTION 3 — Index & Data Flow Issues

---

## 6️⃣ Alerts Appearing Delayed

### 🔎 Symptoms

* Attack occurs
* Dashboard shows alert after delay

### ⚠️ Causes

* Wazuh indexing delay
* OpenSearch refresh interval
* System resource constraints

### ✅ Validate

Check:

```bash id="g6sj2w"
sudo tail -f /var/ossec/logs/ossec.log
```

Ensure system CPU/memory not overloaded.

---

## 7️⃣ Alerts Visible in Discover but Not in Dashboard

### 🔎 Cause

Dashboard filter mismatch.

### ✅ Fix

Remove all filters temporarily.

Confirm:

```text
rule.groups: suricata
```

Re-add visualizations if necessary.

---

# 🔹 SECTION 4 — Scalability & Policy Issues

---

## 8️⃣ New Suricata Sensor Not Showing Alerts

### 🔎 Diagnose

1. Verify Suricata running
2. Confirm eve.json generating
3. Check Wazuh agent status
4. Confirm agent added to Suricata group
5. Verify group config applied
6. Restart services

### SOC Best Practice

Always troubleshoot bottom-up:

Suricata → Agent → Manager → Index → Dashboard

Never assume dashboard is the problem.

---

# 🔹 SECTION 5 — Real SOC Troubleshooting Approach

---

When facing operational issues:

1. Validate log generation
2. Validate forwarding
3. Validate decoding
4. Validate rule match
5. Validate indexing
6. Validate visualization
7. Validate escalation pipeline

Layered debugging prevents wasted time.

---

# 🔹 SECTION 6 — Common Operational Mistakes

---

✔ Forgetting manager restart after rule change
✔ Using duplicate rule IDs
✔ Incorrect agent ID while grouping
✔ Editing wrong shared folder
✔ Using wrong index pattern
✔ Incorrect field name in visualization
✔ Suppressing too many alerts

---

# 🔹 FINAL TAKEAWAY

This troubleshooting process demonstrates:

* Operational maturity
* Centralized configuration debugging
* Dashboard validation skills
* SOC-grade investigation workflow
* Enterprise scaling awareness

Part 3 proves this project is not just a lab —
It reflects real SOC operational readiness.

---
