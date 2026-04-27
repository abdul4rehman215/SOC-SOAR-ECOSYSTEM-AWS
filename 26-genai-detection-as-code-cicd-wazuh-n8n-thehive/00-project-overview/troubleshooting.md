# Project Overview Troubleshooting

## Problem: duplicate Slack/TheHive alerts

Cause: more than one Flow C workflow is active on the same `/webhook/wazuh-genai-alerts` path.

Fix: deactivate older Flow C workflows and keep only the latest production workflow active.

## Problem: dashboard rows are not updating

Cause: dashboard collector workflow is inactive, or the HTTP nodes still point to the wrong `/webhook-test/` URL.

Fix: activate `Flow_SOC_Dashboard_Event_Collector_v1` and use `/webhook/soc-dashboard-event` for production.

## Problem: workflow import shows missing credentials

Cause: JSON exports are sanitized and do not include live credentials.

Fix: open each affected node and select the correct GitHub, Slack, TheHive, or DataTable credential/table.

## Problem: TheHive case promotion fails

Cause: the required TheHive case template does not exist or the promote node has an empty template value.

Fix: create `flowc-direct-prompt-injection` and `flowc-indirect-prompt-injection` templates in TheHive and reselect/confirm them in the promote nodes.
