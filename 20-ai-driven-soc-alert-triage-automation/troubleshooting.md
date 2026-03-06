# 🛠️ Troubleshooting Guide — AI-Driven SOC Alert Triage Automation (Wazuh + n8n + Gemini)

> This guide covers the most common issues when building an **AI-powered SOC triage pipeline** that forwards Wazuh alerts to **n8n**, runs an **AI triage agent (Gemini)**, and sends a **formatted HTML email report** to a SOC analyst.

✅ Format used: **Problem → Possible Causes → Diagnosis → Resolution → Prevention**

---

## 🧩 Issue 1 — n8n UI is not accessible on `http://<EC2_PUBLIC_IP>:5678`

### ❌ Problem
Browser cannot open the n8n interface.

### 🔍 Possible Causes
- AWS Security Group inbound rule for **5678** missing
- EC2 instance firewall (UFW) blocking port 5678
- n8n container not running / crashed
- Wrong EC2 public IP (changed after stop/start)
- Port binding not mapped correctly in Docker

### 🧪 Diagnosis
```bash
# Check n8n container
docker ps | grep n8n

# Check if port is listening
sudo ss -tulnp | grep 5678

# Check n8n logs
docker logs n8n --tail 100
````

### ✅ Resolution

1. Ensure AWS inbound rule exists:

* TCP **5678** → Your IP (recommended) or `0.0.0.0/0` (testing only)

2. Restart container:

```bash
docker restart n8n
docker ps | grep n8n
docker logs n8n --tail 50
```

3. If UFW is enabled:

```bash
sudo ufw status
sudo ufw allow 5678/tcp
```

### 🛡️ Prevention

* Use an **Elastic IP** if you frequently stop/start EC2.
* Restrict 5678 access to **your IP**.

---

## 🌐 Issue 2 — Wazuh alerts are not reaching the n8n Webhook

### ❌ Problem

Wazuh is generating alerts, but n8n shows **no webhook executions**.

### 🔍 Possible Causes

* Wrong webhook URL (test URL used instead of production)
* Workflow is not active in n8n
* Wazuh integration block missing or incorrect in `ossec.conf`
* Script permissions incorrect (Wazuh cannot execute)
* Severity threshold too high (alerts filtered out)
* Network connectivity issue from Wazuh Manager to n8n URL

### 🧪 Diagnosis

**1) Confirm the workflow is ACTIVE**

* In n8n, ensure workflow toggle is ON (**Active**).

**2) Confirm you used Production URL**

* Production URL format must be:

```text
http://<EC2_PUBLIC_IP>:5678/webhook/custom-n8n-ai
```

⚠️ Do **NOT** use `/webhook-test/` for production.

**3) Check Wazuh integrations log**

```bash
sudo tail -n 200 /var/ossec/logs/integrations.log
```

**4) Confirm your integration block exists**

```bash
sudo grep -n "<integration>" -n /var/ossec/etc/ossec.conf
```

**5) Quick connectivity test**

```bash
curl -i -X POST "http://<EC2_PUBLIC_IP>:5678/webhook/custom-n8n-ai" \
  -H "Content-Type: application/json" \
  -d '{"test":"connectivity"}'
```

### ✅ Resolution

* Ensure `ossec.conf` has correct block:

```xml
<integration>
  <name>custom-n8n-ai</name>
  <hook_url>http://<EC2_PUBLIC_IP>:5678/webhook/custom-n8n-ai</hook_url>
  <level>7</level>
  <alert_format>json</alert_format>
</integration>
```

* Restart Wazuh:

```bash
sudo systemctl restart wazuh-manager
```

* Ensure workflow is Active in n8n.

### 🛡️ Prevention

* Always integrate Wazuh using **production webhook URL**.
* Document webhook path in README and keep it consistent.

---

## 🧨 Issue 3 — “Webhook Test URL confusion” (Events only show during “Listen for test event”)

### ❌ Problem

Webhook works in test mode but stops working later.

### 🔍 Possible Causes

* Using **Test URL** (`/webhook-test/`) in Wazuh integration config
* Workflow not activated

### 🧪 Diagnosis

Check the URL configured in Wazuh:

```bash
sudo grep -n "hook_url" /var/ossec/etc/ossec.conf
```

### ✅ Resolution

Use production URL:

```text
http://<EC2_PUBLIC_IP>:5678/webhook/custom-n8n-ai
```

Activate workflow in n8n.

### 🛡️ Prevention

* Use Test URL only during development.
* Switch to production URL before final deployment.

---

## 🧾 Issue 4 — Wazuh integration script doesn’t execute (no entries in integrations.log)

### ❌ Problem

No forwarding logs appear in `/var/ossec/logs/integrations.log`.

### 🔍 Possible Causes

* Wrong script file name (must match `<name>` in `<integration>`)
* Wrong script location (must be in `/var/ossec/integrations/`)
* Permissions incorrect
* Wazuh manager not restarted after config changes

### 🧪 Diagnosis

```bash
# Check script exists
ls -l /var/ossec/integrations/custom-n8n-ai

