# Information

You can copy-paste directly into:

```bash
/var/ossec/etc/rules/sysmon_custom.xml
```

Then restart:

```bash
systemctl restart wazuh-manager
```

---

# 🔹 VERSION 1 – INITIAL RULES (Before DNS Fix)

This was your **basic Sysmon alerting setup**.

It:

* Triggered alerts for Event 1, 2, 3
* Basic DNS Event 22 logging
* No advanced filtering
* No refined detection logic

---

# 🔴 What Happened in Version 1?

* Process events worked ✅
* Registry events flooded ⚠️
* DNS Event 22 NOT appearing properly ❌
* Needed decoder + config validation
* Needed refined detection

---

# 🔹 VERSION 2 – FINAL FIXED VERSION (After DNS Debug + Advanced Detection)

This version includes:

✔ Proper Event 22 matching
✔ LSASS access detection
✔ Suspicious DNS detection
✔ LOLBins detection
✔ Encoded PowerShell detection
✔ MITRE mapping
✔ Clean grouping

---

# 📌 Difference Between V1 and V2

| Feature             | Version 1 | Version 2 |
| ------------------- | --------- | --------- |
| Basic Sysmon Events | ✅         | ✅         |
| Proper DNS Fix      | ❌         | ✅         |
| LSASS Detection     | ❌         | ✅         |
| LOLBins Detection   | ❌         | ✅         |
| Encoded PowerShell  | ❌         | ✅         |
| MITRE Mapping       | ❌         | ✅         |
| SOC-grade tuning    | ❌         | ✅         |

---

# 🔥 Important After Adding Rules

Always run:

```bash
/var/ossec/bin/wazuh-logtest
```

Then restart:

```bash
systemctl restart wazuh-manager
```

---

# 🧠 Final Advice

Use:

* **Version 1** → For showing debugging journey in GitHub
* **Version 2** → For final working lab environment
