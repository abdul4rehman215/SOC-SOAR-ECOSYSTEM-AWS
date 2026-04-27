# Flow B Design Notes

The workflow uses GitHub as the approval surface and Wazuh as the deployment target. The n8n canvas acts as the release orchestrator. Script nodes perform the risky operations, while code nodes parse results and generate human-readable reports.
