# 🤖 AI-Driven SOC Alert Triage Automation  
## 🔗 Integrating **Wazuh + n8n + AI Agent (Gemini)** for Intelligent Security Operations

<p align="center">
  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/wazuh.png" alt="Wazuh" width="160" />
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/N8n-logo-new.svg.png" alt="n8n" width="160" />
</p>

This capstone project demonstrates a **production-style SOC automation pipeline** where **Wazuh SIEM alerts** are forwarded into **n8n**, triaged/enriched by an **AI Agent (Google Gemini)**, and delivered to analysts as a **clean, severity-colored, analyst-ready email report**.

It’s a practical SOAR-style workflow focused on:  
✅ **reducing manual triage effort**  
✅ **lowering alert fatigue**  
✅ improving **MTTD/MTTR** via **AI-assisted summarization + decision support**  
✅ delivering **actionable next steps** to SOC analysts in seconds

---

## 📌 Quick Visual Architecture

<p align="center">
  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/AI-powered%20SOC%20alert%20triage%20automation.png" alt="AI-Powered SOC Alert Triage Automation" width="900"/>
</p>

---

## 🧠 What This Project Solves

SOC teams don’t struggle with detection — they struggle with:

- too many alerts
- low context per alert
- repetitive triage work
- slow response decision-making
- cognitive overload → alert fatigue

This automation solves that by:

✅ forwarding **only meaningful alerts** (severity threshold)  
✅ structuring raw alerts into **AI-readable context**  
✅ generating consistent SOC-style triage output  
✅ sending **polished reports** to the SOC analyst  
✅ reducing time-to-triage from minutes → seconds  

---

## 🧩 Architecture Overview (Detection → Decision Support)

### ✅ End-to-End Flow
1. **Wazuh** detects activity → generates JSON alert  
2. **Custom Wazuh integration script** filters (rule.level ≥ threshold) and forwards to **n8n webhook**  
3. **n8n Webhook** receives the alert payload  
4. **Normalize node (JavaScript)** extracts key fields + preserves full alert context  
5. **AI Agent (Gemini)** generates structured triage output (no hallucinations policy enforced)  
6. **Email Formatter node (JavaScript)** builds a clean **HTML SOC report** (severity color badges, tables, sections)  
7. **SMTP (Gmail App Password)** sends the report to the SOC analyst email  
8. Analyst receives: **What happened → Why it matters → What to do next**

---

## 🧰 Tools & Technologies Used

- **Wazuh SIEM/XDR** (alerts, metadata, MITRE mapping, rule severity, agent info)
- **n8n (self-hosted)** (SOAR/orchestration engine, GUI-based workflow building)
- **Google Gemini API** (AI triage + decision support)
- **AWS EC2 (Ubuntu)** (deployment environment)
- **Docker** (n8n deployment)
- **SMTP (Gmail App Password)** (email delivery)
- **JavaScript nodes** (normalization + HTML report building)

---

## 🚀 Why Integrate Wazuh with n8n + AI?

### ⚡ Faster Triage
AI summarizes alerts instantly → less manual log review.

### 🧹 Reduced Alert Fatigue
Only high-severity alerts reach analysts (severity threshold + filtering logic).

### ⏱️ Improved MTTD & MTTR
AI produces: **What happened → Risk → Actions → Next step** quickly and consistently.

### 🧠 Actionable Intelligence
Instead of raw logs, analysts get structured decision-ready output:
- Summary
- Risk assessment (with confidence & FP probability)
- Recommended actions
- Clear next step directive

### 🧩 Practical SOAR Engineering (Not Theory)
This was not “just setup”. It included:
- workflow design, iterative debugging, prompt engineering
- context handling fixes (full JSON ingestion)
- formatting & UX improvements (clean HTML report)
- production-style reliability mindset

---

## ✅ Prerequisites

### ☁️ AWS + Networking
- AWS EC2 instance running **Ubuntu**
- docker installed (for n8n)
- Open ports:
  - **22 (SSH)**
  - **5678 (n8n UI + Webhook)**  
- Public IP is enough (domain is optional)

