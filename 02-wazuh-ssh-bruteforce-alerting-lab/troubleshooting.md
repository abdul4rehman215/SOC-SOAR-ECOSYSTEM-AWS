# 🛠 Troubleshooting Guide - SSH Brute Force Detection & Slack Alerting (Wazuh Lab)

> This document covers common issues encountered during detection engineering, alert configuration, and Slack integration.

---

# 🔍 1️⃣ SSH Events Not Appearing in Wazuh Dashboard

### ❌ Problem
You attempt invalid SSH logins but no events appear in Security Events.

### ✅ Check

On Ubuntu client:

```bash
sudo tail -f /var/log/auth.log
````

Confirm you see:

```
Invalid user fakeuser from <ATTACKER_IP>
```

If not:

* SSH service may not be running
* Attack not reaching correct IP
* Firewall blocking SSH
* Wrong credentials test

---

# 🔍 2️⃣ SSH Events Visible but Monitor Not Triggering

### ❌ Problem

Events appear in dashboard but alert monitor never triggers.

### ✅ Verify Monitor Configuration

Check:

* Index: `wazuh-alerts-*`
* Filter: `rule.id = 100300`
* Severity filter: `rule.level >= 5`
* Group By: `data.srcip`
* Time Window: Last 1 minute
* Threshold: Count > 5

### 🔎 Common Causes

* Threshold too high
* Wrong time window
* Wrong field used for grouping
* Monitor disabled
* Monitor schedule misconfigured

---

# 🔍 3️⃣ Alert Triggers but Slack Receives Nothing

### ❌ Problem

Wazuh shows alert triggered, but Slack channel receives nothing.

### ✅ Verify Slack Channel Setup

In Wazuh:

Alerting → Destinations / Channels

Check:

* Correct Webhook URL pasted
* Test button sends message successfully
* Channel saved properly

### 🔎 Common Issues

* Incorrect webhook URL
* Slack app not authorized
* Slack channel archived
* Webhook revoked
* Outbound firewall blocking HTTPS

---

# 🔍 4️⃣ Slack Test Works but Real Alerts Do Not Send

### ❌ Problem

Manual Slack test works but monitor action doesn’t send alert.

### ✅ Verify Monitor Action

Inside monitor:

* Action type: Per Alert
* Slack channel selected
* Action enabled
* Deduplication configured properly

### 🔎 Common Cause

Trigger condition not actually met during test.

Reduce threshold temporarily for validation:

```
Count > 2
```

Then retest.

---

# 🔍 5️⃣ Too Many Alerts (Noise Problem)

### ❌ Problem

Alert triggers for single login attempts.

### ✅ Fix

* Ensure threshold > 5
* Ensure grouping by data.srcip
* Ensure severity filter applied
* Increase time window precision

This prevents alert fatigue.

---

# 🔍 6️⃣ No SSH Logs Being Generated

### ❌ Problem

Kali attempts SSH but no logs appear.

### ✅ Verify

On Ubuntu:

```bash
sudo systemctl status ssh
```

If not active:

```bash
sudo systemctl start ssh
```

Also check:

* Security Group allows port 22
* Correct private IP used
* Same network or VPC

---

# 🔍 7️⃣ Monitor Not Running Automatically

### ❌ Problem

Monitor created but not executing.

### ✅ Check

* Monitor status is Enabled
* Schedule frequency set to 1 minute
* Correct time field: `@timestamp`

---

# 🔍 8️⃣ Rule ID Not Matching

### ❌ Problem

Filtering by rule.id = 100300 returns nothing.

### ✅ Verify Actual Rule ID

In Security Events:

Click one SSH failure event and confirm:

* rule.id value
* rule.description

Sometimes environments differ slightly.

---

# 🔍 9️⃣ Webhook Security Concern

### ❌ Problem

Webhook URL accidentally exposed.

### ✅ Fix Immediately

* Revoke webhook in Slack
* Generate new webhook
* Update Wazuh channel
* Retest integration

Never store webhook publicly.

---

# 🔍 🔟 Detection Not Triggering During Fast Tests

### ❌ Problem

You ran 10 SSH attempts quickly but monitor didn't trigger.

### Possible Cause

Monitor interval may be longer than your test window.

### ✅ Solution

* Confirm monitor runs every 1 minute
* Wait full minute before checking
* Reduce threshold temporarily for testing

---

# 📊 Tuning Recommendations

In production environments:

* Tune threshold based on baseline login volume
* Monitor false positive rate
* Adjust severity filter
* Consider geo-location enrichment
* Consider IP reputation enrichment

Detection tuning is iterative.

---

# 🧠 Key Troubleshooting Principle

If detection fails, validate in this order:

1️⃣ Logs exist
2️⃣ Events visible in dashboard
3️⃣ Rule filter matches
4️⃣ Monitor condition satisfied
5️⃣ Trigger fires
6️⃣ Action executes
7️⃣ Notification delivered

Follow the pipeline step by step.

---

# 🏁 Final Advice

Most issues occur due to:

* Misconfigured filters
* Incorrect grouping fields
* Threshold tuning errors
* Slack webhook mistakes

Detection engineering requires validation at every layer of the pipeline.

---

# ✅ Troubleshooting Complete
