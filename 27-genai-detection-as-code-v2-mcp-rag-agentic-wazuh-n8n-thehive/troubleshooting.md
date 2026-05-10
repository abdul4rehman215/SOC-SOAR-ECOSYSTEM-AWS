# 🧯 Master Troubleshooting Guide

## GitHub PR workflows do not trigger

Check that the workflow is published, only one duplicate is active, and GitHub credentials are selected after import.

## n8n workflow is green but no DataTable row appears

Open the DataTable node and verify column types. The most common issue is a Git SHA mapped into a numeric column. Git SHAs must be strings.

## Flow A2 says CI failed with 0/0 stages

The local runner probably could not fetch or read the PR checkout. Validate `.env.ci`, GitHub token/SSH access, and script permissions.

## Flow B2 gate passes but deployment fails

Review the stage result in the GitHub comment. Common causes are SSH quoting, remote path permissions, Wazuh restart permissions, or local staging path permissions.

## Flow C2 sends RAG/MCP events to agentic tables

Use the fixed `Flow_C2_Runtime_GenAI_MCP_RAG_Memory_Agentic_Triage_FIXED_ROUTING.json`. The final fix makes rule ID ranges win over broad Wazuh groups.

## TheHive alert is not promoted to case

Check `case_promotion_eligible`, `thehive_alert_id`, and `thehive_case_template`. Case template names must match TheHive templates.

## Slack posts but row builder loses context

Slack nodes return Slack response objects. The workflow should restore original context after Slack before DataTable writes.
