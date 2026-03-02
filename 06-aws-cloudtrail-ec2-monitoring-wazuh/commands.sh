#!/bin/bash

# =====================================================
# AWS CLOUDTRAIL + WAZUH EC2 MONITORING COMMANDS
# =====================================================
# This file documents all terminal commands used
# in the AWS CloudTrail EC2 monitoring integration.
# =====================================================



# =====================================================
# SECTION 1 — WAZUH MANAGER (EC2 LINUX INSTANCE)
# =====================================================

# 1️⃣ Edit Wazuh configuration file
sudo nano /var/ossec/etc/ossec.conf


# 2️⃣ Add AWS S3 Wodle block inside <ossec_config>
# (See README for full XML block)


# 3️⃣ Validate configuration syntax
sudo /var/ossec/bin/wazuh-logtest


# 4️⃣ Restart Wazuh Manager
sudo systemctl restart wazuh-manager


# 5️⃣ Check Wazuh service status
sudo systemctl status wazuh-manager


# 6️⃣ Monitor Wazuh logs (Check CloudTrail ingestion)
sudo tail -f /var/ossec/logs/ossec.log


# =====================================================
# SECTION 2 — VERIFY S3 ACCESS FROM EC2
# =====================================================

# Confirm IAM role is attached
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/

# If role attached, it should return role name


# =====================================================
# SECTION 3 — VERIFY CLOUDTRAIL LOG DELIVERY
# =====================================================

# List CloudTrail bucket contents
aws s3 ls s3://your-cloudtrail-bucket-name --recursive

# If AWS CLI is not installed:
sudo apt update
sudo apt install awscli -y

# Verify instance identity
aws sts get-caller-identity


# =====================================================
# SECTION 4 — VALIDATE CLOUDTRAIL INGESTION
# =====================================================

# Check archives.json for CloudTrail events
sudo tail -f /var/ossec/logs/archives/archives.json

# Search for EC2 events
sudo grep StartInstances /var/ossec/logs/archives/archives.json
sudo grep StopInstances /var/ossec/logs/archives/archives.json
sudo grep TerminateInstances /var/ossec/logs/archives/archives.json


# =====================================================
# SECTION 5 — TRIGGER TEST EVENTS (AWS CONSOLE)
# =====================================================
# Perform manually in AWS Console:
#
# - Start EC2 Instance
# - Stop EC2 Instance
# - Terminate Test Instance
# - Login to AWS Console
#
# These generate CloudTrail management events.


# =====================================================
# SECTION 6 — DASHBOARD VALIDATION
# =====================================================
# In Wazuh Dashboard:
#
# Go to → Security Events
# Filter:
# rule.groups: amazon
#
# Or filter:
# data.aws.eventName: StartInstances
# data.aws.eventName: StopInstances
# data.aws.eventName: ConsoleLogin


# =====================================================
# SECTION 7 — TROUBLESHOOTING COMMANDS
# =====================================================

# Check if aws-s3 wodle is running
sudo grep aws-s3 /var/ossec/logs/ossec.log

# Check for S3 permission errors
sudo grep AccessDenied /var/ossec/logs/ossec.log

# Check CloudTrail ingestion interval logs
sudo grep cloudtrail /var/ossec/logs/ossec.log

# Restart if ingestion stuck
sudo systemctl restart wazuh-manager


# =====================================================
# END OF COMMANDS
# =====================================================
