# 🛠️ Troubleshooting Guide — SOC MITRE ATT&CK Coverage Dashboard

## 🌐 Overview

This troubleshooting guide covers common issues that may appear while building, viewing, importing, saving, or validating the **SOC MITRE ATT&CK Coverage Dashboard** in Wazuh Dashboard / OpenSearch Dashboards.

This project focuses only on the **dashboard engineering and ATT&CK visualization layer**, so the issues below are centered around:

- missing MITRE fields
- empty tactic or technique charts
- timeline issues
- high-severity filter problems
- imported dashboard mismatch
- field mapping differences
- missing ATT&CK data in alerts
- visualization save or render issues

Wazuh deployment and Wazuh agent installation are intentionally not included here, because those are already documented in separate setup folders in the repository.

---

## 1️⃣ Issue: `rule.mitre.*` Fields Do Not Appear in Discover

### ❌ Problem

You open **Discover** using `wazuh-alerts-*`, but the expected MITRE fields are missing, such as:

```text
rule.mitre.tactic
rule.mitre.technique
rule.mitre.id
````

---

### 🔍 Possible Causes

* The current alerts do not include MITRE mapping
* The rules being triggered are not MITRE-mapped
* The selected time range does not include relevant alerts
* The dataset currently contains mostly benign or low-value events
* The field exists in some alerts but not in the currently visible subset
* The environment is generating alerts that do not include ATT&CK metadata

---

### ✅ Resolution

Start by widening the time range and reviewing a larger event set in **Discover**.

Use the index pattern:

```text id="6k3h3v"
wazuh-alerts-*
```

Then inspect different alerts to see whether MITRE fields are present in some events but not others.

Also check whether the alert descriptions you are testing are the kinds of detections that commonly include MITRE mapping, such as:

* brute-force detections
* credential-related detections
* account manipulation alerts
* persistence-style activity
* privilege-related alerts

If none of the current alerts contain MITRE fields, then the dashboard cannot provide ATT&CK visibility until those mapped alerts exist in the data.

---

### 🧪 Validation

A working MITRE-mapped alert should show fields such as:

```text id="ppf65s"
rule.mitre.tactic
rule.mitre.technique
rule.mitre.id
```

with actual values like:

```text id="xep0ee"
Initial Access
Brute Force
T1110
```

---

## 2️⃣ Issue: Tactics Distribution Chart Is Empty

### ❌ Problem

The **MITRE – Tactics Distribution** panel appears blank or shows no results.

---

### 🔍 Possible Causes

* `rule.mitre.tactic` is missing in the current dataset
* The severity filter removes all matching events
* The selected time range excludes MITRE-mapped alerts
* The visualization is using the wrong field name
* Imported dashboard field mapping differs from the current environment

---

### ✅ Resolution

Open **Discover** and manually validate whether the following field exists in matching alerts:

```text id="usmxa1"
rule.mitre.tactic
```

Then check whether the events also satisfy the dashboard’s alert filter:

```text id="3l3m1v"
rule.level between 8 and 15
```

If MITRE tactics exist in alerts but the chart is still empty, inspect the saved visualization configuration and confirm:

* aggregation is `Terms`
* field is `rule.mitre.tactic`
* metric is `Count`

If needed, temporarily remove the severity filter and confirm whether data appears.

---

### 🧪 Validation

A successful fix should show tactic values such as:

```text id="ryc3pr"
Initial Access
Credential Access
Persistence
Defense Evasion
Command and Control
```

---

## 3️⃣ Issue: “MITRE – Top Techniques” Shows No Data

### ❌ Problem

The **Top Techniques** pie chart does not show values or remains blank.

---

### 🔍 Possible Causes

* `rule.mitre.technique` is not populated
* The alerts being generated do not include ATT&CK technique names
* The chosen field name differs in the environment
* The severity filter excludes matching records
* The current alert dataset is too limited

---

### ✅ Resolution

In **Discover**, inspect sample events and confirm whether a technique field is present.

Validate field presence first before relying on the visualization.

If the field exists but remains empty in the chart, re-check:

* the time range
* the severity filter
* the `Terms` aggregation
* the exact field used in the visualization

If multiple technique-related field variants exist in your environment, make sure the visualization uses the one that contains actual values.

---

### 🧪 Validation

A successful chart should show values such as:

```text id="em04uk"
Brute Force
Valid Accounts
Account Manipulation
```

or other ATT&CK techniques present in your alert data.

---

## 4️⃣ Issue: “MITRE – Technique IDs” Does Not Display ATT&CK IDs

### ❌ Problem

The **Technique IDs** visualization fails to show ATT&CK IDs such as `T1110`, `T1078`, or similar values.

---

### 🔍 Possible Causes

* `rule.mitre.id` is not present
* Some alerts contain ATT&CK tactic/technique names but not the ID field
* Field mapping differs in the environment
* Imported dashboard references a field not available in the current dataset
* Time range or severity filter excludes ATT&CK-mapped records

---

### ✅ Resolution

Inspect events directly in **Discover** and confirm whether `rule.mitre.id` exists as a populated field.

If ATT&CK technique names are present but IDs are missing, this may be a **data-content issue** rather than a visualization issue.

Also verify the chart configuration:

```text id="00c7y1"
Aggregation → Terms
Field → rule.mitre.id
Metric → Count
```

If needed, temporarily broaden the time range and remove the severity filter to determine whether ATT&CK IDs exist in any part of the dataset.

---

### 🧪 Validation

A working chart should show ATT&CK IDs such as:

```text id="zt8phq"
T1110
T1078
T1098
T1136
```

or any other IDs present in the environment.

---

## 5️⃣ Issue: Technique Timeline Looks Flat, Empty, or Incomplete

### ❌ Problem

The **MITRE – Technique Timeline** chart is empty, nearly flat, or does not show the expected behavior progression.

---

### 🔍 Possible Causes

* Very low alert volume in the selected time range
* Too few MITRE-mapped alerts
* `timestamp` histogram grouping hides small spikes
* technique split field is empty or sparse
* severity filter excludes the relevant alerts
* selected time range does not include simulated attack windows

---

### ✅ Resolution

Start by checking the time picker. A narrow or mismatched time range is a common reason timeline charts appear incorrect.

Then validate that the chart uses:

```text id="rll0zh"
Y-Axis → Count
X-Axis → Date Histogram on timestamp
Split Series → Terms on rule.mitre.technique
```

If the line chart still looks incomplete:

* broaden the time range
* verify MITRE-mapped alerts exist in that range
* confirm `rule.level between 8 and 15` is not excluding all relevant technique data
* inspect Discover manually for matching events

If needed, remove the split series temporarily to confirm the time histogram is functioning.

---

### 🧪 Validation

A working timeline should show technique-related activity changing across time, with visible spikes or recurring patterns depending on the alert data present.

---

## 6️⃣ Issue: Dashboard Imports but Panels Look Different After Import

### ❌ Problem

The JSON imports successfully, but the dashboard panels appear blank, partially different, or not exactly like the original.

---

### 🔍 Possible Causes

* Field names differ between environments
* ATT&CK mapping differs in the target environment
* Imported dashboard expects data that is not present
* The target environment has fewer MITRE-mapped alerts
* Time picker defaults differ
* Visualization objects reference filters that do not match current data

---

### ✅ Resolution

After import, check the following:

1. the dashboard is using the correct index pattern
2. MITRE fields are present in the target environment
3. the selected time range includes relevant alert data
4. the severity filter matches actual alert levels in the environment
5. each visualization can be opened and inspected individually

If the environment differs from the original one, some panel adjustments may be needed even though the JSON imported successfully.

---

### 🧪 Validation

Once equivalent data and field mappings are available, the imported dashboard should closely match the original layout and ATT&CK-focused visibility.

---

## 7️⃣ Issue: Dashboard Contains Too Little ATT&CK Data to Be Useful

### ❌ Problem

The dashboard works technically, but it shows very limited technique or tactic diversity.

---

### 🔍 Possible Causes

* Only one or two ATT&CK-mapped alert types were generated
* The environment has too little simulated attack activity
* MITRE mapping exists, but alert variety is low
* The time range is too short
* Current data does not yet represent a richer attack scenario

---

### ✅ Resolution

This is often not a dashboard failure. It is a **data richness issue**.

To improve dashboard usefulness, ensure the environment has a broader set of meaningful detections that contain ATT&CK metadata.

Examples of activity that may improve coverage include:

* repeated authentication failures
* account-related detections
* brute-force scenarios
* persistence-like behavior
* privilege-related detections
* additional monitored event sources

The dashboard becomes more useful as the underlying ATT&CK-mapped data becomes richer.

---

### 🧪 Validation

A strong ATT&CK dashboard should show meaningful variation across:

* tactics
* techniques
* ATT&CK IDs
* timeline behavior

---

## 8️⃣ Issue: Time Range Is Correct but Charts Still Show No Results

### ❌ Problem

You know relevant alerts exist, but the dashboard panels still show no results.

---

### 🔍 Possible Causes

* Panel-specific filter is too restrictive
* Field path mismatch
* chart bucket configuration is incorrect
* dashboard-level filter conflicts with visualization logic
* imported visualization references stale settings

---

### ✅ Resolution

Inspect each visualization individually rather than only through the dashboard.

Check:

* field name
* metric
* bucket type
* time range
* severity filter
* dashboard-level filters
* saved object configuration

If necessary, recreate the chart manually from a working query confirmed in Discover.

---

### 🧪 Validation

If Discover returns matching ATT&CK-mapped data and the visualization uses the correct field/filter logic, the chart should render successfully.

---

## 9️⃣ Issue: ATT&CK Fields Appear in Some Alerts but Not Others

### ❌ Problem

Some Wazuh alerts include MITRE fields while others do not, making the dashboard appear inconsistent.

---

### 🔍 Possible Causes

* Not every Wazuh rule is MITRE-mapped
* The dashboard combines multiple alert categories
* Some detections are generic or operational rather than ATT&CK-oriented
* The alert mix is broader than the ATT&CK dashboard’s intended use case

---

### ✅ Resolution

This is normal in many environments.

The dashboard is most useful when it focuses on the subset of alerts that do contain ATT&CK mapping. That is why:

* field validation matters
* severity filtering matters
* data-source awareness matters

If necessary, refine the dashboard or use more targeted data to make the ATT&CK views stronger.

---

### 🧪 Validation

The dashboard should still work correctly as long as a meaningful portion of the selected data includes populated ATT&CK fields.

---

## 🔟 Issue: Dashboard Saves Fail or Visualizations Do Not Save

### ❌ Problem

You create the dashboard or visualizations, but they fail to save properly.

---

### 🔍 Possible Causes

* insufficient dashboard permissions
* expired session
* browser or UI issue
* backend saved-object problem
* save attempted with conflicting object state

---

### ✅ Resolution

Try the following:

* log in again and refresh the session
* save with a unique clear name
* test saving a smaller visualization first
* verify object-save permissions
* try another browser if necessary
* confirm the dashboard service is functioning normally

---

### 🧪 Validation

A successful save should retain:

* title
* description
* visualization configuration
* dashboard layout
* panel membership

---

## 1️⃣1️⃣ Issue: ATT&CK Dashboard Works but Does Not Improve Investigation Context

### ❌ Problem

The dashboard renders correctly, but it does not add much value during analysis.

---

### 🔍 Possible Causes

* ATT&CK data is present but too generic
* the chosen panels are technically correct but not operationally useful
* the alert mix is too noisy
* the ATT&CK technique coverage is too narrow
* the dataset does not reflect meaningful adversary simulation

---

### ✅ Resolution

Review the dashboard from the analyst’s perspective.

Ask:

* Does this help explain attacker behavior?
* Does it reveal technique trends?
* Does it improve understanding beyond rule descriptions?
* Does it help distinguish attack stage?
* Does it make reporting or triage easier?

If not, refine:

* severity focus
* time range
* data selection
* layout
* simulation depth
* ATT&CK-rich alert generation

A good ATT&CK dashboard should improve **behavioral understanding**, not just look visually structured.

---

### 🧪 Validation

A useful ATT&CK dashboard should make it easier to explain:

* what tactic is active
* what technique is repeating
* how activity is evolving
* whether the behavior reflects a broader attack pattern

---

## 1️⃣2️⃣ Issue: Imported Dashboard Exists but Is Not Easy to Find

### ❌ Problem

The JSON import appears to succeed, but the dashboard or visualizations are not immediately visible in the expected list.

---

### 🔍 Possible Causes

* imported into a different context or space
* object title differs slightly from expected naming
* visualizations imported but dashboard object not found yet
* user searched using incomplete or wrong title

---

### ✅ Resolution

Search dashboard and visualization lists using partial names such as:

```text id="ux8jgh"
MITRE
SOC
ATT&CK
Technique
Tactics
```

Also check saved objects if needed.

If necessary, re-import and watch for any warnings or skipped objects.

---

### 🧪 Validation

You should see objects like:

```text id="vt05ww"
SOC – MITRE ATT&CK Coverage Dashboard
MITRE – Tactics Distribution
MITRE – Top Techniques
MITRE – Technique IDs
MITRE – Technique Timeline
```

---

## 🧠 Best-Practice Prevention Tips

To reduce troubleshooting problems while building this dashboard:

* validate MITRE fields in Discover before building charts
* confirm high-severity alerts actually contain ATT&CK mapping
* use clear object names and descriptions
* verify time range before assuming a dashboard problem
* export JSON only after reaching a known-good dashboard state
* test each visualization individually before assembling the dashboard
* remember that ATT&CK dashboards depend heavily on data quality, not just UI configuration

---

## ✅ Final Troubleshooting Summary

Most problems with this dashboard usually come from one of these causes:

* missing MITRE fields
* time range mismatch
* severity filter removing all useful events
* incorrect field selection
* sparse ATT&CK-mapped alert data
* differences after JSON import into another environment

The best troubleshooting sequence is:

1. validate data in **Discover**
2. confirm `rule.mitre.*` fields exist
3. confirm the time range
4. confirm the severity filter
5. inspect each visualization individually
6. then re-check the dashboard as a whole

This project works best when the dashboard is treated as a practical **ATT&CK-based SOC analysis tool**, built on meaningful MITRE-mapped Wazuh alerts rather than only a visualization exercise.

---
