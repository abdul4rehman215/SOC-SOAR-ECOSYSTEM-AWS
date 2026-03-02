# 🛠 Troubleshooting Guide - Behavior-Based HTTP Anomaly Detection

---

## 🔍 1. Apache Logs Not Appearing in Wazuh

Check:

```bash
sudo tail -f /var/log/apache2/access.log
````

If logs exist but not in dashboard:

* Restart wazuh-agent
* Verify agent registration
* Confirm rule.groups:web assigned

---

## 🔍 2. Anomaly Detector Not Triggering

Possible reasons:

* Insufficient baseline learning time
* Low traffic volume
* Threshold too high
* Shingle size too large

Fix:

* Run historical analysis
* Lower grade threshold
* Increase attack volume

---

## 🔍 3. No Slack Alert Received

Check:

* Monitor is enabled
* Trigger conditions correct
* Slack webhook valid
* Outbound HTTPS allowed

---

## 🔍 4. Confidence Always Low

Causes:

* Not enough historical data
* Detector recently created
* Traffic too inconsistent

Solution:

Allow baseline to stabilize.

---

## 🔍 5. iptables Rule Not Blocking

Verify:

```bash
sudo iptables -L -n --line-numbers
```

Ensure rule appears before ACCEPT rules.

---

## 🔍 6. Apache Still Responding After Block

Possible:

* Wrong IP blocked
* Reverse proxy in front
* Load balancer in use

Verify source IP in logs.

---

## 🔍 7. ModSecurity Not Working

Check:

```bash
sudo apachectl -M | grep security
```

If not enabled:

```bash
sudo a2enmod security2
sudo systemctl restart apache2
```

---

## 🔍 8. Anomaly Grade Fluctuates Too Often

Reason:

Traffic volatility.

Fix:

* Increase shingle size
* Adjust confidence threshold
* Tune interval

---

## 🔍 9. False Positives During Normal Traffic

Solution:

* Expand baseline training window
* Exclude known benign IPs
* Apply data filters

---

## 🔍 10. Case Not Updating in TheHive

Check:

* Required fields completed
* Proper case status transitions
* User permissions
* Service running

---

# Troubleshooting Philosophy

Validate pipeline step-by-step:

1. Log generation
2. Rule assignment
3. Index storage
4. ML detection
5. Alert trigger
6. Notification delivery
7. Investigation
8. Mitigation
9. Verification
10. Case closure

SOC troubleshooting mirrors the incident lifecycle.

---
