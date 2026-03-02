# 🛡️ Wazuh Agent Deployment – Ubuntu 24.04

### Endpoint Security Integration with Wazuh Manager (AWS SOC)

---

## 🎯 Role in SOC Architecture

Wazuh Agent runs on endpoints and performs:

* Log collection
* File Integrity Monitoring (FIM)
* Rootkit detection
* Syscheck monitoring
* Active response
* Vulnerability detection
* Process & port monitoring

Flow:

Ubuntu Endpoint
→ Wazuh Agent
→ Wazuh Manager
→ Wazuh Indexer
→ Wazuh Dashboard
→ SOC Analyst

The agent is the data collection layer of the SOC.

---

# 🧱 Infrastructure Context

* Endpoint OS: Ubuntu 24.04 LTS
* Wazuh Manager: AWS EC2
* Communication Port: 1514/TCP
* Enrollment: authd enabled
* Encryption: AES

---

# 🚀 Step 1 – Deploy Agent from Wazuh Dashboard

## 📍 In Wazuh Dashboard

1. Login to Wazuh Dashboard
2. Navigate to:
   → ☰ Menu
   → Agents Management
   → Summary
3. Click: **Deploy new agent**
4. Select:

   * Operating system: Linux
   * Package: .deb (amd64)
   * Server address: WAZUH_SERVER_IP
   * Agent name: ubuntu-client01
   * Group: default
5. Click **Generate installation command**
6. Copy the command

---

# 💻 Step 2 – Install on Ubuntu Endpoint

Paste the generated command on the endpoint terminal.

This typically includes:

```bash
curl -so wazuh-agent.deb https://packages.wazuh.com/...
sudo WAZUH_MANAGER='WAZUH_SERVER_IP' dpkg -i wazuh-agent.deb
```

Then enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable wazuh-agent
sudo systemctl start wazuh-agent
```

---

# ✅ Step 3 – Verify Agent Connection

On Dashboard:

Agents → Summary

Agent status should show:

🟢 Active

On endpoint:

```bash
sudo systemctl status wazuh-agent
```

---

# ⚙ Step 4 – Apply Standard Agent Configuration

After installation, replace default config with my standard `agent.conf`.

Location:

```bash
sudo nano /var/ossec/etc/ossec.conf
```

Replace with provided configuration file (agent.conf).

Then restart:

```bash
sudo systemctl restart wazuh-agent
```

---

# 📊 Step 5 – Verify Monitoring is Working

In Dashboard:

* Check FIM alerts
* Check syscheck events
* Check rootcheck results
* Check log collection events

---

# 📘 Official Documentation References

[Wazuh Agent Installation Guide](documentation.wazuh.com/current/installation-guide/wazuh-agent/index.html)

[Linux Agent Package Installation](documentation.wazuh.com/current/installation-guide/wazuh-agent/wazuh-agent-package-linux.html)

---

# 🏁 Result

- ✔ Agent installed
- ✔ Enrollment successful
- ✔ Agent visible in dashboard
- ✔ FIM enabled
- ✔ Rootcheck enabled
- ✔ Log collection active

The endpoint is now fully integrated into the SOC.

---
