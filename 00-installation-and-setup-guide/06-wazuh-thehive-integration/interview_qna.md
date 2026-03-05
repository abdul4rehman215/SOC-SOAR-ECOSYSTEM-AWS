# 🎤 Interview Q&A - Wazuh ↔ TheHive Integration

---

## 1️⃣ Why integrate Wazuh with TheHive?

Wazuh generates alerts, while TheHive manages incidents.  
Integration automates the workflow from detection to investigation.

---

## 2️⃣ What problem does this integration solve?

It eliminates manual alert copying and enables structured incident response workflows.

---

## 3️⃣ What protocol is used for integration?

The integration uses REST API calls from Wazuh to TheHive.

---

## 4️⃣ What library is required for the integration?

The integration uses:

```bash
thehive4py
```

Installed inside Wazuh's embedded Python environment.

---

## 5️⃣ Why must the integration script use Wazuh’s embedded Python?

Because Wazuh runs its own Python framework.  
Using system Python may cause module mismatch errors.

---

## 6️⃣ Where is the integration script placed?

```
/var/ossec/integrations/
```

Both:
- custom-w2thive
- custom-w2thive.py

---

## 7️⃣ What does the integration script do?

It:
- Reads Wazuh JSON alert
- Formats alert description
- Extracts artifacts (IP, URL, domain)
- Sends alert to TheHive via API

---

## 8️⃣ How are severity levels controlled?

Through:

- `lvl_threshold` inside the Python script
- `<level>` tag inside ossec.conf

Alerts below threshold are ignored.

---

## 9️⃣ How do you test the integration manually?

```bash
/var/ossec/integrations/custom-w2thive \
/var/ossec/logs/alerts/alerts.json \
API_KEY \
http://THEHIVE_IP:9000
```

No output = success.

---

## 🔟 What logs should be monitored?

Integration logs:

```bash
tail -f /var/ossec/logs/integrations.log
```

Manager logs:

```bash
tail -f /var/ossec/logs/ossec.log
```

---

## 1️⃣1️⃣ What security considerations apply?

- Restrict port 9000
- Protect API key
- Use HTTPS in production
- Limit access via Security Groups

---

## 1️⃣2️⃣ What happens if the API key is invalid?

TheHive returns 401/403, and the alert will not be created.

---

## 1️⃣3️⃣ Why is this integration important in a SOC?

It enables:

- Automated case creation
- Faster MTTR
- Better collaboration
- Complete audit trail

---

## 1️⃣4️⃣ What is the benefit over using email alerts?

Email is unstructured.  
TheHive provides structured, trackable, task-based incident response.

---

## 1️⃣5️⃣ How does this improve SOC maturity?

It transforms the environment from:

Alert Monitoring  
to  
Incident Lifecycle Management.

---

# 🏁 Summary

The Wazuh ↔ TheHive integration is a critical component of a modern SOC.

It bridges:

Detection → Investigation → Response

and enables automation, collaboration, and structured incident handling.
