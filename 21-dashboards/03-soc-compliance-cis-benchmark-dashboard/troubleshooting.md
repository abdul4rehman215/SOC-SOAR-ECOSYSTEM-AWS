# 🛠️ Troubleshooting Guide — SOC Compliance & CIS Benchmark Dashboard

## 🌐 Overview

This troubleshooting guide covers common issues that may occur while building, viewing, saving, importing, validating, or using the **SOC Compliance & CIS Benchmark Dashboard** in Wazuh Dashboard / OpenSearch Dashboards.

This project focuses only on the **dashboard engineering and compliance-visualization layer**, so the issues below are centered on:

- missing SCA data
- incorrect filtering
- empty compliance charts
- failed-check visualizations not populating
- findings timeline issues
- gauge interpretation confusion
- field mapping differences after import
- dashboard save/import issues

Wazuh deployment and Wazuh agent installation are intentionally not covered here, because those setup phases are already documented in separate repository folders.

---

## 1️⃣ Issue: No SCA Data Appears in Discover

### ❌ Problem

You open **Discover** and select `wazuh-alerts-*`, but no compliance-related data appears after applying the SCA filter.

---

### 🔍 Possible Causes

- No SCA findings have been generated yet
- Incorrect index pattern selected
- Time range is too narrow
- `rule.groups is sca` filter is not returning results because SCA data is absent
- Agents have not sent recent SCA findings
- Current environment contains other alert types but not compliance findings

---

### ✅ Resolution

First, confirm the selected index pattern is:

