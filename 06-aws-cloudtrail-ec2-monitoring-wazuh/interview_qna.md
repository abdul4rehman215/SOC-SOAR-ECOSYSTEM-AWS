# 🎤 AWS CloudTrail + Wazuh EC2 Monitoring  
## Interview Questions & SOC Discussion Guide

---

## 1️⃣ Why did you integrate CloudTrail with Wazuh?

CloudTrail records AWS API activity, but it does not provide centralized investigation, correlation, or alerting.

By integrating with Wazuh:

- Logs are centralized in SIEM
- Events can be correlated with other infrastructure logs
- Alerts can be severity-ranked
- SOC investigation becomes easier
- Cloud activity is no longer isolated from endpoint/network telemetry

This transforms raw audit logs into actionable security intelligence.

---

## 2️⃣ Why use IAM Role instead of AWS Access Keys?

Using IAM roles:

- Eliminates hardcoded credentials
- Reduces credential exposure risk
- Follows least-privilege model
- Supports automatic key rotation
- Is production best practice

Hardcoded keys inside ossec.conf would be insecure and not enterprise-ready.

---

## 3️⃣ What type of CloudTrail events are most critical for SOC monitoring?

High-risk EC2 events:

- TerminateInstances
- StopInstances
- RunInstances
- ModifyInstanceAttribute
- CreateSecurityGroup
- AuthorizeSecurityGroupIngress
- ConsoleLogin
- AssumeRole

These may indicate:

- Credential compromise
- Privilege abuse
- Infrastructure tampering
- Lateral movement in cloud

---

## 4️⃣ How quickly are events detected in this architecture?

Detection timing:

- CloudTrail delivery to S3 → Seconds to minutes
- Wazuh polling interval → 1 minute
- Total delay → ~1–2 minutes

This is near real-time for management-level monitoring.

---

## 5️⃣ What happens internally when Wazuh ingests CloudTrail logs?

Flow:

1. aws-s3 wodle pulls JSON from S3
2. AWS decoder parses event fields
3. Rule engine evaluates event
4. Severity level assigned
5. Indexed into OpenSearch
6. Visible in Wazuh Dashboard

This converts AWS audit logs into structured SIEM events.

---

## 6️⃣ What security risks does this project mitigate?

It helps detect:

- Unauthorized EC2 shutdowns
- Destructive instance termination
- Suspicious console logins
- Region-based anomalies
- Abuse of IAM privileges
- Unauthorized resource creation

It reduces cloud visibility blind spots.

---

## 7️⃣ What is the difference between Management Events and Data Events?

Management Events:
- Control plane API calls
- EC2 start/stop/terminate
- IAM changes
- ConsoleLogin

Data Events:
- Object-level activity (e.g., S3 object access)
- Lambda invocation
- More granular operations

For EC2 monitoring, Management Events are critical.

---

## 8️⃣ How would you improve this architecture in production?

Improvements could include:

- Using AWS EventBridge for real-time event streaming
- Sending logs to SQS instead of polling
- Implementing alerting thresholds
- Enabling GuardDuty for threat detection correlation
- Creating custom Wazuh rules for high-risk EC2 actions
- Adding geo-IP anomaly detection

---

## 9️⃣ What detection engineering opportunities exist here?

Custom rules could detect:

- EC2 termination outside business hours
- EC2 start in unauthorized region
- ConsoleLogin from unknown IP range
- Excessive instance creation (possible crypto mining)
- AssumeRole activity from unexpected accounts

This project provides telemetry foundation for advanced cloud detection engineering.

---

## 🔟 What would you investigate if a StopInstances event appears?

SOC investigation steps:

1. Identify userIdentity
2. Check sourceIPAddress
3. Verify IAM role used
4. Check eventTime
5. Confirm business justification
6. Check related CloudTrail events
7. Look for lateral IAM activity

This ensures event context is analyzed before escalation.

---

## 1️⃣1️⃣ Why is centralized monitoring important in cloud environments?

Cloud environments are API-driven.

Without central logging:

- Actions leave no visible trail
- Compromised credentials go unnoticed
- Infrastructure changes are hard to track
- Incident response is delayed

CloudTrail + Wazuh creates centralized cloud observability.

---

## 1️⃣2️⃣ What MITRE ATT&CK techniques could apply here?

Examples:

- T1078 – Valid Accounts
- T1098 – Account Manipulation
- T1485 – Data Destruction
- T1531 – Account Access Removal
- T1562 – Impair Defenses

Cloud API misuse often maps to Valid Accounts (T1078).

---

## 1️⃣3️⃣ How does this project demonstrate SOC readiness?

It shows:

- Secure IAM design
- Cloud audit logging architecture
- SIEM ingestion engineering
- Detection validation workflow
- Real cloud event investigation capability

This reflects real cloud SOC monitoring operations.

---

# 💡 Summary for Interviews

If asked to summarize:

"This project demonstrates how I engineered a secure AWS CloudTrail ingestion pipeline into Wazuh SIEM to monitor EC2 management activity in near real-time, applying secure IAM design principles and enabling SOC-level cloud investigation visibility."