### 🔑 Accounts/Keys
- **Google Gemini API key**
- Gmail with **2FA enabled** + **App Password**

### 🧠 Required Knowledge
- Basic Linux commands (SSH, apt, systemctl)
- Basic Wazuh concepts (ossec.conf, rule levels)
- Comfort with GUI workflow tools (n8n node chaining)

---

## 🗂️ Repository Structure

```text
20-ai-driven-soc-alert-triage-automation/
├── README.md
├── commands.sh
├── architecture.txt
├── interview_qna.md
├── troubleshooting.md
├── scripts/
│   ├── custom-n8n-ai                 # Wazuh integration script (forward alerts to n8n)
│   ├── normalize_wazuh_alert.js      # JS snippet used in n8n "Normalize" node
│   ├── format_soc_email_report.js    # JS snippet used in n8n email formatter node
│   ├── ai_soc_prompt.txt             # production-grade prompt (strict format + no hallucinations)
│   └── N8N Wazuh Alert Workflow.json # Importable n8n workflow (nodes + prompt + formatter + email flow)
├── configs/
│   └── ossec_integration_block.xml   # ossec.conf integration block snippet
└── docs/
   └── AI-Driven SOC Triage Automation Using Wazuh and n8n.pdf  # Full PDF guide (screenshots + full walkthrough)

````

> 📄 If you prefer a visual, screenshot-based step-by-step walkthrough, open:
> **[Full PDF Implementation Guide](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/20-ai-driven-soc-alert-triage-automation/docs/AI-Driven%20SOC%20Triage%20Automation%20Using%20Wazuh%20and%20n8n.pdf)**

---

## 🧪 Implementation Guide (Step-by-Step)

> This guide is intentionally detailed so a beginner can reproduce the project without missing anything.
> Full command history is also provided in **`commands.sh`**.

---

# 1️⃣ Deploy n8n on AWS (Docker)

## 1.1 Install Docker (Ubuntu)

👉 Refer to:  
**Docker Installation Guide**  
[Open Docker Installation Guide](../../02-docker-installation/README.md)

## 1.2 Run n8n Container (Persistent / Recommended)

```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  --restart unless-stopped \
  n8nio/n8n
```

## 1.3 Access n8n UI

Open:

```text
http://<EC2_PUBLIC_IP>:5678
```

✅ Confirm n8n loads and you can create workflows.

---

# 2️⃣ Create Webhook Trigger (Wazuh Entry Point)

In n8n GUI:

1. Create a new workflow
2. Add node: **Webhook**
3. Method: **POST**
4. Path: `custom-n8n-ai` (or your preferred path)

You will see:

* **Test URL** (works only while listening)
* **Production URL** (works only when workflow is ACTIVE)

✅ For Wazuh production integration, always use **Production URL**:

```text
http://<EC2_PUBLIC_IP>:5678/webhook/custom-n8n-ai
```

---

# 3️⃣ Configure Wazuh → n8n Integration (Wazuh Manager)

## 3.1 Add Custom Integration Script

On Wazuh manager:

```bash
cd /var/ossec/integrations
```

Place the script file:

* **`scripts/custom-n8n-ai`** → copy it into:

  * `/var/ossec/integrations/custom-n8n-ai`

✅ The script:

* filters alerts by severity (`rule.level >= 7`)
* forwards JSON to the n8n webhook
* logs activity in `integrations.log`

> 📌 Script content is provided in: **`scripts/custom-n8n-ai`** (repo file)

## 3.2 Set Script Permissions

```bash
sudo chown root:wazuh /var/ossec/integrations/custom-n8n-ai
sudo chmod 750 /var/ossec/integrations/custom-n8n-ai
```

## 3.3 Add Integration Block in `ossec.conf`

Edit:

```bash
sudo nano /var/ossec/etc/ossec.conf
```

Add (inside `<ossec_config>`):

```xml
<integration>
  <name>custom-n8n-ai</name>
  <hook_url>http://<EC2_PUBLIC_IP>:5678/webhook/custom-n8n-ai</hook_url>
  <level>7</level>
  <alert_format>json</alert_format>
