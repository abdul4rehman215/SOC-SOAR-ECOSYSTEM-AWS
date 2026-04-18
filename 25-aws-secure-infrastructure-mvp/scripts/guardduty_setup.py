#!/usr/bin/env python3
"""
Enable GuardDuty, export findings to S3 with KMS, and send high-severity alerts to SNS.
"""

import argparse
import json
import logging

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def get_detector_id(guardduty_client):
    detector_ids = guardduty_client.list_detectors().get("DetectorIds", [])
    if detector_ids:
        logger.info("Using existing GuardDuty detector %s", detector_ids[0])
        return detector_ids[0]

    response = guardduty_client.create_detector(Enable=True)
    detector_id = response["DetectorId"]
    logger.info("Created GuardDuty detector %s", detector_id)
    return detector_id


def create_kms_key(kms_client, account_id, region, detector_id):
    detector_arn = f"arn:aws:guardduty:{region}:{account_id}:detector/{detector_id}"

    key_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowRootAccountFullAccess",
                "Effect": "Allow",
                "Principal": {"AWS": f"arn:aws:iam::{account_id}:root"},
                "Action": "kms:*",
                "Resource": "*"
            },
            {
                "Sid": "AllowGuardDutyToUseKey",
                "Effect": "Allow",
                "Principal": {"Service": "guardduty.amazonaws.com"},
                "Action": [
                    "kms:GenerateDataKey",
                    "kms:Decrypt",
                    "kms:Encrypt",
                    "kms:ReEncryptFrom",
                    "kms:ReEncryptTo",
                    "kms:DescribeKey"
                ],
                "Resource": "*",
                "Condition": {
                    "StringEquals": {
                        "aws:SourceAccount": account_id
                    },
                    "ArnLike": {
                        "aws:SourceArn": detector_arn
                    }
                }
            }
        ]
    }

    response = kms_client.create_key(
        Description="KMS key for GuardDuty findings export",
        KeyUsage="ENCRYPT_DECRYPT",
        Origin="AWS_KMS",
        Policy=json.dumps(key_policy)
    )

    key_arn = response["KeyMetadata"]["Arn"]
    key_id = response["KeyMetadata"]["KeyId"]

    try:
        kms_client.create_alias(
            AliasName="alias/secure-lab-guardduty-findings",
            TargetKeyId=key_id
        )
    except ClientError:
        pass

    logger.info("Created or using KMS key %s", key_arn)
    return key_arn


def update_bucket_policy(s3_client, bucket_name, account_id, region, detector_id, prefix):
    detector_arn = f"arn:aws:guardduty:{region}:{account_id}:detector/{detector_id}"

    try:
        current_policy = s3_client.get_bucket_policy(Bucket=bucket_name)
        policy = json.loads(current_policy["Policy"])
    except ClientError:
        policy = {"Version": "2012-10-17", "Statement": []}

    statements = policy.get("Statement", [])

    get_bucket_location_statement = {
        "Sid": "AllowGuardDutyGetBucketLocation",
        "Effect": "Allow",
        "Principal": {"Service": "guardduty.amazonaws.com"},
        "Action": "s3:GetBucketLocation",
        "Resource": f"arn:aws:s3:::{bucket_name}",
        "Condition": {
            "StringEquals": {"aws:SourceAccount": account_id},
            "ArnLike": {"aws:SourceArn": detector_arn}
        }
    }

    put_object_statement = {
        "Sid": "AllowGuardDutyPutObject",
        "Effect": "Allow",
        "Principal": {"Service": "guardduty.amazonaws.com"},
        "Action": "s3:PutObject",
        "Resource": f"arn:aws:s3:::{bucket_name}/{prefix}*",
        "Condition": {
            "StringEquals": {
                "aws:SourceAccount": account_id,
                "s3:x-amz-acl": "bucket-owner-full-control"
            },
            "ArnLike": {
                "aws:SourceArn": detector_arn
            }
        }
    }

    existing_sids = {statement.get("Sid") for statement in statements}
    if get_bucket_location_statement["Sid"] not in existing_sids:
        statements.append(get_bucket_location_statement)
    if put_object_statement["Sid"] not in existing_sids:
        statements.append(put_object_statement)

    policy["Statement"] = statements
    s3_client.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(policy))
    logger.info("Updated bucket policy for GuardDuty export on %s", bucket_name)


