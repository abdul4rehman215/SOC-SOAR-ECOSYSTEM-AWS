#!/bin/bash
# ============================================================
# DNS Threat Hunting Deployment Script
# Wazuh + DNS-Stats + AlienVault OTX
# ============================================================

# IMPORTANT:
# This script is a structured reference.
# Some steps require manual editing (API keys, config files).
# Run step-by-step — not blindly in production.

# ============================================================
# PART 1 — SYSTEM PREPARATION
# ============================================================

echo "[+] Updating system..."
sudo apt update -y

echo "[+] Installing dependencies..."
sudo apt install -y python3 python3-pip git curl net-tools

# ============================================================
# PART 2 — INSTALL DNS-STATS
# ============================================================

echo "[+] Cloning DNS-Stats repository..."
cd /opt
sudo git clone https://github.com/MarkBaggett/domain_stats.git

cd /opt/domain_stats

echo "[+] Installing DNS-Stats..."
sudo pip3 install .

echo "[+] Creating DNS-Stats data directory..."
sudo mkdir -p /opt/domain-stats-data

echo "[+] Initializing DNS-Stats database..."
domain_stats --init /opt/domain-stats-data

# ============================================================
# PART 3 — START DNS-STATS SERVICE
# ============================================================

echo "[+] Starting DNS-Stats via Gunicorn..."
cd /opt/domain_stats
gunicorn --bind 127.0.0.1:5730 domain_stats.server:config_app\('/opt/domain-stats-data'\) &

sleep 5

echo "[+] Checking listening port..."
sudo ss -lntp | grep 5730

echo "[+] Testing DNS-Stats API..."
curl http://127.0.0.1:5730/google.com

# ============================================================
# PART 4 — CREATE WAZUH DNS-STATS INTEGRATION
# ============================================================

echo "[+] Creating custom DNS-Stats integration script..."

sudo tee /var/ossec/integrations/custom-dnsstats.py > /dev/null << 'EOF'
#!/usr/bin/env python3
import sys
import json
import requests

DNS_STATS_URL = "http://127.0.0.1:5730/"

def main():
    alert = json.loads(sys.stdin.read())
    try:
        domain = alert["data"]["win"]["eventdata"]["queryName"]
    except:
        sys.exit(0)

    try:
        response = requests.get(DNS_STATS_URL + domain)
        data = response.json()
    except:
        sys.exit(0)

    output = {
        "integration": "dnsstat",
        "query": domain,
        "dnsstat": data
    }

    print(json.dumps(output))

if __name__ == "__main__":
    main()
EOF

sudo chown root:wazuh /var/ossec/integrations/custom-dnsstats.py
sudo chmod 750 /var/ossec/integrations/custom-dnsstats.py

# ============================================================
# PART 5 — CREATE DNS-STATS RULES
# ============================================================

echo "[+] Creating DNS-Stats rules..."

sudo tee /var/ossec/etc/rules/local_dnsstats.xml > /dev/null << 'EOF'
<group name="dnsstat,">

  <rule id="101100" level="3">
    <if_sid>61600</if_sid>
    <field name="win.system.eventID">22</field>
    <description>Sysmon - DNS Query Detected</description>
    <group>dns,</group>
  </rule>

  <rule id="101101" level="5">
    <if_sid>101100</if_sid>
    <field name="dnsstat.category">SUSPICIOUS</field>
    <description>DNS Stats - Suspicious Domain</description>
    <group>dnsstat_alert,</group>
  </rule>

  <rule id="101102" level="6">
    <if_sid>101100</if_sid>
    <field name="dnsstat.freq_score">^([0-3]\..*)</field>
    <description>DNS Stats - Low Frequency Domain</description>
    <group>dnsstat_alert,</group>
  </rule>

</group>
EOF

# ============================================================
# PART 6 — CREATE ALIENVAULT OTX INTEGRATION
# ============================================================

echo "[+] Creating AlienVault OTX integration script..."

sudo tee /var/ossec/integrations/custom-alienvault.py > /dev/null << 'EOF'
#!/usr/bin/env python3
import sys
import json
import requests

OTX_API_KEY = "PASTE_YOUR_API_KEY_HERE"
OTX_URL = "https://otx.alienvault.com/api/v1/indicators/domain/"

def main():
    alert = json.loads(sys.stdin.read())
    try:
        domain = alert["data"]["dnsstat"]["query"]
    except:
        sys.exit(0)

    headers = {"X-OTX-API-KEY": OTX_API_KEY}

    try:
        response = requests.get(OTX_URL + domain + "/general", headers=headers)
        data = response.json()
    except:
        sys.exit(0)

    if data.get("pulse_info", {}).get("count", 0) > 0:
        output = {
            "integration": "alienvault",
            "indicator": domain,
            "type": "domain",
            "otx_pulses": data["pulse_info"]["count"],
            "threat": "malicious"
        }
        print(json.dumps(output))

if __name__ == "__main__":
    main()
EOF

sudo chown root:wazuh /var/ossec/integrations/custom-alienvault.py
sudo chmod 750 /var/ossec/integrations/custom-alienvault.py

# ============================================================
# PART 7 — CREATE OTX RULE
# ============================================================

echo "[+] Creating AlienVault detection rule..."

sudo tee /var/ossec/etc/rules/local_otx.xml > /dev/null << 'EOF'
<group name="alienvault,otx_ioc,">

  <rule id="101200" level="12">
    <field name="integration">alienvault</field>
    <description>AlienVault OTX - Indicator(s) Found</description>
    <group>threat_intel,</group>
    <mitre>
      <id>T1036</id>
    </mitre>
  </rule>

</group>
EOF

# ============================================================
# PART 8 — ADD INTEGRATION BLOCKS TO OSSEC.CONF
# ============================================================

echo "[!] Manual Step Required:"
echo "Edit /var/ossec/etc/ossec.conf and add the following blocks:"
echo ""
echo "<integration>"
echo "  <name>custom-dnsstats</name>"
echo "  <rule_id>101100</rule_id>"
echo "  <alert_format>json</alert_format>"
echo "</integration>"
echo ""
echo "<integration>"
echo "  <name>custom-alienvault</name>"
echo "  <group>dnsstat_alert</group>"
echo "  <alert_format>json</alert_format>"
echo "</integration>"

# ============================================================
# PART 9 — RESTART WAZUH
# ============================================================

echo "[+] Restarting Wazuh Manager..."
sudo systemctl restart wazuh-manager

echo "[+] Deployment Complete."
echo "Next steps:"
echo "1. Install Sysmon on Windows endpoint"
echo "2. Ensure Event ID 22 is enabled"
echo "3. Generate DNS queries using Resolve-DnsName"
echo "4. Check Wazuh dashboard for enriched alerts"

# ============================================================
# END OF SCRIPT
# ============================================================
