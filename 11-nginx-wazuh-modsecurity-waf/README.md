# 🛡️ Web Application Security Monitoring  
## NGINX 1.24 + ModSecurity v3 (WAF) + OWASP CRS 3.x + Wazuh SIEM

<p align="center">
  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/wazuh-modsecurity-logo.png"/>
</p>

---

## 🎯 Project Vision

This project is not just a setup.

It is about:

- Detection Engineering
- Web Application Layer Monitoring
- WAF Implementation
- SOC Visibility Expansion
- Log-Based Threat Detection
- Real-world Web Attack Simulation
- SIEM Correlation & MITRE Mapping

We are adding a **Layer 7 Web Application Firewall Monitoring Layer** to our SOC ecosystem.

This strengthens our security architecture by protecting and monitoring the web server layer.

---

# 📌 What This Project Achieves

- ✔ Deploy NGINX 1.24 Web Server  
- ✔ Compile and Install ModSecurity v3 (from source)  
- ✔ Integrate OWASP Core Rule Set (CRS 3.x)  
- ✔ Enable Active Blocking Mode  
- ✔ Simulate Real Web Attacks  
- ✔ Analyze Raw WAF Logs  
- ✔ Integrate Logs into Wazuh SIEM  
- ✔ Generate SOC Alerts  
- ✔ Map Alerts to MITRE ATT&CK  
- ✔ Perform SOC-Level Investigation  

---

# 🌍 Why NGINX This Time?

Previously, WAF was implemented with Apache.

This time we move to **NGINX** because:

- NGINX is event-driven and high-performance
- Common in cloud-native environments
- Widely used as reverse proxy and load balancer
- Modern production environments prefer NGINX
- ModSecurity integration requires dynamic module compilation (advanced learning)
- Helps understand WAF engineering deeply

Official NGINX documentation is available through the official NGINX website.

---

# 🔥 What is NGINX?

NGINX is:

- High-performance web server
- Reverse proxy
- Load balancer
- SSL terminator
- API gateway

It is widely used in:

- Cloud platforms
- Kubernetes ingress
- Microservices architecture
- Enterprise web hosting

---

# 🧱 What is ModSecurity v3?

ModSecurity v3 is:

- Open-source Web Application Firewall (WAF)
- HTTP traffic inspection engine
- Rule-based detection system
- Compatible with OWASP CRS

It:

- Detects SQL Injection
- Detects Cross-Site Scripting (XSS)
- Detects LFI / RFI
- Detects Command Injection
- Detects Directory Traversal
- Blocks attacks in real time (403 response)

Official ModSecurity documentation is available on the ModSecurity official website.

---

# 🛡️ What is OWASP CRS?

OWASP Core Rule Set (CRS) is:

- Community-maintained WAF rule set
- Designed to block OWASP Top 10 attacks
- Covers common web attack patterns
- Continuously updated

---

# 📊 Why Integrate With Wazuh?

ModSecurity alone = Blocking + Logging

But no centralized SOC visibility.

Wazuh provides:

- Centralized log collection
- Alert generation
- Severity classification
- MITRE ATT&CK mapping
- Dashboard visualization
- Investigation workflow
- Active Response capabilities (future)

For deeper integration understanding, refer to the official Wazuh ModSecurity integration article available on the Wazuh blog.

---

# 🏗️ Architecture Overview

<p align="center">
  <img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/nginx-modsecurity-wazuh-architecture.png" width="700"/>
</p>

---

## 🔁 Data Flow

Attacker  
→ Malicious HTTP Request  
→ NGINX Web Server  
→ ModSecurity v3 Engine  
→ OWASP CRS Rules  
→ Request Blocked (403)  
→ Logged in error.log  
→ Wazuh Agent Collects  
→ Wazuh Manager Analyzes  
→ Alert Generated  
→ SOC Dashboard Investigation  

---

# 🖥️ Environment

- Ubuntu Server
- NGINX 1.24
- ModSecurity v3 (compiled)
- OWASP CRS 3.x
- Wazuh Agent Installed
- Wazuh Manager Running

---

# 🚀 FULL IMPLEMENTATION GUIDE

---

# 1️⃣ Install NGINX

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl status nginx
````

---

# 2️⃣ Verify NGINX

Open:

```
http://<server-ip>
```

Expected:

Welcome to nginx!

---

# 3️⃣ Install Build Dependencies

```bash
sudo apt install -y \
git gcc make build-essential \
libpcre3 libpcre3-dev \
libssl-dev \
libxml2 libxml2-dev \
libyajl-dev \
liblmdb-dev \
libgeoip-dev \
pkgconf \
libtool \
autoconf \
automake \
curl
```

---

# 4️⃣ Install ModSecurity v3 (Library Mode)

```bash
cd /opt
sudo git clone --depth 1 https://github.com/SpiderLabs/ModSecurity
cd ModSecurity
sudo git submodule init
sudo git submodule update
sudo ./build.sh
sudo ./configure
sudo make
sudo make install
```

---

# 5️⃣ Update Linker

```bash
echo "/usr/local/modsecurity/lib" | sudo tee /etc/ld.so.conf.d/modsecurity.conf
sudo ldconfig
ldconfig -p | grep modsecurity
```

Expected:
libmodsecurity.so

---

# 6️⃣ Clone ModSecurity-NGINX Connector

```bash
cd /opt
sudo git clone https://github.com/SpiderLabs/ModSecurity-nginx.git
```

