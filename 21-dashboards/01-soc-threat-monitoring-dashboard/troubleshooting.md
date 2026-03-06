# 🛠️ Troubleshooting Guide — SOC Threat Monitoring Dashboard

## 🌐 Overview

This troubleshooting guide covers common issues that may occur while building, viewing, saving, importing, or validating the **SOC Threat Monitoring Dashboard** in Wazuh Dashboard / OpenSearch Dashboards.

This project focuses only on the **dashboard engineering and visualization layer**, so the issues below are centered on:

- missing or incomplete alert data
- broken visualizations
- empty charts
- missing source IP values
- geo map issues
- timeline problems
- dashboard save/import problems
- field and index pattern issues

Wazuh deployment and Wazuh agent installation are intentionally not covered here because those setup phases are documented in separate repository folders.

---

## 1️⃣ Issue: No Data Appears in `wazuh-alerts-*`

### ❌ Problem

You open **Discover**, **Visualize**, or the dashboard itself, but no security data appears from the `wazuh-alerts-*` index.

---

### 🔍 Possible Causes

- No recent alerts have been generated
- Incorrect index pattern selected
- Time picker is too narrow
- Wazuh alerts are not being indexed properly
- The dashboard is pointing to the wrong data source
- Alert-producing activity has not yet occurred

---

### ✅ Resolution

First, verify the selected index pattern:

