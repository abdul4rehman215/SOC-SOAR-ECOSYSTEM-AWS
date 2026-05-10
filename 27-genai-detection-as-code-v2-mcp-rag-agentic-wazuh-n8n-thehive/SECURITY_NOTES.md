# 🔐 Security Notes

This folder is prepared as a GitHub-ready portfolio artifact. It intentionally does **not** include live secrets.

## 🚫 Do not commit

- GitHub personal access tokens
- Slack webhooks
- TheHive API keys
- Wazuh API passwords
- private SSH keys
- `.env.ci`
- real customer/user data
- production IPs or credentials

## ✅ Included safely

- `.env.ci.example` with placeholder values
- n8n workflow JSON exports without embedded tokens
- scripts and test fixtures
- Wazuh rules/decoders
- sample DataTable schemas and evidence CSVs
- project PDFs and documentation

## 🧪 Lab-only warning

This prototype is designed for controlled lab validation. It simulates AI runtime security events and safe mock actions. Production usage requires proper threat modeling, access control, secret management, hardened deployment runners, and formal change approval.

## 🔁 If real secrets were used during testing

Rotate them before publishing the repository.
