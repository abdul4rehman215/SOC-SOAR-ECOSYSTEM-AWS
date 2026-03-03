
# 🚨 Wazuh + VirusTotal Integration – Troubleshooting Guide


## 🧪 FIRST – QUICK VALIDATION CHECKLIST

Before deep troubleshooting, validate:

- ✔ Wazuh Manager running
- ✔ Wazuh Agent running
- ✔ VirusTotal API key correct
- ✔ FIM directory configured
- ✔ Custom rules loaded
- ✔ Active Response block enabled
- ✔ remove-threat.sh executable
- ✔ alerts.json updating

------------------------------------------------------------

Run:

sudo systemctl status wazuh-manager
sudo systemctl status wazuh-agent

------------------------------------------------------------

Check logs:

sudo tail -f /var/ossec/logs/ossec.log

---

## 1️⃣ VIRUSTOTAL LOOKUP NOT WORKING

🔎 Symptoms:
- No data.virustotal fields in alert
- No enrichment visible
- API not triggered

📌 Possible Causes:
- Wrong API key
- Integration block missing
- rule_id mismatch
- Manager not restarted
- Public API limit exceeded

------------------------------------------------------------

✅ Check API key in ossec.conf

File:
 /var/ossec/etc/ossec.conf

Verify:

<integration>
  <name>virustotal</name>
  <api_key>YOUR_API_KEY</api_key>
</integration>

------------------------------------------------------------

✅ Confirm integration script exists:

ls /var/ossec/integrations/

Expected:
virustotal.py

------------------------------------------------------------

✅ Check for API errors:

sudo grep virustotal /var/ossec/logs/ossec.log

Common error:
"Invalid API key"
"Rate limit exceeded"

------------------------------------------------------------

If rate limit exceeded:

- Reduce monitored directories
- Filter only executables
- Upgrade to premium API

---

## 2️⃣ EXECUTABLE FILE NOT TRIGGERING VIRUSTOTAL

🔎 Symptoms:
- File created
- FIM alert generated
- But no VirusTotal enrichment

📌 Root Cause:
Custom rule not matching file extension.

------------------------------------------------------------

✅ Check rule configuration:

/var/ossec/etc/rules/local_rules.xml

Verify regex:

\.(exe|elf|sh|py|js|ps1|bat)$

------------------------------------------------------------

✅ Confirm rule is loaded:

sudo /var/ossec/bin/wazuh-logtest

Paste a sample event and check rule match.

------------------------------------------------------------

If rule not matching:
- Adjust regex
- Restart manager

---

## 3️⃣ CLEAN FILES STILL SHOWING ALERTS

🔎 Symptoms:
- Clean VirusTotal results appear in dashboard

📌 Root Cause:
Suppression rule not working.

------------------------------------------------------------

Check rule:

<rule id="100029" level="0">
  <if_sid>87104</if_sid>
  <field name="data.virustotal.positives">^0$</field>
  <options>no_log</options>
</rule>

------------------------------------------------------------

If still visible:
- Confirm if_sid matches correct SID
- Restart manager
- Verify via wazuh-logtest

---

## 4️⃣ ACTIVE RESPONSE NOT EXECUTING

🔎 Symptoms:
- Malware detected
- No file deletion
- No active response alert

------------------------------------------------------------

📌 Root Causes:

1. active-response block missing
2. rules_id mismatch
3. Script path incorrect
4. Script permission denied
5. JSON parsing error in script

------------------------------------------------------------

✅ Check ossec.conf:

<active-response>
  <command>remove-threat</command>
  <location>local</location>
  <rules_id>87105</rules_id>
</active-response>

------------------------------------------------------------

✅ Check script exists:

ls -lah /var/ossec/active-response/bin/remove-threat.sh

------------------------------------------------------------

✅ Verify permissions:

sudo chmod 750 /var/ossec/active-response/bin/remove-threat.sh
sudo chown root:wazuh /var/ossec/active-response/bin/remove-threat.sh

------------------------------------------------------------

