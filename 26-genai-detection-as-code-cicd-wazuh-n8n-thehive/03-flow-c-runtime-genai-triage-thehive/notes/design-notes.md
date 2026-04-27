# Flow C Design Notes

Flow C was intentionally built after proving Wazuh ingestion first. The correct order was:

1. Wazuh localfile ingestion
2. Wazuh rules and decoder firing
3. n8n webhook triage
4. Slack notification
5. AI demo app
6. TheHive alert/case handling
7. Dashboard and audit additions

This avoided debugging n8n before confirming the SIEM pipeline was actually producing target alerts.
