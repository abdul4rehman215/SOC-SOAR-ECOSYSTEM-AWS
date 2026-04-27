# Security Notes and Redaction Policy

This folder is designed for a public GitHub portfolio repository. It intentionally avoids including live secrets.

## Do not commit

Never commit the following:

- `.env.ci` with real tokens or passwords
- private SSH keys
- Slack webhook URLs
- GitHub personal access tokens
- Wazuh API passwords
- TheHive API keys
- n8n credential exports containing actual credential values

## Included instead

This folder includes:

- sanitized n8n workflow skeletons
- `.env.ci.example` with placeholder values
- Wazuh config snippets
- scripts that reference environment variables rather than hardcoded credentials
- PDFs and documentation that explain the MVP

## Before publishing

Review screenshots and PDFs for lab IP addresses or private hostnames if you want the repository to be fully environment-neutral. The workflow JSON files in this package have been sanitized for credential IDs and live endpoint URLs where practical, but PDFs may still show evidence screenshots from the lab.

## Credential remapping after import

After importing workflow JSON files into n8n, re-map:

- GitHub credential
- Slack credential/channel
- TheHive 5 credential
- DataTable selections
- any HTTP URL pointing to your n8n, Wazuh, or TheHive instance

## Why this matters

A security automation project should model safe operational behavior. Redaction and credential hygiene are part of the engineering story, not an afterthought.
