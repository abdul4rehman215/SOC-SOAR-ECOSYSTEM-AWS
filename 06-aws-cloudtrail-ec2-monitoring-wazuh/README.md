# 🛡️ AWS CloudTrail EC2 Monitoring with Wazuh SIEM  
## Real-World SOC Cloud Monitoring Implementation

---

# 📌 Project Overview

This project demonstrates enterprise-grade **AWS EC2 activity monitoring** using:

- AWS CloudTrail
- Amazon S3
- IAM Role (EC2 Trust)
- Wazuh AWS S3 Wodle
- Wazuh SIEM Dashboard

The objective was to build a real SOC-ready cloud monitoring pipeline capable of detecting and investigating:

- StartInstances
- StopInstances
- TerminateInstances
- ConsoleLogin
- Other EC2 management API actions

This simulates a real-world cloud security monitoring use case.

---

# 🏗 Architecture

<div align="center">

<img src="https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/resources/aws-ec2-monitoring-architecture-diagram.png" width="100%">

</div>

### Architecture Flow:

AWS CloudTrail  
→ Amazon S3 (Log Storage)  
→ IAM Role (Secure Access)  
→ Wazuh AWS S3 Module  
→ Wazuh Dashboard  

---

# 🎯 Why This Project Matters

EC2 instances are critical production assets.

Unauthorized API actions can:

- Stop production systems
- Terminate infrastructure
- Launch unauthorized instances
- Indicate compromised credentials
- Cause financial damage

CloudTrail logs everything.
Wazuh centralizes and analyzes it.

This is real cloud SOC monitoring.

---

# 🧰 Technologies Used

- AWS CloudTrail
- Amazon S3
- AWS IAM
- EC2
- Wazuh Manager
- Wazuh Dashboard

---

# 🚀 Full Implementation Guide

---

# 1️⃣ AWS CloudTrail Configuration

## Step 1: Create Multi-Region Trail

AWS Console → CloudTrail → Create Trail

Configuration:

- Multi-region trail
- Enable log file validation
- Management Events:
  - Read
  - Write
- Do NOT exclude AWS KMS events

Why?

EC2 Start/Stop/Terminate are management API calls.

---

## Step 2: Configure Secure Log Storage

During setup:

- Create new S3 bucket
- Enable Log file validation
- Enable SSE-KMS encryption

This ensures:

- Log integrity
- Encryption at rest
- Tamper protection

(See screenshot in `images/s3-config.png`)

---

## Step 3: Verify Logging Status

CloudTrail → Trails → Confirm:

Status = Logging

This ensures logs are being delivered to S3.

---

# 2️⃣ IAM Role Configuration

## Step 4: Create IAM Role for EC2

IAM → Roles → Create Role

Trusted entity:
AWS Service → EC2

Why?

Allows EC2 (Wazuh Manager instance) to access S3 securely without hardcoded credentials.

---

## Step 5: Attach S3 Read Permissions

Attach policy:

AmazonS3ReadOnlyAccess

This allows Wazuh Manager to read CloudTrail logs.

---

## Step 6: Attach Role to EC2 Instance

EC2 → Instance → Security → Modify IAM Role → Attach Role

Now Wazuh can securely access S3.

---

# 3️⃣ Wazuh CloudTrail Integration

Wazuh uses the AWS S3 wodle module to ingest CloudTrail logs.

---

## Step 7: Configure aws-s3 Wodle

On Wazuh Manager:

```bash
sudo nano /var/ossec/etc/ossec.conf
````

Add:

```xml
<wodle name="aws-s3">
  <disabled>no</disabled>
  <interval>1m</interval>
  <run_on_start>yes</run_on_start>
  <skip_on_error>yes</skip_on_error>

  <bucket type="cloudtrail">
    <name>your-cloudtrail-bucket-name</name>
  </bucket>
</wodle>
```

Explanation:

* interval → Checks S3 every 1 minute
* run_on_start → Immediate ingestion
* type="cloudtrail" → Parses CloudTrail JSON format

---

## Step 8: Restart Wazuh

```bash
sudo systemctl restart wazuh-manager
```

Monitor logs:

```bash
sudo tail -f /var/ossec/logs/ossec.log
```

---

# 4️⃣ Detection Validation

## Step 9: Trigger Test EC2 Events

Perform:

* Start EC2 instance
* Stop EC2 instance
* Login to AWS Console

---

## Step 10: Validate in Wazuh Dashboard

Go to:

Security Events → Filter:

```
rule.groups: amazon
```

You should see:

* cloudtrail source
* AWS service name
* EventName: StartInstances
* EventName: StopInstances
* ConsoleLogin

Each event includes:

* Timestamp
* AWS Account ID
* User Identity
* API action
* Source IP

---

# 📊 What We Achieved

- ✔ Centralized AWS monitoring
- ✔ Real-time EC2 activity tracking
- ✔ Secure IAM-based integration
- ✔ CloudTrail ingestion every 60 seconds
- ✔ SOC-ready detection visibility

---

# 🛡 Real SOC Scenario

If an attacker gains AWS credentials and:

* Stops production instance
* Terminates EC2
* Launches crypto mining instance

CloudTrail logs the API call
Wazuh ingests it
SOC investigates immediately

---

# 📘 Full Project Documentation

For complete step-by-step screenshots and validation:

👉 **View the full implementation PDF here**

[Complete AWS CloudTrail EC2 Monitoring Lab (Full PDF Guide)](https://github.com/abdul4rehman215/SOC-SOAR-ECOSYSTEM-AWS/blob/main/06-aws-cloudtrail-ec2-monitoring-wazuh/docs/AWS%20CloudTrail%20EC2%20Monitoring%20Wazuh%20SIEM.pdf)

---


# 📁 Repository Structure

```
06-aws-cloudtrail-ec2-monitoring-wazuh/
│
├── README.md
├── commands.sh
├── architecture-notes.txt
├── interview_qna.md
├── troubleshooting.md
│
└── docs/
    └── AWS CloudTrail EC2 Monitoring Wazuh SIEM.pdf
```

---

# 📈 Project Benefits

* Centralized AWS activity monitoring
* Improved cloud security visibility
* Faster detection of unauthorized actions
* SOC-ready logging and investigation
* Reduced cloud blind spots

---

# 🧠 Skills Demonstrated

* CloudTrail configuration
* IAM role trust design
* Secure S3 log ingestion
* Wazuh module configuration
* Cloud API log analysis
* Detection validation workflow

---

# 🏁 Conclusion

This project demonstrates practical SOC implementation of cloud monitoring using AWS CloudTrail integrated with Wazuh SIEM.

It reflects:

* Cloud auditing expertise
* Secure IAM architecture
* SIEM ingestion engineering
* Real-world detection validation

This is directly applicable to:

* SOC Analyst
* Cloud Security Analyst
* Security Engineer
* Detection Engineer roles

---
