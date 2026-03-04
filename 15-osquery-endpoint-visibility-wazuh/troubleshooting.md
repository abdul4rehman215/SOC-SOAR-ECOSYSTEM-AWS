# 🛠️ Troubleshooting Guide — Osquery + Wazuh Integration

This troubleshooting guide covers common issues that may occur during the deployment and integration of **Osquery with Wazuh SIEM**.

The goal is to help security engineers and SOC analysts quickly diagnose and resolve problems encountered during endpoint telemetry monitoring setup.

---

# ⚠️ Issue 1 — Osquery Installation Fails

## Symptoms

During installation, the following errors may appear:

```

E: Unable to locate package osquery

```

or

```

Repository not found

```

---

## Possible Causes

- Osquery repository was not added correctly
- System package lists were not updated
- Network connectivity issues

---

## Diagnostic Commands

Check repository configuration:

```

cat /etc/apt/sources.list

```id="e8odnd"

Check repository connectivity:

```

ping pkg.osquery.io

```id="0fub7s"

---

## Resolution

Re-add the Osquery repository and update package lists.

```

curl -L [https://pkg.osquery.io/deb/pubkey.gpg](https://pkg.osquery.io/deb/pubkey.gpg) | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] [https://pkg.osquery.io/deb](https://pkg.osquery.io/deb) deb main"
sudo apt update
sudo apt install osquery -y

```id="dzxqpr"

---

# ⚠️ Issue 2 — Osquery Interactive Shell Not Launching

## Symptoms

Running the command:

```

osqueryi

```id="1ah6fq"

results in:

```

command not found

```

---

## Possible Causes

- Osquery installation incomplete
- PATH variable not updated
- Binary missing

---

## Diagnostic Commands

Verify installation:

```

which osqueryi

```id="5ptb1l"

Check installed packages:

```

dpkg -l | grep osquery

```id="7m5hff"

---

## Resolution

Reinstall Osquery.

```

sudo apt remove osquery -y
sudo apt install osquery -y

```id="q3rs6p"

---

# ⚠️ Issue 3 — Osquery Service Not Running

## Symptoms

Checking service status shows:

```

sudo systemctl status osqueryd

```

Output:

```

inactive (dead)

```

---

## Possible Causes

- Osquery daemon not started
- Configuration error
- Service crash

---

## Diagnostic Commands

Check service status:

```

sudo systemctl status osqueryd

```id="6btg0k"

Check service logs:

```

journalctl -u osqueryd

```id="xj4y4q"

---

## Resolution

Restart the service.

```

sudo systemctl restart osqueryd

```id="p3owj7"

Enable auto start.

```

sudo systemctl enable osqueryd

```id="2d9e7n"

---

# ⚠️ Issue 4 — Osquery Logs Not Generated

## Symptoms

No logs appear in:

```

/var/log/osquery/osqueryd.results.log

```

---

## Possible Causes

- Scheduled queries not configured
- Logging plugin not enabled
- Incorrect configuration file

---

## Diagnostic Commands

Verify configuration file:

```

cat /etc/osquery/osquery.conf

```id="crd6ik"

Check log directory:

```

ls /var/log/osquery

```id="gczr7o"

---

## Resolution

Ensure the configuration includes logging options.

Example configuration:

```

{
"options": {
"logger_plugin": "filesystem",
"logger_path": "/var/log/osquery",
"log_result_events": "true"
}
}

```id="8b45kn"

Restart Osquery.

```

sudo systemctl restart osqueryd

```id="vsc2r6"

---

# ⚠️ Issue 5 — Wazuh Not Receiving Osquery Logs

## Symptoms

Osquery logs exist but **no events appear in Wazuh dashboard**.

---

## Possible Causes

- Wazuh Osquery module disabled
- Incorrect log path in Wazuh configuration
- Agent service not restarted

---

## Diagnostic Commands

Check Wazuh agent configuration:

```

cat /var/ossec/etc/ossec.conf

```id="x8uv8p"

Search for Osquery module:

```

grep osquery /var/ossec/etc/ossec.conf

```id="v6g7ht"

Check Wazuh logs:

```

sudo tail -f /var/ossec/logs/ossec.log

```id="ynse60"

---

## Resolution

Ensure Osquery module is configured.

```

<wodle name="osquery">
  <disabled>no</disabled>
  <run_daemon>no</run_daemon>
  <log_path>/var/log/osquery/osqueryd.results.log</log_path>
  <config_path>/etc/osquery/osquery.conf</config_path>
  <add_labels>yes</add_labels>
</wodle>
``` id="ffk4t4"

Restart Wazuh agent.

````
sudo systemctl restart wazuh-agent
``` id="w2cpg0"

---

# ⚠️ Issue 6 — Osquery Data Not Appearing in Dashboard

## Symptoms

Events exist in logs but not visible in the **Wazuh Dashboard Discover view**.

---

## Possible Causes

- Index pattern not refreshed
- Incorrect search filter
- Wazuh rules not parsing events

---

## Diagnostic Steps

Open the Wazuh Dashboard and navigate to:

````

Discover

```id="i0zv1o"

Search using the query:

```

rule.groups : osquery

```id="h9o2iw"

---

## Resolution

Refresh the index pattern.

Navigate to:

```

Stack Management → Index Patterns

```

Update the Wazuh index.

---

# ⚠️ Issue 7 — Wazuh Rules Not Triggering

## Symptoms

Osquery logs appear but **no alerts are generated**.

---

## Possible Causes

- Missing rule definitions
- Incorrect rule configuration
- Wazuh manager not restarted

---

## Diagnostic Commands

Check rules directory:

```

ls /var/ossec/etc/rules

```id="1w9hpb"

Inspect rule file:

```

cat /var/ossec/etc/rules/osquery_rules.xml

```id="qk9fx3"

---

## Resolution

Add Osquery rule definitions.

```

<group name="osquery">

<rule id="200220" level="1">
  <if_sid>1002</if_sid>
  <decoded_as>json</decoded_as>
  <description>Osquery messages grouped</description>
</rule>

</group>
``` id="9hszvo"

Restart Wazuh manager.

````
sudo systemctl restart wazuh-manager
``` id="l39o4o"

---

# 🔍 Best Practices for Stable Integration

To maintain a stable Osquery + Wazuh deployment:

- Regularly monitor Osquery logs
- Validate scheduled queries
- Tune detection rules carefully
- Avoid excessive high-frequency queries
- Monitor system resource usage

---

# 📌 Final Notes

When properly configured, Osquery combined with Wazuh provides powerful capabilities for:

- endpoint telemetry monitoring
- threat hunting
- incident investigation
- security analytics

This integration greatly enhances **endpoint visibility within a SOC environment**.

---