def create_publishing_destination(guardduty_client, detector_id, bucket_name, kms_key_arn, prefix):
    existing = guardduty_client.list_publishing_destinations(DetectorId=detector_id).get("Destinations", [])
    if existing:
        logger.info("Publishing destination already exists")
        return existing[0]["DestinationId"]

    response = guardduty_client.create_publishing_destination(
        DetectorId=detector_id,
        DestinationType="S3",
        DestinationProperties={
            "DestinationArn": f"arn:aws:s3:::{bucket_name}/{prefix}",
            "KmsKeyArn": kms_key_arn
        }
    )
    destination_id = response["DestinationId"]
    logger.info("Created GuardDuty publishing destination %s", destination_id)
    return destination_id


def create_sns_and_eventbridge(region):
    sns_client = boto3.client("sns", region_name=region)
    events_client = boto3.client("events", region_name=region)

    topic_response = sns_client.create_topic(Name="secure-lab-guardduty-alerts")
    topic_arn = topic_response["TopicArn"]
    logger.info("Created or using SNS topic %s", topic_arn)

    event_pattern = {
        "source": ["aws.guardduty"],
        "detail-type": ["GuardDuty Finding"],
        "detail": {
            "severity": [
                {
                    "numeric": [">=", 7]
                }
            ]
        }
    }

    rule_response = events_client.put_rule(
        Name="secure-lab-guardduty-high-severity",
        EventPattern=json.dumps(event_pattern),
        State="ENABLED",
        Description="Send high-severity GuardDuty findings to SNS"
    )
    rule_arn = rule_response["RuleArn"]

    events_client.put_targets(
        Rule="secure-lab-guardduty-high-severity",
        Targets=[
            {
                "Id": "GuardDutyHighSeveritySNSTarget",
                "Arn": topic_arn
            }
        ]
    )

    topic_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowEventBridgePublish",
                "Effect": "Allow",
                "Principal": {"Service": "events.amazonaws.com"},
                "Action": "sns:Publish",
                "Resource": topic_arn,
                "Condition": {
                    "ArnEquals": {
                        "aws:SourceArn": rule_arn
                    }
                }
            }
        ]
    }

    sns_client.set_topic_attributes(
        TopicArn=topic_arn,
        AttributeName="Policy",
        AttributeValue=json.dumps(topic_policy)
    )

    logger.info("Created EventBridge rule and SNS target for high-severity findings")
    return topic_arn, rule_arn


def main():
    parser = argparse.ArgumentParser(description="Set up GuardDuty export and alerting")
    parser.add_argument("--bucket-name", required=True, help="S3 bucket for findings export")
    parser.add_argument("--region", default="us-east-1", help="AWS region")
    parser.add_argument("--prefix", default="guardduty-findings/", help="S3 prefix for findings")
    args = parser.parse_args()

    sts_client = boto3.client("sts")
    account_id = sts_client.get_caller_identity()["Account"]

    guardduty_client = boto3.client("guardduty", region_name=args.region)
    kms_client = boto3.client("kms", region_name=args.region)
    s3_client = boto3.client("s3", region_name=args.region)

    detector_id = get_detector_id(guardduty_client)
    kms_key_arn = create_kms_key(kms_client, account_id, args.region, detector_id)
    update_bucket_policy(s3_client, args.bucket_name, account_id, args.region, detector_id, args.prefix)
    destination_id = create_publishing_destination(
        guardduty_client,
        detector_id,
        args.bucket_name,
        kms_key_arn,
        args.prefix
    )
    topic_arn, rule_arn = create_sns_and_eventbridge(args.region)

    report = {
        "detector_id": detector_id,
        "kms_key_arn": kms_key_arn,
        "publishing_destination_id": destination_id,
        "sns_topic_arn": topic_arn,
        "eventbridge_rule_arn": rule_arn
    }

    with open("guardduty_setup_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    logger.info("GuardDuty setup complete.")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
