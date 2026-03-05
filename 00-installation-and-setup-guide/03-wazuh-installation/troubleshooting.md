# 🛠️ Troubleshooting Guide - Wazuh Installation
### AWS EC2 – Ubuntu 24.04 – All-in-One Deployment

---

# 1️⃣ Dashboard Not Accessible (Port 443 Issue)

## Symptoms
- Browser shows "Connection Refused"
- Timeout error
- HTTPS not reachable

## Root Causes
- Port 443 not allowed in Security Group
- NACL blocking inbound
- Wazuh dashboard service not running
- Firewall (UFW) blocking

## Diagnosis

```bash
sudo systemctl status wazuh-dashboard
sudo ss -tulnp | grep 443
sudo ufw status
````

## Fix

AWS Security Group:

Allow:

* TCP 443 → Your public IP

If UFW enabled:

```bash
sudo ufw allow 443/tcp
sudo ufw reload
```

Restart dashboard:

```bash
sudo systemctl restart wazuh-dashboard
```

---

# 2️⃣ Indexer Service Not Starting

## Symptoms

* wazuh-indexer service fails
* Dashboard shows "Server not ready"
* Port 9200 not listening

## Root Causes

* Low RAM (less than 8GB)
* Disk space exhausted
* OpenSearch heap memory issue
* Corrupted index

## Diagnosis

```bash
sudo systemctl status wazuh-indexer
sudo journalctl -u wazuh-indexer -xe
free -h
df -h
```

## Fix

Minimum requirements:

* 8GB RAM
* 100GB disk

If memory low:

```bash
sudo nano /etc/wazuh-indexer/jvm.options
```

Adjust heap:

```
-Xms2g
-Xmx2g
```

Restart:

```bash
sudo systemctl restart wazuh-indexer
```

---

# 3️⃣ Agents Not Connecting

## Symptoms

* Agent status shows "Never Connected"
* Agent inactive in dashboard
* No logs received

## Root Causes

* Port 1514 blocked
* Port 1515 blocked
* Wrong server IP configured
* Firewall issue

## Diagnosis

On server:

```bash
sudo ss -tulnp | grep 1514
sudo ss -tulnp | grep 1515
```

Check logs:

```bash
sudo tail -f /var/ossec/logs/ossec.log
```

## Fix

AWS Security Group:

Allow:

* TCP 1514
* TCP 1515

Restart manager:

```bash
sudo systemctl restart wazuh-manager
```

---

# 4️⃣ API Not Responding (Port 55000)

## Symptoms

* Dashboard API error
* curl [https://localhost:55000](https://localhost:55000) fails

## Diagnosis

```bash
sudo systemctl status wazuh-manager
sudo ss -tulnp | grep 55000
```

Test API:

```bash
curl -k -u admin:PASSWORD https://localhost:55000
```

## Fix

Ensure:

* Port 55000 allowed
* wazuh-manager running

Restart:

```bash
sudo systemctl restart wazuh-manager
```

---

# 5️⃣ Vulnerability Detection Not Working

## Symptoms

* No vulnerability data in dashboard
* Vulnerabilities tab empty

## Root Causes

* Internet access blocked
* NVD feeds not updating
* Provider misconfiguration

## Diagnosis

Check logs:

```bash
sudo tail -f /var/ossec/logs/ossec.log
```

Search for:

* nvd
* vulnerability

Test internet:

```bash
curl https://nvd.nist.gov
```

## Fix

Ensure:

* Outbound internet allowed
* DNS working
* Correct provider config in ossec.conf

Restart:

```bash
sudo systemctl restart wazuh-manager
```

---

# 6️⃣ File Integrity Monitoring Not Generating Alerts

## Symptoms

* No FIM alerts
* Modifying /etc files produces nothing

## Diagnosis

Modify test file:

```bash
sudo touch /etc/testfile
```

Check logs:

```bash
sudo tail -f /var/ossec/logs/ossec.log
```

## Fix

Ensure:

```xml
<syscheck>
  <disabled>no</disabled>
</syscheck>
```

Restart:

```bash
sudo systemctl restart wazuh-manager
```

---

# 7️⃣ Installation Script Fails

## Symptoms

* GPG error
* Repository not signed
* Key error

## Root Cause

* Network interruption
* DNS issue
* Partial key import

## Fix

Clean:

```bash
sudo rm -f wazuh-install.sh
```

Re-download:

```bash
curl -sO https://packages.wazuh.com/4.14/wazuh-install.sh
sudo bash ./wazuh-install.sh -a
```

---

# 8️⃣ High Memory Usage

## Symptoms

* Server becomes slow
* Swap usage high
* Indexer consuming RAM

## Diagnosis

```bash
free -h
htop
```

## Fix

Upgrade instance to:

* t3.large or higher

Or adjust indexer heap:

```bash
sudo nano /etc/wazuh-indexer/jvm.options
```

---

# 9️⃣ SSL Certificate Warning

## Explanation

Self-signed certificate is generated during installation.

This is normal in lab environment.

For production:

* Replace with valid certificate
* Use reverse proxy

---

# 🔟 Manager Crashes After Editing ossec.conf

## Root Cause

Syntax error in XML

## Diagnosis

Check log:

```bash
sudo tail -n 50 /var/ossec/logs/ossec.log
```

Validate XML:

```bash
xmllint --noout /var/ossec/etc/ossec.conf
```

## Fix

Restore backup:

```bash
sudo cp /var/ossec/etc/ossec.conf.backup /var/ossec/etc/ossec.conf
sudo systemctl restart wazuh-manager
```

---

# 🧠 Best Practices

* Always backup config before editing
* Never edit indexer config without memory check
* Monitor disk usage weekly
* Restrict dashboard to admin IP only
* Do not expose 9200 publicly

---

# ✅ Final Health Check

```bash
systemctl status wazuh-manager
systemctl status wazuh-indexer
systemctl status wazuh-dashboard
systemctl status filebeat
```

Dashboard should load
Agents should connect
Logs should be flowing

SOC core is operational.

---

End of Troubleshooting Guide.

---
