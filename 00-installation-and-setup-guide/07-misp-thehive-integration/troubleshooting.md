# 🛠 Troubleshooting Guide - MISP ↔ TheHive Integration 

---

# 🔍 1️⃣ Test Connection Fails in TheHive

### ❌ Error:

Test server connection fails after entering API key.

---

## ✅ Possible Causes & Fixes

### 🔐 1. Invalid API Key

**Cause:**

* API key copied incorrectly
* Key expired
* Wrong user

**Fix:**

1. Go to MISP
   → Administration → List Auth Keys
2. Regenerate a new key
3. Update it in TheHive
4. Click **Test server connection**

---

### 🌐 2. Wrong Server URL

**Cause:**

* HTTP instead of HTTPS
* Wrong IP
* Missing port
* DNS issue

**Fix:**
Verify:

```
https://YOUR_MISP_IP
```

Try accessing it in browser from TheHive server.

---

### 🔥 3. Firewall Blocking Connection

**Cause:**

* Port 443 blocked
* Security group misconfigured

**Fix:**

* Allow inbound 443 on MISP
* Allow outbound HTTPS from TheHive
* Check AWS Security Groups

---

### 🔒 4. SSL Certificate Error

**Cause:**

* Self-signed certificate
* Untrusted CA

**Fix (Lab only):**
Enable in TheHive:

* Disable certificate authority check
* Disable hostname verification

⚠️ Not recommended in production.

---

# 🔁 2️⃣ MISP Events Not Importing

### ❌ Problem:

Connector shows OK but no alerts appear.

---

## ✅ Check the Following

### ⏱ Polling Interval

Go to:

Platform Management → Connectors → MISP

Ensure interval is not too high.

---

### 🏷 Filter Settings Too Restrictive

Check:

* Maximum age
* Allowed tags list
* Prohibited tags
* Organization filters

**Common mistake:**
Allowed tags list defined but MISP events don’t contain those tags.

---

### 📅 Maximum Age Filter

If set to:

```
Maximum age: 1 day
```

Older MISP events won’t import.

Try increasing it.

---

### 🏢 Organization Restriction

If specific org selected:

Only that org’s events will import.

Ensure correct org selected.

---

# 📤 3️⃣ Case Export to MISP Fails

### ❌ Error:

Export button visible but export fails.

---

## ✅ Possible Reasons

### 🔐 Read-Only API Key

If "Read Only" was checked when generating key in MISP:

Export will fail.

**Fix:**
Create new key without read-only restriction.

---

### 👤 Insufficient User Permissions in MISP

The integration user must have:

* Event creation permissions
* Attribute creation permissions

Check MISP role settings.

---

### 🌍 Network Issue

Verify:

* TheHive can reach MISP
* Firewall not blocking outbound request

---

# 🔎 4️⃣ Observables Not Enriching

### ❌ Problem:

Observable added but no MISP correlation shown.

---

## ✅ Troubleshooting Steps

### 🔑 Verify Import Mode

If connector is set to:

```
Export only
```

Enrichment will not work.

Use:

```
Import & Export
```

---

### 🧪 Check Observable Type

Ensure observable type matches MISP attribute type:

| TheHive Observable | MISP Attribute  |
| ------------------ | --------------- |
| IP                 | ip-dst / ip-src |
| Domain             | domain          |
| Hash               | md5 / sha256    |

Mismatch may prevent correlation.

---

### 🏷 Tags Filtering Blocking Match

If prohibited tag list includes:

```
tlp:white
```

And MISP event contains that tag — enrichment may fail.

Review filter settings.

---

# 🧱 5️⃣ Too Many Alerts (Alert Flood)

### ❌ Problem:

Hundreds of MISP alerts flooding TheHive.

---

## ✅ Solution

Adjust:

### Filter Settings

* Set maximum age
* Limit maximum attributes
* Use allowed tags
* Exclude noisy organizations

---

### Example Good SOC Setup

| Setting        | Recommended |
| -------------- | ----------- |
| Maximum age    | 7 days      |
| Allowed tags   | tlp:amber   |
| Max attributes | 200         |

---

# 🐢 6️⃣ Performance Issues

### ❌ Symptoms:

* TheHive slow
* Alerts take long to load
* UI lagging

---

## ✅ Causes

* Large MISP events (1000+ attributes)
* Too frequent polling
* No filtering

---

## ✅ Fix

* Reduce polling frequency
* Limit maximum attributes
* Increase server resources
* Filter old events

---

# 🔄 7️⃣ API Key Expired

### ❌ Symptoms:

* Previously working
* Suddenly fails
* Test connection fails

---

## ✅ Fix

1. Generate new API key in MISP
2. Update connector in TheHive
3. Test connection
4. Save

---

# 🧾 8️⃣ How to Verify Integration is Working

### Check 1:

Test server connection → Success

### Check 2:

New MISP event → Appears in Alerts

### Check 3:

Observable added → Shows correlation

### Check 4:

Export case → New MISP event created

---

# 🔐 9️⃣ Security Hardening Issues

### ❌ Using Self-Signed Certificates in Production

**Risk:**
MITM attacks possible.

**Fix:**
Use valid CA-signed certificate.

---

### ❌ API Key Stored Insecurely

**Risk:**
Credential leakage.

**Fix:**

* Restrict access
* Rotate regularly
* Limit IP access in MISP

---

# 🧠 1️⃣0️⃣ Common Beginner Mistakes

| Mistake                  | Impact             |
| ------------------------ | ------------------ |
| Using admin API key      | Security risk      |
| Import only mode enabled | No export possible |
| Wrong URL format         | Connection fails   |
| Read-only API key        | Export fails       |
| Over-restrictive filters | No alerts imported |
| No filtering             | Alert flood        |

---

# 🏁 Final Troubleshooting Checklist

Before escalation, verify:

- ✔ API key valid
- ✔ HTTPS working
- ✔ Correct URL
- ✔ Proper permissions
- ✔ Filters configured correctly
- ✔ Polling interval reasonable
- ✔ Firewall not blocking
- ✔ Certificate trusted

---

# 📊 When to Escalate

Escalate if:

* Connector logs show repeated 500 errors
* MISP server unstable
* Java truststore SSL issue
* Database performance issue

---

# 🎯 Summary

Most integration issues fall into:

1. API key problems
2. Network/firewall restrictions
3. Filtering misconfiguration
4. Permission errors
5. SSL certificate issues

Systematic troubleshooting solves 95% of issues.

---

# 🚀 SOC Tip

In production:

* Start with Import only
* Validate alert quality
* Tune filters
* Then enable Export
* Monitor performance
* Document API key rotation policy

---
