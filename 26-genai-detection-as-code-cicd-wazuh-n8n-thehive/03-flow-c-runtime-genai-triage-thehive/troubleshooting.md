# Flow C Troubleshooting

## Wazuh does not alert

Check the Wazuh agent localfile block, file permissions on `/var/log/ai-demo/guardrail-events.jsonl`, and manager connectivity.

## Wazuh alerts but n8n does not receive anything

Check the Wazuh manager integration block and custom integration script path/permissions.

## Slack duplicates alerts

Deactivate old Flow C workflows using the same webhook path.

## TheHive promotion fails

Confirm case templates exist:

- `flowc-direct-prompt-injection`
- `flowc-indirect-prompt-injection`

Then reselect templates in the promote nodes.

## Dashboard rows missing

Check whether the dashboard collector workflow is active and whether Flow C HTTP node points to `/webhook/soc-dashboard-event`.