```text
wazuh-alerts-*
````

Then widen the time range from the dashboard time picker. Try:

```text
Last 24 hours
Last 7 days
Last 30 days
```

Next, open:

```text
Discover
```

and confirm whether any events are visible at all.

If there is still no data, verify whether alert-producing activity actually occurred in the environment. This dashboard depends on meaningful alert data already being available.

---

### 🧪 Validation

You should be able to see documents containing fields such as:

```text
timestamp
rule.level
rule.description
agent.name
data.srcip
```

If these fields are not visible in Discover, the visualizations will not work properly.

---

## 2️⃣ Issue: Dashboard Panels Show “No Results Found”

### ❌ Problem

The dashboard loads, but one or more panels show **No results found** or appear blank.

---

### 🔍 Possible Causes

* The panel filter is too restrictive
* The selected time range excludes matching alerts
* The visualization field does not exist in current data
* Imported dashboard references data not present in this environment
* Field mappings differ from the original environment

---

### ✅ Resolution

Start by checking the global time filter.

Then inspect the panel-specific logic:

* does the visualization use `rule.level` filter `8 to 15`?
* does the data actually contain alerts in that severity range?
* does the source field such as `data.srcip` exist in the indexed events?

Open **Discover** and run simple checks manually.

Examples:

```text
rule.level >= 8
rule.description exists
data.srcip exists
```

If a panel depends on a field not present in the current data, adjust the visualization or generate appropriate alerts to populate that field.

---

### 🧪 Validation

A working panel should show values once matching events exist in the selected time range.

---

## 3️⃣ Issue: “SOC – Top Attacker IPs” Chart Is Empty

### ❌ Problem

The **Top Attacker IPs** visualization shows no data or very few values.

---

### 🔍 Possible Causes

* `data.srcip` is not present in your alerts
* Alerts do not contain network-origin source IP information
* Severity filter `8 to 15` removes all matching records
* The security events being generated are local-only events
* Wazuh rules triggered without populating source-IP fields

---

### ✅ Resolution

Open **Discover** and inspect the event documents directly.

Check whether the field exists:

```text
data.srcip
```

If not, confirm which alert types are being generated. Some alerts may be:

* local system events
* host-only activity
* registry or file-change events
* non-network alerts

These may not contain source IP data.

If `data.srcip` exists but the chart is still empty, review the visualization filter and confirm that matching alerts also satisfy:

```text
rule.level between 8 and 15
```

If needed, temporarily remove the severity filter to validate field presence.

---

### 🧪 Validation

A successful fix should display source IP terms such as:

```text
3.75.217.115
101.36.228.201
```

or whatever attacker/source IPs are present in your environment.

---

## 4️⃣ Issue: Geo Map Does Not Show Attack Locations

### ❌ Problem

The **SOC – Attack Source Geo Map** panel appears empty or does not render expected attacker locations.

---

### 🔍 Possible Causes

* GeoIP enrichment is not available
* The map uses a geolocation field that does not exist in current data
* Source IPs are missing
* The map layer is configured against the wrong field
* Severity filtering excludes all geolocatable records
* Imported map references field mappings different from your environment

---

### ✅ Resolution

First, verify whether your events contain a mappable geolocation field.
The exact field may differ depending on the Wazuh/OpenSearch pipeline used in your environment.

Check in Discover whether:

* source IP exists
* any geolocation-related field exists
* the relevant alerts survive the severity filter

If you imported the dashboard JSON into another environment, the map may need field remapping if the geolocation field name differs.

Also validate that the selected time range contains relevant network-origin events.

---

### 🧪 Validation

A successful configuration should render attack-source points on the world map for alerts that contain valid source-IP geolocation data.

---

## 5️⃣ Issue: “SOC – High Severity Attack Timeline” Looks Flat or Empty

### ❌ Problem

The timeline chart shows no visible spikes, looks nearly flat, or remains empty.

---

### 🔍 Possible Causes

* Very low alert volume in selected time range
* No alerts match severity level `8 to 15`
* The date histogram interval is too broad or too narrow
* Timestamp field mapping is incorrect
* Current data does not contain attack bursts

---

### ✅ Resolution

Check the selected time range first. If the time window is too broad, spikes may appear flattened. If too narrow, activity may be excluded.

Then confirm the visualization uses:

```text
Field → timestamp
Aggregation → Date Histogram
```

If needed:

* expand the time range
* generate more meaningful alert activity
* validate that high-severity alerts actually exist
* inspect a few sample events in Discover

For testing, you can temporarily remove the severity filter and verify the chart shape with broader alert coverage.

---

### 🧪 Validation

A properly functioning timeline should show changes in alert counts over time and reflect periods of higher security activity.

---

## 6️⃣ Issue: “SOC – Top Alert Types” Shows Unexpected or Noisy Categories

### ❌ Problem

The **Top Alert Types** chart is dominated by unexpected alerts, overly noisy categories, or values that are not useful for analyst triage.

---

### 🔍 Possible Causes

* Broad alert set with no filtering
* Alert volume includes benign but frequent operational events
* Low-value or noisy rules dominate the data
* Time range includes too much historical noise
* Dashboard is reflecting mixed use cases rather than focused threat activity

---

### ✅ Resolution

Review the selected time range and inspect the most frequent `rule.description` values in Discover.

If the visualization is too noisy, consider refining:

* time range
* severity range
* dashboard use-case scope
* upstream rule tuning in other projects/folders

This project intentionally focuses on dashboarding, but it also reveals where **rule tuning and noise reduction** may be needed elsewhere in the SOC.

---

### 🧪 Validation

A useful chart should highlight recognizable attack-relevant or monitoring-relevant categories rather than only repetitive low-value noise.

---

## 7️⃣ Issue: “SOC – Alerts by Severity” Does Not Show Expected Levels

### ❌ Problem

The severity chart displays unexpected rule levels, too few severity groups, or no higher-severity alerts.

---

### 🔍 Possible Causes

* Current data is dominated by lower-severity events
* High-severity detections were not triggered
* Time range excludes periods of suspicious activity
* Imported dashboard is functioning correctly, but the environment data differs

---

### ✅ Resolution

Check raw events in Discover and inspect:

```text
rule.level
```

Review whether the environment actually contains alerts in the levels you expect.
If not, this is often a **data reality issue**, not a dashboard failure.

If the purpose is to demonstrate a threat-focused dashboard, generate or retain meaningful security activity that creates mid/high severity detections.

---

### 🧪 Validation

A working severity chart should show the distribution of actual alert severity values present in the selected data set.

---

## 8️⃣ Issue: Dashboard JSON Imports but Looks Different After Import

### ❌ Problem

The imported dashboard loads, but some panels are missing, different, blank, or not behaving exactly like the original.

---

### 🔍 Possible Causes

* Field names differ in the new environment
* Index patterns are different
* GeoIP/geolocation fields differ
* Current dataset does not match the original environment
* Visualization dependencies are present but underlying data is missing
* Time range defaults differ

---

### ✅ Resolution

After importing the dashboard JSON:

1. Confirm the correct index pattern is available
2. Confirm relevant fields exist
3. Check the time picker
4. Inspect each panel individually
5. Re-map fields if the target environment uses a different field structure

This is especially important for:

* source IP fields
* geolocation fields
* severity-based visualizations

---

### 🧪 Validation

An imported dashboard should visually resemble the original once equivalent data, mappings, and time ranges are available.

---

## 9️⃣ Issue: Cannot Save Visualization or Dashboard

### ❌ Problem

You create a visualization or dashboard, but it does not save successfully.

---

### 🔍 Possible Causes

* Insufficient permissions in Wazuh/OpenSearch Dashboards
* Session timeout
* Browser issue
* Naming conflict or save failure
* Backend/dashboard service issue

---

### ✅ Resolution

Try the following:

* refresh the session and log in again
* save with a clear unique name
* verify dashboard privileges for the user account
* test saving a smaller/simple visualization
* try another browser if needed

Also confirm that the dashboard service is functioning normally and the session has not expired.

---

### 🧪 Validation

A successful save should preserve:

* title
* visualization type
* description
* panel configuration
* dashboard layout

---

## 🔟 Issue: Imported Dashboard Exists but Is Not Visible in Dashboard List

### ❌ Problem

The JSON import process appears to complete, but the dashboard does not appear where expected.

---

### 🔍 Possible Causes

* Imported into a different space/tenant/context
* Saved object import succeeded partially
* Object naming mismatch
* Dashboard exists but not searched by the exact name
* Related visualizations imported, but the dashboard object itself did not

---

### ✅ Resolution

Search carefully in the dashboard list using part of the expected title, such as:

```text
SOC
Threat Monitoring
Wazuh Threat Monitoring Dashboard
```

Also check:

* saved objects
* dashboards list
* visualization list

If needed, repeat the import and watch for any object-level warnings.

---

### 🧪 Validation

You should see the dashboard entry in the dashboard list with the expected title and description.

---

## 1️⃣1️⃣ Issue: Dashboard Looks Correct but Triage Value Is Poor

### ❌ Problem

The dashboard works technically, but it does not help much during investigation or prioritization.

---

### 🔍 Possible Causes

* Panels are visually correct but not operationally useful
* Data source includes too much noise
* Severity thresholds are too broad or too narrow
* Alert mix does not represent the intended threat-monitoring use case
* Visualizations are not aligned with analyst questions

---

### ✅ Resolution

Re-evaluate the dashboard from the analyst’s perspective.

Ask:

* Does this panel help triage?
* Does it improve visibility?
* Does it highlight meaningful suspicious activity?
* Does it support investigation or just display counts?

If needed, refine:

* filters
* field choice
* panel scope
* time window
* layout

A good SOC dashboard should improve decision-making, not just display data.

---

### 🧪 Validation

A useful dashboard should help an analyst answer practical questions quickly without needing to start from raw logs every time.

---

## 1️⃣2️⃣ Issue: Data Exists in Discover but Not in Visualization

### ❌ Problem

You can see matching alerts in **Discover**, but the visualization still appears empty or wrong.

---

### 🔍 Possible Causes

* Visualization field mismatch
* Bucket configuration error
* panel filter conflict
* saved visualization using stale configuration
* dashboard-level filter overriding expected results

---

### ✅ Resolution

Compare the visualization configuration carefully against the working data seen in Discover.

Validate:

* index pattern
* field name
* filter conditions
* aggregation type
* time picker
* dashboard-level filters
* visualization-level filters

If needed, rebuild the panel from scratch using the same working query logic confirmed in Discover.

---

### 🧪 Validation

If Discover returns matching events and the visualization uses the same field/filter logic, the panel should begin showing data.

---

## 🧠 Best-Practice Prevention Tips

To reduce troubleshooting problems while building or importing this dashboard:

* always validate fields in Discover first
* confirm useful alert volume before building charts
* keep visualization names clear and consistent
* use meaningful descriptions while saving
* verify geolocation field availability before building maps
* test severity filters before finalizing panels
* export the dashboard JSON after a known-good state
* document the dashboard even if JSON is preserved

---

## ✅ Final Troubleshooting Summary

Most issues with this project usually come from one of these areas:

* no matching alert data
* incorrect time range
* missing source IP values
* missing geolocation field
* severity filter excluding results
* environment differences after JSON import

The best troubleshooting method is:

1. validate data in **Discover**
2. confirm the field exists
3. confirm the time range
4. confirm filters
5. inspect each panel individually
6. then re-check the dashboard as a whole

This project is strongest when the dashboard is treated not just as a visual artifact, but as a **working SOC monitoring tool built on real alert data**.
