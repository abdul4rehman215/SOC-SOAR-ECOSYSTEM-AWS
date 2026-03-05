# 🛠 Troubleshooting Guide - AWS CloudTrail + Wazuh 

This document covers:

- Integration errors
- IAM permission issues
- CloudTrail delivery failures
- Detection gaps
- SOC response workflow

---

# 1️⃣ CloudTrail Logs Not Appearing in Wazuh

## Possible Causes

- CloudTrail not logging
- Logs not delivered to S3
- IAM role not attached
- Incorrect bucket name in ossec.conf
- Wazuh manager not restarted

---

## Step-by-Step Diagnosis

### Step 1: Verify CloudTrail Status

AWS Console → CloudTrail → Trails

Check:
Status = Logging

If not logging:
Enable logging immediately.

---

### Step 2: Verify Logs in S3

On Wazuh EC2:

```bash
aws s3 ls s3://your-cloudtrail-bucket-name --recursive
```

If empty:
CloudTrail not delivering logs.

---

### Step 3: Check IAM Role Attachment

On EC2:

```bash
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

If empty:
IAM role not attached.

Attach role and restart Wazuh.

---

### Step 4: Check Wazuh Logs

```bash
sudo tail -f /var/ossec/logs/ossec.log
```

Look for:
- AccessDenied
- Bucket errors
- aws-s3 errors

---

# 2️⃣ AccessDenied Error in ossec.log

Example:

AccessDenied: Access Denied

## Cause

IAM role missing S3 read permissions.

## Fix

Attach policy:

AmazonS3ReadOnlyAccess

Or create custom least-privilege policy:

Allow:
- s3:GetObject
- s3:ListBucket

Then restart Wazuh.

---

# 3️⃣ CloudTrail Logging Enabled but No EC2 Events

## Cause

Management events not enabled during trail creation.

## Fix

CloudTrail → Edit trail:

Ensure:
- Management events enabled
- Read & Write selected

Save changes.

---

# 4️⃣ Wazuh Service Restarted but No Ingestion

## Cause

Incorrect bucket name in ossec.conf.

Example mistake:

<name>wrong-bucket-name</name>

## Fix

Verify exact bucket name in AWS.
Update configuration.
Restart service:

```bash
sudo systemctl restart wazuh-manager
```

---

# 5️⃣ Event Appears Late (Delay)

## Why It Happens

CloudTrail log delivery delay + Wazuh polling interval (1m).

Expected total delay:
1–2 minutes.

This is normal behavior.

---

# 6️⃣ Detection Gap Scenario (SOC-Level)

Scenario:

Attacker gains AWS credentials.
Stops EC2 instance.

CloudTrail logs event.
But SOC does not investigate immediately.

Why?

- No alert severity tuning
- No rule escalation
- No alert notifications configured

Mitigation:

Create custom Wazuh rule:

If eventName = TerminateInstances
→ Raise severity to 10+

Add alerting integration (Slack / Email).

---

# 7️⃣ Suspicious ConsoleLogin Investigation Workflow

If ConsoleLogin detected:

SOC Steps:

1. Check userIdentity
2. Check sourceIPAddress
3. Compare with known IP ranges
4. Check geo-location
5. Look for AssumeRole activity
6. Check subsequent EC2 events
7. Escalate if suspicious

This ensures context-aware response.

---

# 8️⃣ Bucket Misconfiguration

If bucket policy blocks EC2 access:

Symptoms:
- AccessDenied in logs
- No ingestion

Fix:

Update bucket policy to allow:

Principal:
EC2 IAM Role ARN

Action:
- s3:GetObject
- s3:ListBucket

---

# 9️⃣ AWS CLI Not Installed on EC2

If "aws: command not found":

Install:

```bash
sudo apt update
sudo apt install awscli -y
```

---

# 🔟 CloudTrail Region Mismatch

If CloudTrail created in one region but EC2 activity occurs in another:

Solution:

Use Multi-Region Trail.

This ensures all regions are monitored.

---

# 1️⃣1️⃣ SOC Mitigation Example

Case:
TerminateInstances detected.

SOC Response:

1. Identify userIdentity
2. Confirm business justification
3. Check IAM policy permissions
4. Disable compromised credentials
5. Rotate access keys
6. Investigate related activity
7. Document incident

---

# 1️⃣2️⃣ Hardening Recommendations

To improve this architecture:

- Enable CloudTrail organization-wide
- Enable GuardDuty
- Create custom high-severity rules
- Add real-time alerting
- Enable MFA enforcement
- Restrict EC2 termination permissions

---

# 1️⃣3️⃣ Common Configuration Mistakes

- Forgetting to restart Wazuh
- Typo in bucket name
- IAM role not attached to EC2
- Excluding management events
- Using single-region trail
- Not verifying S3 delivery

---

# 🧠 Key Takeaway

Cloud monitoring requires:

- Correct logging configuration
- Secure IAM design
- Proper SIEM ingestion
- Alert severity tuning
- Continuous validation

This project demonstrates full lifecycle:

Configuration → Ingestion → Detection → Investigation → Mitigation