# Validate ownership and mode
stat /var/ossec/integrations/custom-n8n-ai

# Check Wazuh service
sudo systemctl status wazuh-manager --no-pager
```

### ✅ Resolution

Fix permissions:

```bash
sudo chown root:wazuh /var/ossec/integrations/custom-n8n-ai
sudo chmod 750 /var/ossec/integrations/custom-n8n-ai
```

Restart Wazuh:

```bash
sudo systemctl restart wazuh-manager
```

### 🛡️ Prevention

* Keep script names consistent.
* Always restart Wazuh after changing `ossec.conf`.

---

## 🧯 Issue 5 — Alerts are forwarded but always filtered out (no AI emails ever sent)

### ❌ Problem

Everything is “working” but no alerts trigger the pipeline.

### 🔍 Possible Causes

* Severity filter too strict:

  * `<level>7</level>` in `ossec.conf`
  * and `rule.level >= 7` in script
* Your test alerts don’t reach severity 7+
* Your environment generates mostly low-level informational alerts

### 🧪 Diagnosis

Check the rule level in the alert JSON (sample):

* In Wazuh dashboard: open alert → verify rule.level
* Or inspect `/var/ossec/logs/alerts/alerts.json` (if enabled):

```bash
sudo tail -n 50 /var/ossec/logs/alerts/alerts.json
```

### ✅ Resolution

Temporarily lower threshold for testing (example: 5):

```xml
<level>5</level>
```

And in script:

```python
if level < 5:
    return ""
```

Then restart Wazuh:

```bash
sudo systemctl restart wazuh-manager
```

### 🛡️ Prevention

* Keep level 7 for production, but test with known high-severity rule events first.

---

## 🔗 Issue 6 — n8n “Referenced node doesn’t exist” / `$items("Normalize Wazuh Alert")` failing

### ❌ Problem

Formatter node throws error: referenced node doesn’t exist.

### 🔍 Possible Causes

* Node renamed in n8n GUI (name mismatch)
* Using `$items("...")` referencing old node name
* Copy/paste mismatch between workflow and script

### 🧪 Diagnosis

* In n8n workflow canvas, confirm exact node name:

  * Example: `Normalize Wazuh Alert`
* Match it exactly (case + spaces).

### ✅ Resolution

Update formatter reference:

```javascript
const alert = $items("Normalize Wazuh Alert")[0].json;
```

### 🛡️ Prevention

* Lock node names before finalizing.
* Use stable names exactly as documented.

---

## 🤖 Issue 7 — AI output is messy, inconsistent, or hallucinating details

### ❌ Problem

AI produces irrelevant content, wrong scenario, inconsistent format, or invented values.

### 🔍 Possible Causes

* Prompt is too loose / missing strict rules
* You are passing partial data (no context)
* The AI agent is configured incorrectly (wrong model or input)
* AI node receiving stringified JSON incorrectly

### 🧪 Diagnosis

* Inspect what the AI node receives (execution data).
* Confirm `full_alert` is present in Normalize output.
* Confirm prompt contains hard rules:

  * Use only JSON
  * No assumptions
  * Format must match

### ✅ Resolution

1. Ensure Normalize node sends full JSON:

```javascript
full_alert: alert
```

2. Ensure prompt uses strict “production SOC analyst” format and includes:

* `ALERT_OVERVIEW`
* `TRIAGE_SUMMARY`
* `RISK_ASSESSMENT`
* `RECOMMENDED_ACTIONS`
* `NEXT_STEP`

3. Avoid “examples” in the prompt (can bias outputs).

### 🛡️ Prevention

* Use strict prompt engineering.
* Pass full context.
* Keep output schema fixed.

---

## 🧾 Issue 8 — AI sections not parsing correctly (Summary/Risk/Actions empty)

### ❌ Problem

Email shows blank sections even though AI node output has content.

### 🔍 Possible Causes

* AI output formatting slightly different than parser expects
* Section headers changed (e.g., “NEXT STEP” vs “NEXT_STEP”)
* Unexpected markdown artifacts in AI output
* Regex parser too strict

### 🧪 Diagnosis

* Print/inspect raw AI output in n8n execution
* Compare section labels with what the formatter extracts

### ✅ Resolution

1. Ensure AI prompt enforces exact section labels.
2. Ensure formatter:

* removes ``` blocks
* removes **bold**
* uses regex tolerant extraction

