# 🔗 MISP ↔ TheHive Integration (GUI-Based SOC Deployment)

<p align="center">
  <img src="https://www.misp-project.org/img/logo.png" width="200">
    <img src="https://docs.strangebee.com/thehive/images/overview/thehive.svg" width="200"/>
</p>

## Threat Intelligence ↔ Incident Response Automation

This integration connects:

* **MISP (Threat Intelligence Platform)**
* **TheHive (Incident Response Platform)**

Result:

> 🧠 Threat intelligence automatically enriches investigations
> 🔄 Cases can export indicators back to MISP
> 📊 SOC gains bidirectional intelligence flow

---

# 🧠 Why Integrate MISP with TheHive?

MISP stores:

* IOCs (IPs, Domains, Hashes)
* TTPs (MITRE ATT&CK)
* Malware intelligence
* Threat actor data
* Community shared intelligence

TheHive manages:

* Alerts
* Cases
* Tasks
* Observables
* Investigation workflow

When integrated:

- ✔ MISP events become alerts in TheHive
- ✔ Observables auto-enrich using threat intel
- ✔ Cases can export IOCs back to MISP
- ✔ Full intelligence lifecycle is enabled

---

# 📊 Real SOC Use Case

Example workflow:

1. SOC receives suspicious alert
2. Observable (IP / Hash) added to case
3. TheHive queries MISP automatically
4. MISP match found → enrichment attached
5. Analyst investigates
6. If confirmed malicious → export case back to MISP
7. Threat shared with community

This creates a **closed intelligence loop**.

---

# 🖥 Environment Used

| Component        | Deployment           |
| ---------------- | -------------------- |
| MISP             | AWS EC2              |
| TheHive          | AWS EC2 (5.5.2-1)    |
| Integration Type | Native GUI Connector |
| Transport        | REST API             |
| Direction        | Import + Export      |

---


# 📂 Repository Structure
```
07-misp-thehive-integration/
├── README.md
├── troubleshooting.md
├── architecture-notes.txt
└── interview_qna.md
```
---

# 🔐 STEP 1 – Generate API Key in MISP (GUI)

TheHive connects to MISP using an API key.

### Login to MISP

Open:

```
https://YOUR_MISP_IP
```

Login as admin or user with API permissions.

---

## 🔑 Create Authentication Key

### Navigate:

Top Menu → **Administration** → **List Auth Keys**

Click:

➕ **Add authentication key**

---

### Fill the form:

| Field       | Value                             |
| ----------- | --------------------------------- |
| User        | Select integration user           |
| Comment     | TheHive Integration               |
| Allowed IPs | (Optional) TheHive server IP      |
| Expiration  | Optional                          |
| Read-only   | Unchecked (for export capability) |

Click **Submit**

---

⚠️ Important:

* The API key will be shown only once
* Copy it immediately
* Store securely
* Never commit to GitHub

---

# 🔗 STEP 2 – Configure MISP Connector in TheHive (GUI)

Now configure inside TheHive.

---

### Login to TheHive

Open:

```
http://THEHIVE_IP:9000
```

Login as admin or user with:

`managePlatform` permission

---

## Navigate to Connector Settings

Sidebar → **Platform Management**

Then:

**Connectors** tab → Select **MISP**

---

## ➕ Add New MISP Server

Click the **+ (Add Server)** button.

A configuration drawer opens.

---

## Fill General Settings

| Field       | Value                 |
| ----------- | --------------------- |
| Server Name | MISP                  |
| Server URL  | https://YOUR_MISP_IP  |
| API Key     | (Paste generated key) |
| Purpose     | Import & Export       |

### Purpose Options Explained:

* **Import only** → Pull MISP events as alerts
* **Export only** → Push case observables to MISP
* **Import & Export** → Full bidirectional integration (Recommended)

---

## Proxy Settings (Optional)

Use only if:

* Corporate proxy exists
* Outbound traffic restricted

Otherwise leave default.

---

## SSL Settings

If using self-signed certificate:

You may enable:

* Disable certificate authority check
* Disable hostname verification

