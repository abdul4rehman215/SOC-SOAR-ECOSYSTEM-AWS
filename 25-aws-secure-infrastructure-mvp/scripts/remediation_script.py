#!/usr/bin/env python3
"""
Security remediation script for common AWS vulnerabilities
"""

import argparse
import logging

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

session = boto3.Session()
s3_client = session.client("s3")
ec2_client = session.client("ec2")
cloudtrail_client = session.client("cloudtrail")
iam_client = session.client("iam")


def enable_s3_encryption(bucket_name):
    s3_client.put_bucket_encryption(
        Bucket=bucket_name,
        ServerSideEncryptionConfiguration={
            "Rules": [{
                "ApplyServerSideEncryptionByDefault": {
                    "SSEAlgorithm": "AES256"
                }
            }]
        }
    )
    logger.info("Enabled AES256 default encryption on bucket %s", bucket_name)


def restrict_security_group(sg_id, port, allowed_cidr):
    response = ec2_client.describe_security_groups(GroupIds=[sg_id])
    permissions = response["SecurityGroups"][0].get("IpPermissions", [])

    open_permission_found = False
    for permission in permissions:
        from_port = permission.get("FromPort")
        to_port = permission.get("ToPort")
        if from_port == port and to_port == port:
            for ip_range in permission.get("IpRanges", []):
                if ip_range.get("CidrIp") == "0.0.0.0/0":
                    open_permission_found = True
                    try:
                        ec2_client.revoke_security_group_ingress(
                            GroupId=sg_id,
                            IpPermissions=[{
                                "IpProtocol": permission.get("IpProtocol", "tcp"),
                                "FromPort": port,
                                "ToPort": port,
                                "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
                            }]
                        )
                        logger.info("Revoked 0.0.0.0/0 access on port %s for %s", port, sg_id)
                    except ClientError as error:
                        logger.warning("Could not revoke open rule: %s", error)

    try:
        ec2_client.authorize_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=[{
                "IpProtocol": "tcp",
                "FromPort": port,
                "ToPort": port,
                "IpRanges": [{"CidrIp": allowed_cidr, "Description": "Restricted lab access"}]
            }]
        )
        logger.info("Added restricted ingress %s on port %s for %s", allowed_cidr, port, sg_id)
    except ClientError as error:
        if error.response["Error"]["Code"] == "InvalidPermission.Duplicate":
            logger.info("Restricted ingress rule already exists.")
        else:
            raise

    if not open_permission_found:
        logger.info("No open 0.0.0.0/0 rule was found for port %s on %s", port, sg_id)


def enable_cloudtrail_logging(trail_name, bucket_name):
    trails = cloudtrail_client.describe_trails()["trailList"]
    existing_names = [trail["Name"] for trail in trails]

    if trail_name not in existing_names:
        cloudtrail_client.create_trail(
            Name=trail_name,
            S3BucketName=bucket_name,
            IncludeGlobalServiceEvents=True,
            IsMultiRegionTrail=True,
            EnableLogFileValidation=True
        )
        logger.info("Created CloudTrail trail %s", trail_name)
    else:
        cloudtrail_client.update_trail(
            Name=trail_name,
            S3BucketName=bucket_name,
            IncludeGlobalServiceEvents=True,
            IsMultiRegionTrail=True,
            EnableLogFileValidation=True
        )
        logger.info("Updated existing CloudTrail trail %s", trail_name)

    cloudtrail_client.start_logging(Name=trail_name)
    logger.info("Started CloudTrail logging for %s", trail_name)


def enforce_iam_password_policy():
    iam_client.update_account_password_policy(
        MinimumPasswordLength=14,
        RequireSymbols=True,
        RequireNumbers=True,
        RequireUppercaseCharacters=True,
        RequireLowercaseCharacters=True,
        AllowUsersToChangePassword=True,
        MaxPasswordAge=90,
        PasswordReusePrevention=5,
        HardExpiry=False
    )
    logger.info("Enforced strong IAM password policy")


def main():
    parser = argparse.ArgumentParser(description="Remediate common AWS security issues")
    parser.add_argument("--bucket-name", required=True, help="S3 bucket name")
    parser.add_argument("--security-group-id", required=True, help="Security group ID to restrict")
    parser.add_argument("--port", type=int, default=22, help="Port to restrict")
    parser.add_argument("--allowed-cidr", required=True, help="Allowed CIDR after remediation")
    parser.add_argument("--trail-name", required=True, help="CloudTrail trail name")
    args = parser.parse_args()

    enable_s3_encryption(args.bucket_name)
    restrict_security_group(args.security_group_id, args.port, args.allowed_cidr)
    enable_cloudtrail_logging(args.trail_name, args.bucket_name)
    enforce_iam_password_policy()

    logger.info("Remediation complete.")


if __name__ == "__main__":
    main()