### 🛡️ Prevention

* Keep section titles stable and uppercase.
* Use strict prompt + validation.

---

## 📧 Issue 9 — Gmail SMTP authentication fails (“Username and Password not accepted”)

### ❌ Problem

Send Email node fails with auth error.

### 🔍 Possible Causes

* Using Gmail password instead of App Password
* 2FA not enabled
* SMTP config wrong (port/SSL)
* “Less secure apps” setting confusion (not applicable for modern Gmail)

### 🧪 Diagnosis

Confirm SMTP settings:

* Host: `smtp.gmail.com`
* Port: `465`
* SSL/TLS: ON
* Password: **App Password** (16 chars)

### ✅ Resolution

1. Enable 2FA → create App Password.
2. Update n8n SMTP credentials with App Password.
3. Use port 465 with SSL.

### 🛡️ Prevention

* Store App Password securely and never commit it to git.
* Use n8n credentials store (not hardcoded).

---

## 📩 Issue 10 — Email is delivered but formatting is broken (quotes, long blocks, ugly layout)

### ❌ Problem

Email is received but layout is messy, unreadable, or too long.

### 🔍 Possible Causes

* HTML formatter not applied (sending plain text)
* AI output includes quotes and markdown artifacts
* Missing severity badge logic
* Email client strips styles due to malformed HTML

### 🧪 Diagnosis

* Verify Send Email node is set to **HTML mode**
* Confirm `{{ $json.html }}` is used, not the raw AI response

### ✅ Resolution

* Ensure Send Email node uses:

  * Subject: `{{ $json.subject }}`
  * HTML: `{{ $json.html }}`
* Ensure formatter cleans AI output:

  * remove ``` blocks
  * remove **

### 🛡️ Prevention

* Always send final output from the formatter node, not AI node directly.
* Keep HTML minimal and email-client friendly.

---

## 🔥 Issue 11 — Duplicate filtering (IF node + script + ossec.conf) causing missed alerts

### ❌ Problem

Alerts are filtered too aggressively and never reach AI.

### 🔍 Possible Causes

* IF node in n8n filtering severity
* AND Wazuh integration `<level>`
* AND integration script level filtering

### 🧪 Diagnosis

* Confirm where filtering happens:

  * Wazuh integration block
  * Wazuh script
  * n8n IF node

### ✅ Resolution

Use one clean design:

* Filtering upstream (Wazuh) is recommended
* Remove redundant IF nodes in n8n once stable

### 🛡️ Prevention

* Avoid duplicated filtering in multiple places.
* Keep logic minimal and maintainable.

---

## 🧯 Issue 12 — n8n container stops after reboot / workflow doesn’t run later

### ❌ Problem

After reboot, n8n isn’t running.

### 🔍 Possible Causes

* container not set to restart automatically
* docker service not enabled
* EC2 restarted, public IP changed (webhook URL breaks)

### 🧪 Diagnosis

```bash
docker ps | grep n8n
sudo systemctl status docker --no-pager
```

### ✅ Resolution

1. Ensure docker starts on boot:

```bash
sudo systemctl enable docker
```

2. Ensure n8n container is restart-enabled:

```bash
docker update --restart unless-stopped n8n
```

3. Use Elastic IP or update webhook URL in Wazuh after IP change:

```bash
sudo nano /var/ossec/etc/ossec.conf
sudo systemctl restart wazuh-manager
```

### 🛡️ Prevention

* Use **Elastic IP** for stability.
* Keep restart policy enabled.

---

## ✅ Quick Recovery Checklist (If Everything Breaks)

### 1) Confirm services running

```bash
sudo systemctl status wazuh-manager --no-pager
docker ps | grep n8n
```

### 2) Confirm Wazuh forwarding log

```bash
sudo tail -n 50 /var/ossec/logs/integrations.log
```

### 3) Confirm n8n webhook reachable

```bash
curl -i -X POST "http://<EC2_PUBLIC_IP>:5678/webhook/custom-n8n-ai" \
  -H "Content-Type: application/json" \
  -d '{"test":"healthcheck"}'
```

### 4) Confirm workflow is Active + node names match

* Webhook active
* Normalize node name matches formatter reference
* Send Email node uses HTML

---
