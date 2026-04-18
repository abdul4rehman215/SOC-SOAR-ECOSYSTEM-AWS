#!/usr/bin/env python3
"""
Setup AWS Config for continuous compliance monitoring
"""

import argparse
import json
import logging
import time

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def ensure_config_role(iam_client, role_name="AWSConfigRecorderRole"):
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "config.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }

    try:
        iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description="Role for AWS Config recorder"
        )
        logger.info("Created IAM role %s", role_name)
    except ClientError as error:
        if error.response["Error"]["Code"] != "EntityAlreadyExists":
            raise
        logger.info("IAM role %s already exists", role_name)

    iam_client.attach_role_policy(
        RoleName=role_name,
        PolicyArn="arn:aws:iam::aws:policy/service-role/AWS_ConfigRole"
    )

    role_arn = iam_client.get_role(RoleName=role_name)["Role"]["Arn"]
    return role_arn


def put_rule(config_client, rule_name, source_identifier, input_parameters=None):
    rule = {
        "ConfigRuleName": rule_name,
        "Source": {
            "Owner": "AWS",
            "SourceIdentifier": source_identifier
        }
    }

    if input_parameters:
        rule["InputParameters"] = json.dumps(input_parameters)

    config_client.put_config_rule(ConfigRule=rule)
    logger.info("Configured AWS Config rule: %s", rule_name)


def setup_aws_config(bucket_name, region="us-east-1"):
    session = boto3.Session(region_name=region)
    config_client = session.client("config")
    iam_client = session.client("iam")

    role_arn = ensure_config_role(iam_client)

    config_client.put_configuration_recorder(
        ConfigurationRecorder={
            "name": "default",
            "roleARN": role_arn,
            "recordingGroup": {
                "allSupported": True,
                "includeGlobalResourceTypes": True
            }
        }
    )
    logger.info("Created or updated AWS Config recorder")

    config_client.put_delivery_channel(
        DeliveryChannel={
            "name": "default",
            "s3BucketName": bucket_name
        }
    )
    logger.info("Created or updated AWS Config delivery channel")

    time.sleep(5)

    config_client.start_configuration_recorder(
        ConfigurationRecorderName="default"
    )
    logger.info("Started AWS Config recorder")

    put_rule(config_client, "encrypted-volumes", "ENCRYPTED_VOLUMES")
    put_rule(config_client, "s3-bucket-public-read-prohibited", "S3_BUCKET_PUBLIC_READ_PROHIBITED")
    put_rule(
        config_client,
        "iam-password-policy",
        "IAM_PASSWORD_POLICY",
        {
            "RequireUppercaseCharacters": "true",
            "RequireLowercaseCharacters": "true",
            "RequireSymbols": "true",
            "RequireNumbers": "true",
            "MinimumPasswordLength": "14",
            "MaxPasswordAge": "90",
            "PasswordReusePrevention": "5"
        }
    )
    put_rule(config_client, "cloudtrail-enabled", "CLOUD_TRAIL_ENABLED")

    logger.info("AWS Config setup complete.")


def main():
    parser = argparse.ArgumentParser(description="Set up AWS Config")
    parser.add_argument("--bucket-name", required=True, help="S3 bucket name for Config snapshots")
    parser.add_argument("--region", default="us-east-1", help="AWS region")
    args = parser.parse_args()

    setup_aws_config(args.bucket_name, args.region)


if __name__ == "__main__":
    main()
