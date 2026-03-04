# 🛠️ Troubleshooting Guide: Wazuh + Sysmon 

---

## ❌ Issue: Sysmon installed but no logs in Wazuh

### ✅ Check:

1. Event Viewer → Sysmon → Operational
2. Confirm Event ID 1 exists
3. Verify ossec.conf contains:

```
<location>Microsoft-Windows-Sysmon/Operational</location>
```

4. Restart Wazuh Agent

---

## ❌ Issue: Event ID 22 (DNS) not appearing

### Possible Causes:

* DNS logging not enabled in Sysmon config
* Over-filtering in Sysmon XML
* Wazuh rule mismatch

### Fix:

Use minimal DNS config:

```
<DnsQuery onmatch="include">
  <QueryName condition="contains">.</QueryName>
</DnsQuery>
```

Reapply:

```
Sysmon64.exe -c sysmon_config.xml
```

---

## ❌ Issue: Agent not connected

On Manager:

```
/var/ossec/bin/agent_control -l
```

If not active:

* Check firewall ports 1514/1515
* Restart agent

---

## ❌ Issue: Custom rules not triggering

1. Validate XML syntax
2. Run:

```
/var/ossec/bin/wazuh-logtest
```

3. Restart manager:

```
systemctl restart wazuh-manager
```

---

## ❌ Issue: Too many registry alerts

Solution:

* Tune Sysmon registry filters
  OR
* Create Wazuh suppression rule:

```
<rule id="900500" level="0">
  <if_group>sysmon_event13</if_group>
</rule>
```

---

## 🔎 Debugging Workflow Checklist

1. Verify Sysmon logs locally
2. Verify Wazuh agent forwarding
3. Verify manager decoding
4. Verify rule match
5. Verify dashboard index

Never debug only from dashboard.

Always validate from source.

---
