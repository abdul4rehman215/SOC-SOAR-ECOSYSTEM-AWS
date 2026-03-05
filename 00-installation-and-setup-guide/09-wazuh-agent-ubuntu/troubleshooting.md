# 🚨 Troubleshooting Guide - Wazuh Agent

### Ubuntu 24.04 | SOC Endpoint Monitoring

---

## 1️⃣ Agent Not Showing in Dashboard

### Check:

```bash
sudo systemctl status wazuh-agent
```

### Check logs:

```bash
sudo tail -f /var/ossec/logs/ossec.log
```

---

## 2️⃣ Connection Refused

Cause:

* Port 1514 blocked
* Security Group issue
* Incorrect WAZUH_SERVER_IP

Fix:

* Allow TCP 1514 on Manager
* Verify correct IP in config

---

## 3️⃣ Enrollment Failed

Check:

```bash
cat /var/ossec/logs/ossec.log | grep auth
```

Verify:

* authd enabled on manager
* authorization_pass_path correct

---

## 4️⃣ FIM Not Triggering Alerts

Check:

```bash
touch /tmp/testfile
```

Then verify in dashboard.

If no alert:

* Confirm syscheck enabled
* Restart agent

---

## 5️⃣ High CPU Usage on Endpoint

Cause:

* Real-time FIM on large directories

Fix:

* Remove heavy directories
* Adjust max_eps
* Increase synchronization interval

---

## 6️⃣ Agent Stuck in Pending

Fix:

On manager:

```bash
/var/ossec/bin/agent_control -l
```

Delete and re-add if necessary.