---

# 7️⃣ Download NGINX Source (Matching Version)

```bash
cd /opt
wget http://nginx.org/download/nginx-1.24.0.tar.gz
tar -xzf nginx-1.24.0.tar.gz
cd nginx-1.24.0
```

---

# 8️⃣ Compile Dynamic Module

```bash
./configure --with-compat \
--add-dynamic-module=../ModSecurity-nginx
make modules
sudo cp objs/ngx_http_modsecurity_module.so /etc/nginx/modules/
```

---

# 9️⃣ Enable Module in nginx.conf

```bash
sudo nano /etc/nginx/nginx.conf
```

Add at top:

```
load_module modules/ngx_http_modsecurity_module.so;
```

---

# 🔟 Configure ModSecurity

```bash
sudo mkdir /etc/nginx/modsec
sudo cp /opt/ModSecurity/modsecurity.conf-recommended \
/etc/nginx/modsec/modsecurity.conf
sudo nano /etc/nginx/modsec/modsecurity.conf
```

Change:

```
SecRuleEngine On
```

---

# 1️⃣1️⃣ Install OWASP CRS

```bash
cd /opt
sudo git clone https://github.com/coreruleset/coreruleset.git
sudo cp -r coreruleset /etc/nginx/modsec/
cd /etc/nginx/modsec/coreruleset
sudo cp crs-setup.conf.example crs-setup.conf
```

Create main config:

```bash
sudo nano /etc/nginx/modsec/main.conf
```

Add:

```
Include /etc/nginx/modsec/modsecurity.conf
Include /etc/nginx/modsec/coreruleset/crs-setup.conf
Include /etc/nginx/modsec/coreruleset/rules/*.conf
```

---

# 1️⃣2️⃣ Attach WAF to Server Block

```bash
sudo nano /etc/nginx/sites-available/default
```

Inside server block:

```
modsecurity on;
modsecurity_rules_file /etc/nginx/modsec/main.conf;
```

---

# 1️⃣3️⃣ Validate Configuration

```bash
sudo nginx -t
sudo systemctl restart nginx
```

---

# 1️⃣4️⃣ Test WAF Protection

```bash
curl "http://<server-ip>/?q=<script>alert(1)</script>"
curl "http://<server-ip>/?file=../../etc/passwd"
```

Expected:
403 Forbidden

---

# 1️⃣5️⃣ Analyze Raw Logs

```bash
sudo tail -f /var/log/nginx/error.log
```

Observe:

* Rule ID
* Attack category
* Severity
* Matched data

---

# 1️⃣6️⃣ Integrate Logs with Wazuh (Wazuh-agent)

Edit:

```bash
sudo nano /var/ossec/etc/ossec.conf
```

Add:

```xml
<localfile>
  <log_format>syslog</log_format>
  <location>/var/log/nginx/error.log</location>
</localfile>

<localfile>
  <log_format>syslog</log_format>
  <location>/var/log/nginx/access.log</location>
</localfile>
```

Restart:

```bash
sudo systemctl restart wazuh-agent
```

---

# 1️⃣7️⃣ Verify Alerts in Wazuh

Go to:

Security Events
Filter by agent

Search:

modsecurity

You will see:

* XSS attempt
* File traversal
* Common web attack
* ModSecurity rejected query

Each alert includes:

* Rule ID
* Severity level
* Source IP
* URL
* MITRE Technique
* Rule description

---

# 🧠 SOC Capabilities Gained

You can now:

* Monitor OWASP Top 10
* Detect web exploitation
* Analyze attack trends
* Track attacker IPs
* Correlate repeated attempts
* Perform forensic analysis
* Create dashboards
* Enable automated blocking (future)

---

# 📦 Repository Structure

```
11-nginx-wazuh-modsecurity-waf/
│
├── README.md
├── commands.sh
├── architecture.txt
├── interview_qna.md
├── troubleshooting.md
├── wazuh-agent/
|   └── snippets-ossec.conf
└── docs/
    └── Nginx - Web Application Firewall (ModSecurity) with Wazuh Monitoring.pdf
```

---

# 🎯 Project Outcome

- ✔ Enterprise-style WAF deployment
- ✔ Advanced NGINX module compilation
- ✔ OWASP CRS enforcement
- ✔ Real attack blocking
- ✔ SOC monitoring enabled
- ✔ SIEM correlation working

---

# 📈 Skills Demonstrated

* NGINX compilation & module integration
* ModSecurity v3 source build
* WAF engineering
* OWASP CRS tuning
* Log ingestion engineering
* SIEM correlation
* Detection analysis
* SOC investigation workflow
* Security troubleshooting

---

# 🏁 Conclusion

This project demonstrates full web application layer protection and monitoring.

NGINX handles traffic.
ModSecurity inspects & blocks malicious payloads.
OWASP CRS detects known attack patterns.
Wazuh converts raw logs into actionable SOC alerts.

This mirrors real enterprise WAF + SIEM architecture used in production SOC environments.

---

# 📄 PDF Guide

For complete visual step-by-step screenshots and terminal walkthrough,
refer to the detailed PDF implementation guide included in the repository resources folder, or click the link below.

👉 [Click here to view the complete PDF walkthrough guide](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/11-nginx-wazuh-modsecurity-waf/docs/Nginx%20-%20Web%20Application%20Firewall%20(ModSecurity)%20with%20Wazuh%20Monitoring.pdf)

---