</integration>
```

Restart Wazuh manager:

```bash
sudo systemctl restart wazuh-manager
```

---

# 4️⃣ Validate Wazuh → n8n Connectivity

## 4.1 Watch Wazuh Integration Logs

```bash
tail -f /var/ossec/logs/integrations.log
```

✅ You should see logs showing the script executing and posting to the webhook.

## 4.2 Validate Webhook Receives Alert (n8n)

* In n8n workflow: open execution panel
* Use “Listen for test event” (for test URL) OR activate workflow (for production URL)
* Confirm webhook node receives JSON payload

---

---

# 🔁 Option A — Import the Full n8n Workflow (Fastest)

If you want the **exact same workflow** (nodes, prompt, formatting logic, email structure) without building manually, you can import the included workflow JSON:

✅ **Workflow File:** [`scripts/N8N Wazuh Alert Workflow.json`](scripts/N8N%20Wazuh%20Alert%20Workflow.json)

### ✅ How to Import in n8n
1. Open n8n in your browser:
   - `http://<EC2_PUBLIC_IP>:5678`
2. Click **Workflows** → **Import from File**
3. Select:
   - `N8N Wazuh Alert Workflow.json`
4. The entire workflow will be imported with:
   - Webhook trigger
   - Normalize node
   - AI triage agent prompt (Gemini)
   - Email formatter (HTML report)
   - SMTP email send node

### ⚠️ Important Notes After Import
Even after importing, you must still configure:

✅ **1) Credentials**
- Gemini API credential (Google Gemini / PaLM)
- SMTP credential (Gmail App Password)

✅ **2) Webhook URL**
- Confirm webhook path is still:
  - `/webhook/custom-n8n-ai`

✅ **3) Wazuh Side Integration**
n8n import does NOT configure Wazuh.
You still must do:
- `/var/ossec/integrations/custom-n8n-ai`
- `ossec.conf` integration block (level 7)
- restart Wazuh Manager

---

# 🧱 Option B — Build Manually (Best for Learning)

If you want to learn how the workflow was engineered step-by-step, build it manually:

1) Webhook Trigger Node  
2) Normalize Wazuh Alert (JavaScript)  
3) AI SOC Triage Engine (Gemini)  
4) Format SOC Email Report (JavaScript)  
5) Send SOC Alert Email (SMTP)

✅ All code and prompt content are available in:
- [`scripts/normalize_wazuh_alert.js`](scripts/normalize_wazuh_alert.js)
- [`scripts/ai_soc_prompt.txt`](scripts/ai_soc_prompt.txt)
- [`scripts/format_soc_email_report.js`](scripts/format_soc_email_report.js)

---

# 5️⃣ Build the n8n Workflow (GUI Node Chain)

Final node chain:

1. **Webhook** — receives Wazuh JSON
2. **Normalize Wazuh Alert (JavaScript)** — structures key fields, preserves full context
3. **AI SOC Triage Engine (Gemini)** — generates structured triage report
4. **Format SOC Email Report (JavaScript)** — severity badges + HTML email
5. **Send Email (SMTP)** — sends report to SOC analyst

✅ The JavaScript snippets and AI prompt are included in:

* **`scripts/normalize_wazuh_alert.js`**
* **`scripts/format_soc_email_report.js`**
* **`scripts/ai_soc_prompt.txt`**

---

# 6️⃣ Normalize Alert Node (JavaScript)

In n8n:

* Add node: **Code (JavaScript)** after webhook
* Name it: `Normalize Wazuh Alert`

Paste the code from:

* **[`scripts/normalize_wazuh_alert.js`](scripts/normalize_wazuh_alert.js)**

✅ Why this matters:

* extracts rule/agent/MITRE/source user fields safely
* passes **full raw alert JSON** to AI (major improvement for context quality)

---

# 7️⃣ Configure AI Agent (Gemini) + Prompt Engineering

## 7.1 Add Gemini Credential in n8n

* Create credential for Gemini (Google Generative Language API)
* Store API key securely in n8n credentials
* Choose fast model for triage use:

  * example: `gemini-2.5-flash` (fast + efficient)

## 7.2 Apply the “Strict SOC Analyst Prompt”

