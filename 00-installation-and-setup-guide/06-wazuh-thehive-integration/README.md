# 🔗 Wazuh ↔ TheHive Integration (AWS SOC Deployment)

<div align="center">

 <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/icons/wazuh.png" width="300"/>

 <img src="https://docs.strangebee.com/thehive/images/overview/thehive.svg" width="300"/>

</div>

### SOC-SOAR Ecosystem – Detection to Case Automation

This integration connects:

- **Wazuh (SIEM/XDR)** → Detection Engine  
- **TheHive (IR Platform)** → Case Management  

The result:

> 🚨 Wazuh alerts automatically become structured alerts inside TheHive.

This bridges **Detection → Investigation → Response** in a seamless SOC workflow.

---

# 🧠 Why Integrate Wazuh with TheHive?

Wazuh detects security events.

But a mature SOC requires:

- Case creation
- Task assignment
- Collaboration
- Audit trail
- Investigation workflow

TheHive provides that layer.

When integrated:

✔ Alerts automatically become IR-ready objects  
✔ Analysts avoid manual copying  
✔ Faster MTTR  
✔ Structured incident lifecycle  

---

# 📊 Real SOC Use Case

Example workflow:

1. Wazuh detects suspicious login
2. Integration script triggers
3. TheHive creates an alert
4. Analyst converts alert → case
5. Tasks assigned
6. Observables enriched
7. Case documented & closed

This automation reduces analyst workload significantly.