```text
wazuh-alerts-*
````

Then apply the filter:

```text
rule.groups is sca
```

Next, widen the dashboard time picker to something broader such as:

```text
Last 7 days
Last 30 days
```

If you still do not see any SCA data, inspect the event stream without the `sca` filter to confirm whether the environment is receiving alerts at all.

Then verify whether the monitored systems are actually producing SCA findings and whether those findings have recently been indexed.

---

### 🧪 Validation

A working SCA event stream should show fields such as:

```text
rule.groups
data.sca.check.title
data.sca.check.result
data.sca.policy
timestamp
```

with `rule.groups` containing the value:

```text
sca
```

---

## 2️⃣ Issue: “Compliance – Pass vs Fail” Chart Is Empty

### ❌ Problem

The **Compliance – Pass vs Fail** donut chart shows no values or does not render expected pass/fail status.

---

### 🔍 Possible Causes

* `data.sca.check.result` is missing in current SCA events
* `rule.groups is sca` filter excludes all visible data
* Time range excludes compliance findings
* Visualization field selection is incorrect
* Imported dashboard field mapping differs from the target environment

---

### ✅ Resolution

In **Discover**, confirm that SCA events contain the field:

```text
data.sca.check.result
```

Expected values normally include:

```text
passed
failed
not applicable
```

Then confirm the visualization uses:

```text
Aggregation → Terms
Field → data.sca.check.result
Metric → Count
```

If needed, rebuild the panel manually from a working filtered data set confirmed in Discover.

---

### 🧪 Validation

A successful chart should show one or more categories such as:

```text
passed
failed
not applicable
```

with visible distribution across the SCA result states.

---

## 3️⃣ Issue: “Top Failed CIS Checks” Panel Shows No Results

### ❌ Problem

The **Compliance – Top Failed CIS Checks** bar chart is blank or shows very limited data.

---

### 🔍 Possible Causes

* Additional failed-only filter excludes all current records
* `data.sca.check.result` is not equal to `failed` in the selected time range
* `data.sca.check.title` is missing or not populated
* Time range includes mostly passed checks
* Field path differs across environments
* Imported dashboard JSON references fields that do not map exactly in the new environment

---

### ✅ Resolution

This panel depends on **two layers of filtering**:

1. base compliance filter

```text
rule.groups is sca
```

2. failed-only filter

```text
data.sca.check.result is failed
```

Start by checking whether failed findings exist at all in Discover.

Then validate the field:

```text
data.sca.check.title
```

If failed results are rare or absent in the selected time window, the chart may appear empty even though the dashboard is configured correctly.

If necessary, broaden the time range or remove the failed-only filter temporarily to confirm field presence.

---

### 🧪 Validation

A working chart should show failing control titles such as:

```text
Ensure ssh PermitEmptyPasswords is disabled
Ensure ssh HostbasedAuthentication is disabled
Ensure ssh LogLevel is configured
```

or other CIS check titles present in your environment.

---

## 4️⃣ Issue: Findings Timeline Does Not Show Meaningful Trends

### ❌ Problem

The **Compliance – Findings Timeline** chart appears flat, empty, or difficult to interpret.

---

### 🔍 Possible Causes

* Too little SCA data in the selected time range
* Few compliance findings were indexed recently
* Timestamp grouping is too broad or too narrow
* Split series on result field does not have enough variation
* The environment has static posture with little change over time
* Imported dashboard is working, but data volume is low

---

### ✅ Resolution

Check whether the time range includes enough findings to produce visible trends.

Then confirm the visualization uses:

```text
Metric → Count
X-Axis → Date Histogram on timestamp
Split Series → Terms on data.sca.check.result
```

If the chart is hard to interpret:

* expand the time range
* confirm multiple result states exist
* verify that pass/fail findings actually changed over time
* temporarily simplify the chart by removing split series

A flat timeline may reflect **stable posture** rather than dashboard failure.

---

### 🧪 Validation

A useful chart should show changes across time for result types such as:

```text
passed
failed
```

or at least visible count fluctuations if compliance findings are present.

---

## 5️⃣ Issue: “Compliance – Overall Score” Gauge Seems Misleading

### ❌ Problem

The gauge renders, but the number displayed seems confusing, too large, or not like a true percentage score.

---

### 🔍 Possible Causes

* The visualization is using a count metric rather than a calculated percentage
* The gauge reflects event volume instead of normalized compliance percentage
* Range thresholds are cosmetic unless backed by meaningful numeric interpretation
* Imported dashboard preserved the original state, but the environment’s data shape differs
* Multiple gauges or panels may be showing count-based posture indicators rather than a mathematically strict score

---

### ✅ Resolution

This is often a **design interpretation issue**, not a technical failure.

The gauge in this project is used as a high-level compliance posture indicator based on the working configuration used during implementation. If you want a stricter percentage-based representation, the gauge logic may need custom metric design beyond a simple count visualization.

For this project:

* preserve the original exported dashboard state
* document how it is being interpreted
* ensure the README notes that gauge meaning depends on the underlying metric model

If the displayed value is unexpected, inspect the metric configuration and confirm whether it is using a raw count rather than a normalized posture ratio.

---

### 🧪 Validation

A working gauge should at least render consistently and respond to compliance data, even if its interpretation depends on the metric design chosen in the environment.

---

## 6️⃣ Issue: Dashboard JSON Imports but Panels Look Different

### ❌ Problem

The JSON imports successfully, but some panels appear blank, different, or not exactly like the original dashboard.

---

### 🔍 Possible Causes

* Field names differ in the target environment
* The imported environment has different policy names or check titles
* SCA data volume differs
* The time range defaults differ after import
* The same saved objects imported, but the underlying data does not match the original dataset
* Gauge or chart interpretation changes because the new environment has different result distributions

---

### ✅ Resolution

After importing the dashboard:

1. confirm the correct index pattern exists
2. confirm SCA data is present in `wazuh-alerts-*`
3. confirm `rule.groups is sca` returns data
4. inspect each visualization individually
5. confirm fields like `data.sca.check.title`, `data.sca.check.result`, and `data.sca.policy` exist and contain values
6. check the global time range

If the target environment differs meaningfully from the original one, some panel appearance differences are expected even if the dashboard imports correctly.

---

### 🧪 Validation

Once equivalent SCA data and compatible fields are available, the imported dashboard should closely resemble the original layout and function.

---

## 7️⃣ Issue: SCA Fields Exist, but the Dashboard Still Shows Unrelated Data

### ❌ Problem

The dashboard contains unrelated alerts or seems contaminated with non-compliance data.

---

### 🔍 Possible Causes

* The `rule.groups is sca` filter was not applied
* One or more panels were created without the proper compliance-only filter
* The dashboard or visualization is using broader alert data accidentally
* Imported visualization lost a panel-level filter during editing

---

### ✅ Resolution

The most important isolation filter for this project is:

```text
rule.groups is sca
```

Confirm that:

* the dashboard has the filter applied globally, or
* each visualization was created with the proper SCA-only scope

If unrelated data is appearing, open the affected visualization and verify it is not using unfiltered `wazuh-alerts-*` event data.

---

### 🧪 Validation

A correctly scoped dashboard should show only compliance-related fields and findings, not authentication, FIM, IDS, or general security alert categories.

---

## 8️⃣ Issue: SCA Results Appear, but Policy Split Is Missing or Weak

### ❌ Problem

The **Top Failed CIS Checks** chart does not split clearly by policy, or the policy legend is incomplete.

---

### 🔍 Possible Causes

* `data.sca.policy` is missing or sparse
* The current findings come from only one policy
* Policy split size is too small
* Imported data set does not contain multiple policy sources
* The field exists but has inconsistent values

---

### ✅ Resolution

Check in Discover whether the field:

```text
data.sca.policy
```

contains multiple policy names such as:

```text
CIS Ubuntu Linux 24.04
CIS Microsoft Windows
```

If only one policy appears in the current data set, the split series behavior may look limited even though the panel is working correctly.

You can also increase split-series size if needed, but the usefulness depends on actual multi-policy data being present.

---

### 🧪 Validation

A useful policy split should show separate series or legend entries when multiple policy sources are present in the data.

---

## 9️⃣ Issue: Dashboard Saves Fail or Visualizations Do Not Save Properly

### ❌ Problem

You build a visualization or dashboard, but saving fails or the object does not appear afterward.

---

### 🔍 Possible Causes

* insufficient dashboard permissions
* expired session
* browser/UI issue
* save conflict
* backend saved object issue

---

### ✅ Resolution

Try the following:

* refresh the browser and log in again
* save with a clear unique name
* test saving one simple visualization first
* verify user permissions in Wazuh/OpenSearch Dashboards
* try a different browser if needed
* confirm the dashboard service is working normally

---

### 🧪 Validation

A successful save should retain:

* title
* description
* panel settings
* filters
* layout
* aggregation logic

---

## 🔟 Issue: Dashboard Works but Does Not Help Remediation Prioritization

### ❌ Problem

The dashboard renders correctly, but it does not clearly help the team decide what to fix first.

---

### 🔍 Possible Causes

* too many findings with no prioritization context
* result distribution is visible, but failed-control ranking is weak
* current findings are not differentiated enough
* environment contains too little variation in failed checks
* dashboard is technically correct but not action-oriented enough

---

### ✅ Resolution

Evaluate the dashboard from the remediation perspective.

Ask:

* Does it highlight the most frequently failing controls?
* Does it show repeated weak points across systems or policies?
* Does it make trend changes visible?
* Does it guide hardening priorities?

If not, refine:

* failed-only filters
* control-title ordering
* policy splits
* time ranges
* chart layout

A good compliance dashboard should help answer:

> **What posture issue should we fix first?**

not just:

> **What data exists?**

---

### 🧪 Validation

A useful dashboard should help security teams quickly identify the most common and meaningful hardening gaps.

---

## 1️⃣1️⃣ Issue: Findings Timeline Shows Results but Remediation Progress Is Hard to See

### ❌ Problem

The timeline chart shows compliance findings, but it is difficult to tell whether posture is improving.

---

### 🔍 Possible Causes

* the environment has too few remediation cycles
* scan cadence is limited
* there is not enough time-based difference in the findings
* pass/fail counts are stable
* the chart is technically correct but the dataset lacks clear before/after changes

---

### ✅ Resolution

This is often a **data-history issue**, not a broken chart.

To better show remediation progress, the environment needs:

* repeated SCA scans over time
* meaningful changes in controls
* before-and-after posture data
* enough historical findings to visualize trend shifts

If the underlying data does not include improvement cycles yet, the dashboard cannot invent them visually.

---

### 🧪 Validation

A richer timeline becomes visible when the environment contains enough historical posture changes.

---

## 1️⃣2️⃣ Issue: Dashboard Exists After Import but Is Hard to Find

### ❌ Problem

The dashboard or some visualizations appear to import successfully, but they are not easy to find in the dashboard or visualization list.

---

### 🔍 Possible Causes

* the dashboard title is not searched exactly
* saved objects imported into the environment but were not immediately located
* only some related visualizations are visible at first
* naming was remembered partially

---

### ✅ Resolution

Search the dashboards and visualization lists using partial terms such as:

```text
Compliance
CIS
SCA
Pass
Failed
```

Also inspect saved objects if necessary.

If needed, re-import and watch for object-level warnings or skipped items.

---

### 🧪 Validation

You should be able to find objects such as:

```text
SOC – Compliance & CIS Benchmark Dashboard
Compliance – Overall Score
Compliance – Pass vs Fail
Compliance – Top Failed CIS Checks
Compliance – Findings Timeline
```

---

## 🧠 Best-Practice Prevention Tips

To reduce troubleshooting issues while building this dashboard:

* always validate `rule.groups is sca` first in Discover
* confirm the required `data.sca.*` fields exist before creating charts
* isolate compliance data before building visualizations
* use clear object names and descriptions
* test each visualization individually before adding it to the dashboard
* remember that gauge interpretation depends on metric design
* export the dashboard JSON after reaching a known-good state
* document the dashboard even when the JSON is preserved

---

## ✅ Final Troubleshooting Summary

Most issues with this dashboard usually come from one of these areas:

* no SCA data in the selected time range
* missing or weak `data.sca.*` fields
* forgetting to filter `rule.groups is sca`
* failed-only filters removing all results
* environment differences after JSON import
* misunderstanding gauge metric interpretation

The best troubleshooting sequence is:

1. validate SCA data in **Discover**
2. confirm `rule.groups is sca`
3. confirm `data.sca.*` fields exist
4. inspect each visualization individually
5. confirm the time range
6. then re-check the dashboard as a whole

This project works best when the dashboard is treated as a practical **security posture monitoring tool** built on real SCA findings, not just a reporting screen.