✅ Check active response logs:

cat /var/ossec/logs/active-responses.log

---

## 5️⃣ SCRIPT EXECUTES BUT FILE NOT DELETED

🔎 Symptoms:
- Active response alert generated
- File still present

------------------------------------------------------------

📌 Possible Issues:

- Script not extracting correct JSON field
- Wrong file path
- Permission issue deleting file

------------------------------------------------------------

✅ Confirm script extracts:

parameters.alert.data.virustotal.source.file

------------------------------------------------------------

✅ Test manual deletion:

sudo rm /path/to/file

If permission denied:
- Adjust directory permissions

---

## 6️⃣ DASHBOARD DOES NOT SHOW VIRUSTOTAL FIELDS

🔎 Symptoms:
- Alert visible
- But no enrichment fields

------------------------------------------------------------

Possible causes:

- API call failed
- Alert index refresh needed
- Using wrong filter

------------------------------------------------------------

Filter correctly:

rule.groups: virustotal

Check field:

data.virustotal.positives

---

## 7️⃣ THEHIVE NOT RECEIVING ALERTS

🔎 Symptoms:
- Alert visible in Wazuh
- Not visible in TheHive

------------------------------------------------------------

Check:

- Wazuh → TheHive integration connector
- Webhook configuration
- Authentication key
- Network connectivity

------------------------------------------------------------

Test connectivity:

curl http://THEHIVE_IP:9000

---

## 8️⃣ VIRUSTOTAL RETURNS LOW POSITIVES (FALSE POSITIVE)

If positives = 1 or 2:

System will not auto-delete (threshold ≥ 5)

This is expected behavior.

To adjust threshold:

Modify rule:

<field name="data.virustotal.positives">

---

## 9️⃣ RATE LIMIT ERRORS

Error:
HTTP 204 or Rate limit exceeded

Solution:

- Restrict monitored directory
- Add caching
- Upgrade API plan
- Implement scan delay

---

## 🔟 HIGH CPU OR PERFORMANCE ISSUES

Possible Causes:

- Too many monitored directories
- Bulk file copy
- Frequent FIM scans

------------------------------------------------------------

Monitor:

htop
free -h
df -h

------------------------------------------------------------

Mitigation:

- Limit realtime directories
- Avoid scanning system directories
- Use check_all wisely

---

## 1️⃣1️⃣ RULES NOT APPLYING

Check rule load:

sudo /var/ossec/bin/wazuh-logtest

Check manager log for XML errors.

Common issue:
Missing closing tag in local_rules.xml

---

## 1️⃣2️⃣ ACTIVE RESPONSE TRIGGERS BUT NO ALERT

Ensure custom active response rules exist:

rule id 100092
rule id 100093

Without them, deletion happens but no readable SOC alert appears.

---

## 1️⃣3️⃣ EICAR TEST NOT TRIGGERING

Possible Causes:

- File saved outside monitored directory
- FIM not realtime enabled
- Agent not restarted

Verify:

cat /var/ossec/etc/ossec.conf

Check:

<directories realtime="yes">

---

# 🔐 SECURITY BEST PRACTICES

- ✔ Always tie Active Response to confirmed malicious rule only
- ✔ Avoid deleting files with single AV detection
- ✔ Maintain audit logs
- ✔ Regularly rotate API keys
- ✔ Monitor API usage
- ✔ Use least privilege on script execution
- ✔ Test in staging before production

---

# 📊 FINAL HEALTH CHECK

- ✔ File detected
- ✔ VirusTotal enriched
- ✔ Threshold rule fired
- ✔ Active response executed
- ✔ File removed
- ✔ Removal logged
- ✔ Dashboard shows both alerts
- ✔ TheHive receives case

If all above pass → system fully operational.

---

# 🏁 FINAL NOTE

90% of issues arise from:

- API key mistakes
- Rule mismatch
- Script permission errors
- Missing manager restart
- Rate limit exhaustion

Always restart services after configuration changes.

---

END OF TROUBLESHOOTING GUIDE
