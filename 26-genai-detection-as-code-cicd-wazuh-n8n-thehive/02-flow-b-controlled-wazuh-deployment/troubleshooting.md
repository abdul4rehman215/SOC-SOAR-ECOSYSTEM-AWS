# Flow B Troubleshooting

## Deployment is blocked

Check labels and review state. The workflow expects CI pass, ready-to-deploy, approval, and a valid deploy signal.

## SSH backup fails

Check `DEPLOY_WAZUH_HOST`, SSH key path, port, user, and manager connectivity from the n8n instance.

## Stage succeeds but XML check fails

Inspect the XML file under the staging directory and compare with Wazuh rule/decoder requirements.

## Restart node continues despite error

The restart/postdeploy nodes may be configured with continue-on-error to allow rollback and reporting. Check postdeploy health before assuming success.

## Deployment table row missing

Confirm the final audit node is connected after Slack/GitHub reporting and that `flow_b_deployment_runs` is selected.