Official integration reference:  
👉 **[Wazuh Official Integration Guide](https://wazuh.com/blog/using-wazuh-and-thehive-for-threat-protection-and-incident-response/)**

Community script inspiration:  
👉 **[Wazuh2TheHive GitHub Project](https://github.com/crow1011/wazuh2thehive)**

---

# 🖥 Environment Used in This Deployment

| Component | Deployment |
|------------|------------|
| Wazuh | AWS EC2 |
| TheHive | AWS EC2 (t2.xlarge – 4vCPU / 16GB RAM) |
| Integration Method | Custom Python script |
| Transport | REST API |

---

# 📁 Repository Structure

```
00-installation-and-setup-guide/
└── 06-wazuh-thehive-integration/
    ├── README.md
    ├── scripts/
    |   ├── custom-w2thehive.py
    |   └── custom-w2thehive
    ├── commands.sh
    ├── troubleshooting.md
    └── interview_qna.md
```

---

# 🔑 Step 0 – Create TheHive Service Account & API Key (Required)

Before integrating Wazuh with TheHive, we must create:

- A dedicated **Service user**
- A restricted **Analyst profile**
- A secure **API key**

This API key will be used inside `ossec.conf` to authenticate Wazuh with TheHive.

⚠️ Never use the default admin account for integrations.

---

# 🏢 0.1 – Create Custom Analyst Profile (Recommended)

This ensures least-privilege access.

### Navigate:

Sidebar → **Entities Management** → **Profiles**

### Click:
➕ Create Profile

### Configure:

| Field | Value |
|-------|-------|
| Name | `API_Analyst_Access` |
| Type | Organization |

### Assign Required Permissions

Minimum recommended:

- `manageAlert`
- `manageCase`
- `manageObservable`
- `manageTask`
- `manageCaseReport`

⚠️ Do NOT assign org-admin unless necessary.

Click **Confirm**

---

# 👤 0.2 – Create Service User Account

Now create a dedicated service account.

### Navigate:

Sidebar → **Organizations**  
Select your Organization  
Go to **Users** tab  
Click ➕

---

### Fill the form:

| Field | Value |
|--------|--------|
| Type | **Service** |
| Login | `api_analyst@svc.com` |
| Name | API Service Account – Analyst |
| Profile | `analyst` |

Click **Confirm**

---

⚠️ Important Notes:

- Service accounts **cannot login via UI**
- They authenticate only using API key
- Designed specifically for integrations

---

# 🔐 0.3 – Generate API Key

Now generate the key for this service account.

### Steps:

1. Go to **Users**
2. Hover over `api_analyst_svc`
3. Click Edit (✏️)
4. Click **Create API Key**
5. Copy the generated key
6. Store it securely

⚠️ This key acts as a password for API access.

---

# 📌 0.4 – Store API Key Securely

Best practice:

- Store in password manager
- Never commit to GitHub
- Restrict file permissions if saved on server

---

# 📍 0.5 – Where This API Key Will Be Used

It will be used in:

Manual test:

```bash
/var/ossec/integrations/custom-w2thive \
/var/ossec/logs/alerts/alerts.json \
YOUR_API_KEY \
http://THEHIVE_IP:9000
```

And inside:

```
/var/ossec/etc/ossec.conf
```

```xml
<integration>
  <name>custom-w2thive</name>
  <hook_url>http://THEHIVE_IP:9000</hook_url>
  <api_key>YOUR_API_KEY</api_key>
  <alert_format>json</alert_format>
  <level>9</level>
</integration>
```

---

# 🛡 Why Use a Service Account?

✔ Follows least privilege principle  
✔ Isolates integration access  
✔ Prevents misuse of admin credentials  
✔ Can be rotated independently  
✔ Better audit logging  

---

# ✅ Validation Checklist

Before continuing:

- Profile created
- Service user created
- API key generated
- API key copied securely

Now proceed to Step 1.

---

# ⚙️ Step 1 – Install TheHive Python Module (On Wazuh Server)

```bash
sudo /var/ossec/framework/python/bin/pip3 install thehive4py==1.8.1
```

This installs the official TheHive API client.

---

# ⚙️ Step 2 – Create Integration Script

## File Location:

```
/var/ossec/integrations/custom-w2thive.py
```

Use the provided Python script (TheHive 5.5 compatible).

Setting up permissions, ownership and executable:

```bash
sudo chmod 755 /var/ossec/integrations/custom-w2thive.py
sudo chown root:wazuh /var/ossec/integrations/custom-w2thive.py
sudo chmod +x /var/ossec/integrations/custom-w2thive.py
```

---

# ⚙️ Step 3 – Create Bash Wrapper

## File Location:

```
/var/ossec/integrations/custom-w2thive
```

This ensures Wazuh executes the Python integration correctly.

Setting up permissions, ownership and executable:

```bash
sudo chmod 755 /var/ossec/integrations/custom-w2thive
sudo chown root:wazuh /var/ossec/integrations/custom-w2thive
sudo chmod +x /var/ossec/integrations/custom-w2thive
```

---

# 🧪 Step 4 – Manual Integration Test

Run manually:

```bash
/var/ossec/integrations/custom-w2thive \
/var/ossec/logs/alerts/alerts.json \
YOUR_THEHIVE_API_KEY \
http://THEHIVE_IP:9000
```

If no error appears → Integration is working.

---

# ⚙️ Step 5 – Configure ossec.conf

Edit:

```bash
sudo nano /var/ossec/etc/ossec.conf
```

Add:

```xml
<integration>
  <name>custom-w2thive</name>
  <hook_url>http://THEHIVE_IP:9000</hook_url>
  <api_key>YOUR_THEHIVE_API_KEY</api_key> <!--PASTE THE API KEY MADE FROM THEHIVE HERE-->
  <alert_format>json</alert_format>
  <level>9</level>
</integration>
```

You can adjust `<level>` depending on rule severity threshold.

---

# 🔄 Step 6 – Restart Wazuh Manager

```bash
systemctl restart wazuh-manager
```

---

# 🔎 Step 7 – Monitor Logs

Integration logs:

```bash
tail -f /var/ossec/logs/integrations.log
```

Wazuh manager logs:

```bash
tail -f /var/ossec/logs/ossec.log
```

You should see:

```
Create TheHive alert: <alert_id>
```

---

# 📈 Benefits of This Integration

### 1️⃣ Automated Incident Response

Wazuh alerts automatically trigger TheHive actions.

### 2️⃣ Centralized Case Management

All alerts tracked in structured IR platform.

### 3️⃣ Faster Detection-to-Response

No manual alert transfer.

### 4️⃣ Improved Collaboration

Multiple analysts work on cases in real-time.

### 5️⃣ Custom Playbook Capability

Alerts can trigger automated workflows.

---

# 🔐 Security Considerations

- Restrict TheHive API key permissions
- Restrict inbound port 9000
- Use HTTPS in production
- Store API keys securely
- Monitor integration logs regularly

---

# 🏁 Result

✔ Wazuh alerts automatically create TheHive alerts  
✔ Structured IR workflow enabled  
✔ Detection → Case → Response pipeline active  
✔ SOC automation improved  

---

# 🧩 Why This Integration Matters

Without integration:

- SIEM alerts remain isolated
- Analysts manually copy data
- Investigation delays increase

With integration:

Wazuh becomes the **Detection Engine**  
TheHive becomes the **Incident Response Brain**

Together they form a modern SOC backbone.

---

# 🚀 Conclusion

This integration transforms your environment from:

Monitoring Only  
to  
Full Incident Response Lifecycle Automation.

It is one of the most important integrations in any open-source SOC architecture.