In the AI agent node:

* paste the prompt from:

  * **[`scripts/ai_soc_prompt.txt`](scripts/ai_soc_prompt.txt)**

✅ Prompt design goals:

* no hallucinations
* use only provided JSON
* structured output sections
* consistent report quality every time

---

# 8️⃣ Format Email Report (JavaScript → HTML SOC Report)

In n8n:

* Add node: **Code (JavaScript)**
* Name it: `Format SOC Email Report`

Paste the final formatter code from:

* **[`scripts/format_soc_email_report.js`](scripts/format_soc_email_report.js)**

✅ Final improvements included:

* severity color coding
* alert badges (Low/Medium/High/Critical)
* clean overview table (rule id, fired count, MITRE, source ip, username, timestamp)
* proper AI section parsing (Summary, Risk, Actions, Next Step)
* fallback handling when sections are missing

---

# 9️⃣ Configure SMTP Email Delivery (Gmail App Password)

## 9.1 Create Gmail App Password

* Enable **2FA**
* Create **App Password** (e.g., `n8n-automation`)
* Store it securely in n8n SMTP credentials

## 9.2 SMTP Credential Settings

* Host: `smtp.gmail.com`
* Port: `465`
* SSL/TLS: ON
* Username: your Gmail
* Password: Gmail App Password

---

# 🔟 Activate Workflow (Production)

✅ Activate the n8n workflow.

Now Wazuh will forward alerts to:

```text
http://<EC2_PUBLIC_IP>:5678/webhook/custom-n8n-ai
```

---

## ✅ Verification Checklist (End-to-End)

- ✅ Wazuh generates alert with rule level ≥ 7
- ✅ integrations.log shows forwarding attempts
- ✅ n8n webhook receives JSON
- ✅ normalize node structures fields + full context
- ✅ AI node outputs structured SOC triage report
- ✅ formatter builds polished HTML report
- ✅ analyst receives email with:

* Alert overview
* Log details
* AI triage summary
* Risk assessment
* Recommended actions
* Next step directive

---

## 🧠 What I Learned

* AI triage is only reliable with **strict prompt engineering**
* “Partial context” produces weak triage → full JSON improves quality drastically
* Workflow design requires iterative refinement (formatting, missing fields, parsing)
* SOAR value is real when it produces **decision-ready output**, not just forwarding alerts
* Automation reduces fatigue only when filtering, structure, and output quality are engineered properly

---

## 🌍 Why This Matters

Modern SOC operations are limited by:

* speed
* context
* human bandwidth
* alert overload

This project demonstrates how AI + automation can:

* accelerate triage,
* standardize analysis,
* reduce manual effort,
* deliver consistent analyst-ready output,
* and improve response decision-making in real SOC environments.

---

## 🏢 Real-World Applications

* Tier-1 triage automation (15–20 minutes saved per alert)
* High-severity alert routing (email/Slack/Teams/PagerDuty)
* AI-assisted response recommendations aligned to SOC runbooks
* Better MTTR through faster escalation decisions
* Structured reporting for SOC leadership & compliance workflows

---

## ✅ Project Outcome

- ✅ Production-style AI triage engine integrated into SOC ecosystem
- ✅ Automated analyst-ready email reports delivered in seconds
- ✅ Reduced manual review and cognitive load
- ✅ Strong SOAR capability added using open-source tooling (n8n)
- ✅ Practical “Detection → AI → Analyst” pipeline operational in real time

---

## 🔮 Future Enhancements

* Auto-create cases in **TheHive**
* Auto-enrich IOCs with VirusTotal / AbuseIPDB / AlienVault OTX
* Slack / Teams / PagerDuty routing by severity & time-of-day
* Auto-trigger Wazuh Active Response (block IP, isolate host) with human approval gates
* Store triage results in OpenSearch for long-term SOC analytics

---

## 📎 References

* **[Wazuh](https://wazuh.com/)** — SIEM/XDR engine
* **[n8n](https://n8n.io/)** — workflow automation / SOAR layer
* **[Google Gemini API](https://ai.google.dev/)** — AI triage engine

---