⚠️ Not recommended in production.

---

## Advanced Settings

You can configure:

### Organization Filter

* Include all organizations
* Include selected organizations
* Exclude selected organizations

### Tags

Add tags to imported alerts (example):

`import quality threat intel feeds only`
```
misp-threat-intel
```

---

## Filter Settings (Important for SOC Optimization)

| Option                       | Description               |
| ---------------------------- | ------------------------- |
| Maximum age                  | Only import recent events |
| Organizations to include     | Restrict source org       |
| Maximum number of attributes | Prevent huge events       |
| Allowed tags list            | Import only tagged intel  |
| Prohibited tags              | Exclude noisy feeds       |

This helps reduce alert fatigue.

---

## Test Connection

Click:

**Test server connection**

If successful:

You will see confirmation.

Click:

**Add**

---

# 🔄 STEP 3 – Automatic Import from MISP to TheHive

Once configured:

TheHive will automatically:

* Poll MISP periodically
* Retrieve new events
* Convert events → Alerts

---

## Where to See Imported Events?

Go to:

**Alerts**

You will see:

Type: `misp`

These alerts include:

* Title
* Tags
* Observables
* TTPs
* Source reference

---

# 🔍 Observable Enrichment via MISP

When observables are added to a case:

* TheHive queries MISP
* Matching attributes are attached
* Analyst sees enrichment

Examples:

* IP flagged as malicious
* Hash linked to malware family
* Domain tagged to threat actor

This enables:

✔ Faster triage
✔ Context-driven investigation
✔ Evidence-based decisions

---

# 📤 STEP 4 – Export Case to MISP

The integration is bidirectional.

To export:

1. Open a case
2. Click **Export**
3. Select **Export to MISP**
4. Choose configured server
5. Click **Export**

---

## What Gets Exported?

* Observables marked as IOCs
* Case tags
* Case title
* Optional TheHive case link

This creates a new MISP event.

---

# 🔎 What Happens After Export?

Inside MISP:

* New event created
* Attributes added
* Tags preserved
* Source attribution recorded

You can now:

* Share with community
* Correlate with other events
* Feed into other SOC tools

---

# 🔁 Full Intelligence Lifecycle

Detection → Case → Investigation → IOC → MISP → Community → Back to SOC

This is how modern intelligence-driven SOC operates.

---

# 🧩 Features Enabled by This Integration

### 1️⃣ Automatic Threat Feed Import

MISP events become alerts in TheHive.

---

### 2️⃣ Observable Correlation

Matching IOCs are automatically identified.

---

### 3️⃣ MITRE ATT&CK Mapping

MISP galaxy tags appear inside alerts.

---

### 4️⃣ Bidirectional Intelligence Sharing

Cases exported to MISP improve community defense.

---

### 5️⃣ Reduced Manual Work

No need to:

* Manually copy IOCs
* Switch between tools repeatedly

---

# 🚀 SOC Benefits

| Without Integration | With Integration            |
| ------------------- | --------------------------- |
| Manual enrichment   | Automatic enrichment        |
| Alert isolation     | Threat intelligence context |
| Manual IOC export   | One-click export            |
| Slow investigation  | Faster MTTR                 |
| Disconnected tools  | Unified workflow            |

---

# 🛡 Security Best Practices

* Use dedicated MISP integration user
* Restrict API key by IP
* Use HTTPS
* Rotate API keys periodically
* Monitor connector logs
* Avoid disabling SSL validation in production

---

# 🏁 Result

After successful setup:

✔ MISP events auto-import to TheHive
✔ Observables auto-enrich
✔ Cases export to MISP
✔ Intelligence loop activated
✔ SOC collaboration improved

---

# 🧠 Why This Matters in Modern SOC

Threat intelligence without response is incomplete.

Response without intelligence is blind.

Together:

* MISP becomes the **Threat Intelligence Brain**
* TheHive becomes the **Investigation Engine**

Combined, they form a powerful SOC core.

---

# 📌 Final Architecture View

MISP
↕ REST API
TheHive
↕
Analysts

Bidirectional intelligence pipeline.

---
