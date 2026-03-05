# 🛠 Troubleshooting Guide - Real SSH Brute Force Incident Response

---

## 🔍 1. SSH Events Not Appearing in Wazuh

Check:

```bash
sudo tail -f /var/log/auth.log
````

If no logs:

* SSH service may not be running
* Firewall blocking connections
* Wrong target IP used

---

## 🔍 2. Alert Triggered but Not Visible in TheHive

Check:

* Wazuh → TheHive integration configuration
* API key validity
* TheHive service status

Verify:

```bash
systemctl status thehive
```

---

## 🔍 3. Mitigation Did Not Stop Attempts

Verify iptables rule:

```bash
sudo iptables -L -n --line-numbers
```

Ensure DROP rule is above ACCEPT rules.

---

## 🔍 4. Fail2Ban Not Banning IPs

Check:

```bash
sudo systemctl status fail2ban
sudo fail2ban-client status
```

Ensure SSH jail is active.

---

## 🔍 5. SSH Configuration Changes Not Applied

After editing:

```bash
sudo systemctl restart ssh
```

Confirm:

```bash
sudo systemctl status ssh
```

---

## 🔍 6. MISP Event Not Visible After Creation

Ensure:

* Event is Published
* Distribution set correctly
* Attribute properly added
* No validation errors

---

## 🔍 7. Slack Alert Not Received

Check:

* Webhook validity
* Slack channel permissions
* Outbound HTTPS access
* Webhook not revoked

---

## 🔍 8. Case Not Updating Properly in TheHive

Check:

* Correct case status transitions
* Observable properly added
* Required fields filled
* User permissions

---

## 🔍 9. Incorrect MITRE Mapping

Ensure:

Technique ID: T1110
Tactic: Credential Access

Verify correct tagging in both TheHive and MISP.

---

## 🔍 10. IOC Sharing Failed

Check:

* MISP API access
* User permissions
* Event publication status
* Attribute type correctly set (ip-src)

---

# Final Troubleshooting Principle

Always validate the incident pipeline in order:

1. Log generation
2. Detection rule trigger
3. Alert forwarding
4. Case creation
5. Investigation validation
6. Mitigation applied
7. Documentation completed
8. Intelligence shared

SOC troubleshooting follows the same sequence as incident handling.

--- 
