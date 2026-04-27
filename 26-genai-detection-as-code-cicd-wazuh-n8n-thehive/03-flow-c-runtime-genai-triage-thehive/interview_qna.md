# Flow C Interview Q&A

## What makes Flow C an AI security workflow?

It detects and triages AI-specific runtime behaviors: direct prompt injection, indirect prompt injection through retrieved context, and unsafe generated output handling.

## Why use Wazuh instead of only app logic?

The app can detect guardrail issues locally, but Wazuh makes those events visible in a SOC detection pipeline with rules, levels, groups, alert history, and integration hooks.

## What is the dedup key?

The dedup key combines detection family, request ID, and Wazuh rule ID. It is used for TheHive sourceRef, DataTable upsert, and analyst traceability.

## Why not auto-promote every alert to a case?

Alert fatigue. Flow C promotes only risk_score >= 95 with mapped templates. Medium-priority events remain alerts and audit records.
