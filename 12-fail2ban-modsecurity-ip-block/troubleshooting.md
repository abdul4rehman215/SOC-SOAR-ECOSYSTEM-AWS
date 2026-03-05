# 🚨 Troubleshooting Guide - NGINX + ModSecurity + Fail2Ban + Wazuh SIEM

This guide covers real-world issues encountered during:

- Fail2Ban installation
- Jail configuration
- Regex filter mismatch
- Firewall blocking failures
- Wazuh log ingestion issues
- Decoder and rule problems
- Alert correlation failures
- Production tuning concerns

---

# 1️⃣ Fail2Ban Service Not Starting

## Symptoms

- `systemctl start fail2ban` fails
- Service exits immediately
- Error: configuration error in jail file

## Check Status

```bash
sudo systemctl status fail2ban
````

## Common Causes

* Syntax error in jail file
* Invalid parameter
* Incorrect indentation

## Validate Configuration

```bash
sudo fail2ban-client -d
```

Fix syntax errors before restarting.

---

# 2️⃣ Jail Not Active

## Symptoms

```bash
sudo fail2ban-client status
```

Jail not listed.

## Possible Causes

* Jail file saved in wrong directory
* File extension incorrect
* Service not restarted

## Ensure File Exists

```bash
ls /etc/fail2ban/jail.d/
```

Restart service:

```bash
sudo systemctl restart fail2ban
```

---

# 3️⃣ Fail2Ban Not Matching ModSecurity Logs

## Symptoms

* Attacks detected
* No IP bans occur
* `Currently failed: 0`

## Root Cause

Regex does not match ModSecurity log format.

## Debug with:

```bash
sudo fail2ban-regex /var/log/modsec_audit.log /etc/fail2ban/filter.d/modsecurity.conf
```

If "0 matches":

* Check exact log format
* Adjust regex accordingly

Example alternative pattern:

```ini
failregex = ^.*ModSecurity: Access denied with code 403.*client <HOST>.*$
```

---

# 4️⃣ Wrong Log Path

## Symptoms

Fail2Ban running but no bans triggered.

## Check Log File Exists

```bash
ls -l /var/log/modsec_audit.log
```

If file missing:

* Verify ModSecurity config
* Confirm audit log enabled

In modsecurity.conf:

```ini
SecAuditEngine On
SecAuditLog /var/log/modsec_audit.log
```

Restart NGINX after changes.

---

# 5️⃣ IP Not Appearing in iptables

## Symptoms

Fail2Ban shows banned IP
But firewall not blocking traffic.

## Check Firewall Rules

```bash
sudo iptables -L -n
```

If empty:

* Firewall service may use nftables
* Or firewalld active instead

Check backend:

```bash
sudo update-alternatives --config iptables
```

If using nftables, configure Fail2Ban accordingly.

---

# 6️⃣ Attacker Still Accessing Server After Ban

## Possible Causes

* Reverse proxy in front
* Load balancer IP logged instead of real IP
* Wrong client IP extraction

Solution:

Ensure NGINX is configured with:

```nginx
real_ip_header X-Forwarded-For;
```

And logs correct client IP.

---

# 7️⃣ Wazuh Not Receiving Fail2Ban Logs

## Symptoms

* Ban visible in server
* No alert in Wazuh dashboard

## Check Agent Status

```bash
sudo systemctl status wazuh-agent
```

## Verify ossec.conf Entry

```xml
<localfile>
  <log_format>syslog</log_format>
  <location>/var/log/fail2ban.log</location>
</localfile>
```

Restart agent:

```bash
sudo systemctl restart wazuh-agent
```

---

# 8️⃣ Wazuh Alert Shows Generic Log Only

## Cause

Decoder not configured properly.

Ensure decoder exists:

```xml
<decoder name="fail2ban">
  <program_name>fail2ban</program_name>
</decoder>
```

Restart Wazuh manager.

---

# 9️⃣ Custom Wazuh Rule Not Triggering

## Check Rule ID Conflict

Ensure rule ID not overlapping with existing rules.

Use unique ID range (e.g., 100200+).

Validate rules:

```bash
sudo /var/ossec/bin/ossec-logtest
```

---

# 🔟 Too Many False Positives

## Causes

* maxretry too low
* findtime too short
* Legitimate scanning tools triggering WAF

## Solution

Adjust jail config:

```ini
maxretry = 10
findtime = 600
bantime  = 1800
```

Also whitelist internal IPs:

```ini
ignoreip = 127.0.0.1/8 192.168.1.0/24
```

---

# 1️⃣1️⃣ Permission Denied Reading Logs

Ensure log readable:

```bash
sudo chmod 640 /var/log/modsec_audit.log
sudo chown root:adm /var/log/modsec_audit.log
```

Ensure Fail2Ban user has access.

---

# 1️⃣2️⃣ Fail2Ban Regex Matches But Ban Not Triggering

Check:

```bash
sudo fail2ban-client get modsecurity maxretry
```

Verify threshold met.

Also check:

```bash
sudo fail2ban-client get modsecurity findtime
```

---

# 1️⃣3️⃣ High CPU Usage

Possible reasons:

* CRS paranoia level too high
* Excessive log generation
* Very low ban thresholds

Tune:

* CRS rule exclusions
* Logging verbosity
* Ban parameters

---

# 1️⃣4️⃣ Duplicate Alerts in Wazuh

Cause:

* Multiple log entries for same event
* Both access.log and audit.log monitored

Solution:

* Monitor only required logs
* Tune Wazuh rules

---

# 1️⃣5️⃣ Fail2Ban Not Persisting After Reboot

Ensure enabled:

```bash
sudo systemctl enable fail2ban
```

---

# 1️⃣6️⃣ Ban Not Visible in Dashboard

Check Wazuh Manager logs:

```bash
sudo tail -f /var/ossec/logs/ossec.log
```

Check if decoder loading correctly.

---

# 1️⃣7️⃣ TheHive Not Receiving Alerts

Verify:

* Wazuh integration settings
* Webhook configuration
* Alert forwarding rule

---

# 1️⃣8️⃣ Production Hardening Tips

- ✔ Use HTTPS only
- ✔ Enable rate limiting in NGINX
- ✔ Set CRS paranoia level appropriately
- ✔ Regularly update OWASP CRS
- ✔ Rotate logs properly
- ✔ Use centralized firewall policies
- ✔ Enable log retention policies
- ✔ Monitor ban trends

---

# 1️⃣9️⃣ Debugging Checklist

- ✔ Is NGINX running?
- ✔ Is ModSecurity blocking?
- ✔ Is audit log updating?
- ✔ Does fail2ban-regex match logs?
- ✔ Is jail active?
- ✔ Is firewall rule inserted?
- ✔ Are Wazuh logs ingesting?
- ✔ Are custom rules firing?
- ✔ Are alerts visible in dashboard?

---

# 2️⃣0️⃣ Common Root Causes Summary

Most production issues arise from:

* Wrong log path
* Incorrect regex
* Service not restarted
* Firewall backend mismatch
* Decoder misconfiguration
* Rule ID conflicts
* Permission issues

Always troubleshoot layer by layer.

---

# Final Advice

When debugging:

1. Validate detection.
2. Validate log writing.
3. Validate regex matching.
4. Validate firewall insertion.
5. Validate SIEM ingestion.
6. Validate alert generation.

Never skip layers.

---

End of Troubleshooting Guide.

---
