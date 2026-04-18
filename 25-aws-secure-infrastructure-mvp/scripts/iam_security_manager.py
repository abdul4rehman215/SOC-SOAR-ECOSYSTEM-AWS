#!/usr/bin/env python3
"""
AWS IAM Security Manager
Manages IAM roles and policies following security best practices.
"""

import json
import logging
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class IAMSecurityManager:
    def __init__(self, region="us-east-1"):
        self.region = region
        self.iam_client = boto3.client("iam")
        self.sts_client = boto3.client("sts")
        self.account_id = self.sts_client.get_caller_identity()["Account"]

    def _get_local_policy_arn(self, policy_name):
        paginator = self.iam_client.get_paginator("list_policies")
        for page in paginator.paginate(Scope="Local"):
            for policy in page["Policies"]:
                if policy["PolicyName"] == policy_name:
                    return policy["Arn"]
        return None

    def create_security_policy(self, policy_name, policy_document, description="Custom security policy"):
        try:
            response = self.iam_client.create_policy(
                PolicyName=policy_name,
                PolicyDocument=json.dumps(policy_document),
                Description=description,
                Tags=[
                    {"Key": "ManagedBy", "Value": "IAMSecurityManager"},
                    {"Key": "Environment", "Value": "secure-lab"},
                ],
            )
            policy_arn = response["Policy"]["Arn"]
            logger.info("Created policy: %s", policy_arn)
            return policy_arn
        except ClientError as error:
            if error.response["Error"]["Code"] == "EntityAlreadyExists":
                policy_arn = self._get_local_policy_arn(policy_name)
                logger.info("Policy already exists, using existing ARN: %s", policy_arn)
                return policy_arn
            raise

    def create_security_role(self, role_name, trust_policy, description=""):
        try:
            response = self.iam_client.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                Description=description,
                MaxSessionDuration=3600,
                Tags=[
                    {"Key": "ManagedBy", "Value": "IAMSecurityManager"},
                    {"Key": "Environment", "Value": "secure-lab"},
                ],
            )
            role_arn = response["Role"]["Arn"]
            logger.info("Created role: %s", role_arn)
            return role_arn
        except ClientError as error:
            if error.response["Error"]["Code"] == "EntityAlreadyExists":
                role_arn = self.iam_client.get_role(RoleName=role_name)["Role"]["Arn"]
                logger.info("Role already exists, using existing ARN: %s", role_arn)
                return role_arn
            raise

    def attach_policy_to_role(self, role_name, policy_arn):
        self.iam_client.attach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
        logger.info("Attached policy %s to role %s", policy_arn, role_name)

    def create_ec2_security_role(self):
        role_name = "SecureEC2Role"
        policy_name = "SecureEC2Policy"
        instance_profile_name = "SecureEC2InstanceProfile"

        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": {"Service": "ec2.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }]
        }

        role_arn = self.create_security_role(
            role_name,
            trust_policy,
            description="Least-privilege EC2 role for CloudWatch and encrypted S3 access"
        )

        policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AllowCloudWatchMetricsAndLogs",
                    "Effect": "Allow",
                    "Action": [
                        "cloudwatch:PutMetricData",
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents"
                    ],
                    "Resource": "*"
                },
                {
                    "Sid": "AllowEncryptedS3ObjectAccess",
                    "Effect": "Allow",
                    "Action": ["s3:GetObject", "s3:PutObject"],
                    "Resource": "arn:aws:s3:::secure-lab-*/*",
                    "Condition": {
                        "StringEquals": {
                            "s3:x-amz-server-side-encryption": "AES256"
                        }
                    }
                },
                {
                    "Sid": "ExplicitDenyDangerousActions",
                    "Effect": "Deny",
                    "Action": [
                        "iam:*",
                        "ec2:TerminateInstances",
                        "s3:DeleteBucket"
                    ],
                    "Resource": "*"
                }
            ]
        }

        policy_arn = self.create_security_policy(
            policy_name,
            policy_document,
            description="Least-privilege policy for EC2 instances"
        )
        self.attach_policy_to_role(role_name, policy_arn)

        try:
            self.iam_client.create_instance_profile(
                InstanceProfileName=instance_profile_name,
                Tags=[
                    {"Key": "ManagedBy", "Value": "IAMSecurityManager"},
                    {"Key": "Environment", "Value": "secure-lab"},
                ],
            )
            logger.info("Created instance profile: %s", instance_profile_name)
        except ClientError as error:
            if error.response["Error"]["Code"] != "EntityAlreadyExists":
                raise
            logger.info("Instance profile already exists: %s", instance_profile_name)

        profile = self.iam_client.get_instance_profile(
            InstanceProfileName=instance_profile_name
        )["InstanceProfile"]
        existing_roles = [role["RoleName"] for role in profile.get("Roles", [])]

        if role_name not in existing_roles:
            try:
                self.iam_client.add_role_to_instance_profile(
                    InstanceProfileName=instance_profile_name,
                    RoleName=role_name
                )
                logger.info("Added role %s to instance profile %s", role_name, instance_profile_name)
            except ClientError as error:
                logger.warning("Could not add role to instance profile: %s", error)

        return {
            "role_name": role_name,
            "role_arn": role_arn,
            "policy_name": policy_name,
            "policy_arn": policy_arn,
            "instance_profile_name": instance_profile_name,
            "policy_document": policy_document
        }

    def create_security_audit_role(self):
        role_name = "SecurityAuditRole"
        extras_policy_name = "SecurityAuditExtrasPolicy"

        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": {"AWS": f"arn:aws:iam::{self.account_id}:root"},
                "Action": "sts:AssumeRole",
                "Condition": {
                    "Bool": {"aws:MultiFactorAuthPresent": "true"}
                }
            }]
        }

        role_arn = self.create_security_role(
            role_name,
            trust_policy,
            description="Security auditing role that requires MFA"
        )

        managed_policy_arn = "arn:aws:iam::aws:policy/SecurityAudit"
        self.attach_policy_to_role(role_name, managed_policy_arn)

        extras_policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AllowReadOnlySecurityServices",
                    "Effect": "Allow",
                    "Action": [
                        "config:Describe*",
                        "config:Get*",
                        "config:List*",
                        "guardduty:Get*",
                        "guardduty:List*",
                        "guardduty:Describe*",
                        "cloudtrail:Describe*",
                        "cloudtrail:Get*",
                        "cloudtrail:List*",
                        "logs:Describe*",
                        "logs:Get*",
                        "sns:Get*",
                        "sns:List*"
                    ],
                    "Resource": "*"
                }
            ]
        }

        extras_policy_arn = self.create_security_policy(
            extras_policy_name,
            extras_policy_document,
            description="Additional read-only access for security visibility"
        )
        self.attach_policy_to_role(role_name, extras_policy_arn)

        return {
            "role_name": role_name,
            "role_arn": role_arn,
            "managed_policy_arn": managed_policy_arn,
            "extras_policy_name": extras_policy_name,
            "extras_policy_arn": extras_policy_arn,
            "trust_policy": trust_policy,
            "extras_policy_document": extras_policy_document
        }

    def analyze_policy_security(self, policy_document):
        issues = []
        statements = policy_document.get("Statement", [])
        if isinstance(statements, dict):
            statements = [statements]

        sensitive_actions = {
            "s3:PutObject",
            "sts:AssumeRole",
            "kms:Decrypt",
            "iam:PassRole"
        }

        for index, statement in enumerate(statements, start=1):
            effect = statement.get("Effect", "Allow")
            actions = statement.get("Action", [])
            resources = statement.get("Resource", [])
            principal = statement.get("Principal")

            if isinstance(actions, str):
                actions = [actions]
            if isinstance(resources, str):
                resources = [resources]

            if "*" in actions:
                issues.append(f"Statement {index}: wildcard Action '*' found")

            for action in actions:
                if action.endswith(":*"):
                    issues.append(f"Statement {index}: service wildcard action '{action}' found")
                if action in sensitive_actions and "Condition" not in statement and effect == "Allow":
                    issues.append(f"Statement {index}: sensitive action '{action}' has no Condition")

            if "*" in resources and effect == "Allow":
                issues.append(f"Statement {index}: wildcard Resource '*' found in Allow statement")

            if principal == "*" or principal == {"AWS": "*"}:
                issues.append(f"Statement {index}: overly permissive Principal found")

        return issues


def main():
    manager = IAMSecurityManager()

    ec2_role_result = manager.create_ec2_security_role()
    audit_role_result = manager.create_security_audit_role()

    analysis = {
        "SecureEC2Policy": manager.analyze_policy_security(ec2_role_result["policy_document"]),
        "SecurityAuditTrustPolicy": manager.analyze_policy_security(audit_role_result["trust_policy"]),
        "SecurityAuditExtrasPolicy": manager.analyze_policy_security(audit_role_result["extras_policy_document"]),
    }

    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "account_id": manager.account_id,
        "region": manager.region,
        "created_resources": {
            "ec2_role": ec2_role_result,
            "audit_role": audit_role_result
        },
        "policy_analysis": analysis
    }

    with open("iam_security_report.json", "w", encoding="utf-8") as report_file:
        json.dump(report, report_file, indent=2)

    print("\nIAM setup complete.")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
