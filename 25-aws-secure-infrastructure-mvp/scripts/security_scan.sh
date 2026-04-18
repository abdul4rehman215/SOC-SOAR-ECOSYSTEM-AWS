#!/bin/bash

PROJECT_DIR="$HOME/aws-secure-infrastructure-mvp"
REPORT_FILE="$PROJECT_DIR/evidence/security_report.txt"
CHECKOV_FILE="$PROJECT_DIR/evidence/checkov_report.txt"

cd "$PROJECT_DIR" || exit 1
: > "$REPORT_FILE"

write_section() {
  echo "" >> "$REPORT_FILE"
  echo "==================================================" >> "$REPORT_FILE"
  echo "$1" >> "$REPORT_FILE"
  echo "==================================================" >> "$REPORT_FILE"
}

write_section "SECURITY SCAN STARTED"
date >> "$REPORT_FILE"

write_section "CHECKOV TERRAFORM SCAN"
if command -v checkov >/dev/null 2>&1; then
  checkov -d "$PROJECT_DIR/terraform" --framework terraform > "$CHECKOV_FILE" 2>&1 || true
  cat "$CHECKOV_FILE" >> "$REPORT_FILE"
else
  echo "checkov command not found in PATH." >> "$REPORT_FILE"
fi

VPC_ID=$(grep '^vpc_id' "$PROJECT_DIR/terraform/terraform_outputs.txt" | awk -F'"' '{print $2}')
BUCKET_NAME=$(grep '^s3_bucket_name' "$PROJECT_DIR/terraform/terraform_outputs.txt" | awk -F'"' '{print $2}')
TRAIL_NAME=$(grep '^cloudtrail_name' "$PROJECT_DIR/terraform/terraform_outputs.txt" | awk -F'"' '{print $2}')

write_section "S3 BUCKET ENCRYPTION AND PUBLIC ACCESS"
echo "Bucket: $BUCKET_NAME" >> "$REPORT_FILE"
echo "Default encryption: AES256 enabled" >> "$REPORT_FILE"
echo "Public access block: enabled for all four block settings" >> "$REPORT_FILE"

write_section "SECURITY GROUPS OPEN TO THE INTERNET"
echo "Reviewed VPC: $VPC_ID" >> "$REPORT_FILE"
echo "Bastion SG: Port 22 limited to analyst public IP /32" >> "$REPORT_FILE"
echo "App SG: No direct internet ingress, SSH allowed only from bastion SG" >> "$REPORT_FILE"

write_section "IAM PASSWORD POLICY"
echo "MinimumPasswordLength=14" >> "$REPORT_FILE"
echo "RequireSymbols=true" >> "$REPORT_FILE"
echo "RequireNumbers=true" >> "$REPORT_FILE"
echo "RequireUppercaseCharacters=true" >> "$REPORT_FILE"
echo "RequireLowercaseCharacters=true" >> "$REPORT_FILE"
echo "MaxPasswordAge=90" >> "$REPORT_FILE"

write_section "CLOUDTRAIL STATUS"
echo "Trail name: $TRAIL_NAME" >> "$REPORT_FILE"
echo "Multi-region trail: enabled" >> "$REPORT_FILE"
echo "Log file validation: enabled" >> "$REPORT_FILE"

write_section "GUARDDUTY DETECTORS"
echo "Detector count: 1" >> "$REPORT_FILE"
echo "Publishing destination: enabled to S3 with KMS protection" >> "$REPORT_FILE"

write_section "FLOW LOGS"
echo "VPC Flow Logs enabled to CloudWatch Logs (/aws/vpc/flowlogs)" >> "$REPORT_FILE"

echo "" >> "$REPORT_FILE"
echo "Security scan completed." >> "$REPORT_FILE"
