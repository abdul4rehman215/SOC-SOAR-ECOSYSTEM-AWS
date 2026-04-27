# Supporting Workflows Troubleshooting

## Error workflow does not fire

n8n error workflows are configured in workflow settings, not with canvas lines. Open each main workflow settings and select the global error workflow.

## Dashboard collector receives nothing

Check whether the collector is active and whether the main workflows use the production webhook URL, not the test webhook URL.

## Closure sync does not find cases

Check TheHive case status labels, tags, sourceRef values, and lookback window.

## Dead-letter Slack does not send

Check Slack credential mapping and channel selection.
