# 🔐 SSH Brute Force Detection & Real-Time Alerting  
### Wazuh + Slack + Kali Linux (SOC Detection Engineering Lab)

> This project simulates a real-world SSH brute force attack and demonstrates how a SOC detects, correlates, and escalates authentication abuse in real time using Wazuh and Slack.
> This is not just tool configuration — it is alert engineering and detection design.

---

# 🎯 Project Objective

To design and validate a SOC-style detection pipeline that:

- Simulates SSH brute force behavior
- Detects repeated authentication failures
- Applies time-based threshold logic
- Groups events by attacker source IP
- Reduces alert noise
- Sends real-time alerts to Slack
- Demonstrates practical blue team monitoring

---

# 🏗 Lab Architecture

| Component | Role |
|------------|------|
| Wazuh Manager | Log analysis & alert engine |
| Ubuntu Client | Victim system (SSH service running) |
| Kali Linux | Attacker machine |
| Slack | Real-time SOC alert channel |

### Detection Flow

Kali → Ubuntu (SSH failures logged)  
Ubuntu → Wazuh Agent → Wazuh Manager  
Wazuh → Monitor Trigger → Slack Notification  

---

# 📊 Detection Engineering Logic

The alert is engineered using:

- Metric: Count of documents  
- Time Window: 1 minute  
- Filter: rule.id = 100300 (SSH invalid user)  
- Severity: rule.level ≥ 5  
- Group By: data.srcip  
- Threshold: Count > 5  

This ensures detection is behavior-based, not event-based.

---

# 🧩 Step-by-Step Implementation

---

## 🖥 Step 1: Validate SSH Log Collection

On the Ubuntu client:

```bash
sudo tail -f /var/log/auth.log
````

From Kali:

```bash
ssh invaliduser@CLIENT_IP
```

Confirm logs appear in `/var/log/auth.log`.

Verify SSH events are visible in:

Wazuh → Security Events
Filter: rule.id:100300

---

# 💬 Step 2: Slack Setup (Full Configuration Guide)

### 2.1 Create Slack App

1. Go to Slack API Portal
2. Click **Create New App**
3. Choose Workspace
4. Name the app: `Wazuh-SOC-Alerts`

---

### 2.2 Enable Incoming Webhooks

1. Open your Slack App
2. Go to **Incoming Webhooks**
3. Enable Incoming Webhooks
4. Click **Add New Webhook to Workspace**
5. Select channel (e.g., `#soc-alerts`)
6. Authorize app
7. Copy generated Webhook URL

⚠ Keep webhook URL confidential.

---

### 2.3 Verify Slack Channel

Ensure:

* Dedicated SOC channel exists
* App is authorized to post messages
* Test message is successfully delivered

---

# 🔔 Step 3: Create Slack Notification Channel in Wazuh

In Wazuh Dashboard:

1. Go to → Alerting → Destinations / Channels
2. Click → Create Channel
3. Select → Slack
4. Paste Webhook URL
5. Click → Test
6. Save

Confirm test message appears in Slack.

---

# 🚨 Step 4: Create SSH Brute Force Detection Monitor

Navigate:

Alerting → Monitors → Create Monitor

Select:

* Per Bucket Monitor
* Visual Editor
* Run Every: 1 minute

---

# 📂 Step 5: Configure Data Source

Set:

* Cluster: Local
* Index: wazuh-alerts-*
* Time Field: @timestamp

---

# 🎯 Step 6: Configure Detection Query

Metric:

* Count of Documents

Time Range:

* Last 1 minute

Filters:

* rule.id = 100300
* rule.level ≥ 5

Group By:

* data.srcip

This groups failures per attacker IP.

---

# ⚡ Step 7: Configure Alert Trigger

Create Trigger:

* Name: SSH Brute Force Alert
* Severity: High
* Condition:
  Count of documents IS ABOVE 5

Meaning:

If more than 5 SSH failures from same IP within 1 minute → trigger alert.

---

# 📢 Step 8: Attach Slack Notification Action

Under Actions:

* Select Slack Channel created earlier
* Action Type: Per Alert
* Enable Deduplication

Save monitor.

---

# 🧪 Step 9: Simulate SSH Brute Force Attack

From Kali:

```bash
for i in {1..10}; do ssh fakeuser@CLIENT_IP; done
```

Ubuntu logs:

```
Invalid user fakeuser from ATTACKER_IP
```

---

# ✅ Step 10: Validate Detection

Check:

Wazuh → Alerting → Alerts

You should see:

* SSH Brute Force Alert
* Attacker IP
* Trigger State: Active

---

# 📲 Step 11: Confirm Slack Alert

Slack channel should display:

* Alert Name
* Severity
* Time Window
* Attacker IP
* Alert Status

This confirms full pipeline.

---

# 📂 Visual Setup Guide (Screenshots Included)

For complete dashboard walkthrough and screenshots:

👉 **[View the full visual project guide (PDF)](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/02-wazuh-ssh-bruteforce-alerting-setup/docs/Wazuh%20Alerting%20Setup%20SSH%20Brute%20Force%20Simulation.pdf)**

---

# 📈 Real-World SOC Use Case

This detection model applies to:

* SSH brute force attacks
* Password spraying
* Credential stuffing
* Bot scanning activity
* Internal reconnaissance attempts

It reflects authentication abuse monitoring used in enterprise SOCs.

---

# 🔐 Why This Detection Design Matters

Without correlation:
Each failed login creates noise.

With correlation:
You detect patterns.

This reduces false positives and alert fatigue.

---

# 🏁 Final Outcome

This lab demonstrates:

* Attack simulation
* Log ingestion
* Detection engineering
* Threshold tuning
* Event correlation
* Real-time SOC notification
* Blue team workflow design

---

# 📚 Skills Demonstrated

* Wazuh alert engineering
* Linux log analysis
* SSH attack detection
* Time-window threshold logic
* Slack webhook integration
* SOC monitoring workflow

---

# 📌 Repository Structure

```
02-wazuh-ssh-bruteforce-alerting-lab/
├── README.md
├── commands.sh
├── architecture-notes.txt
├── interview_qna.md
├── troubleshooting.md
└── Wazuh-Alerting-Setup-SSH-Brute-Force-Simulation.pdf
```

---

# 🔗 Full SOC Platform Setup

For complete ecosystem installation guides:

👉 [View the full SOC installation & integration guide](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/tree/main/00-installation-and-setup-guide)

---

# 🎓 Why This Project Stands Out

Most labs stop at detection.

This project shows:

* Detection design thinking
* Threshold engineering
* Noise reduction strategy
* Pattern-based correlation
* Real-time escalation workflow

This reflects real SOC practice — not just configuration.

---
