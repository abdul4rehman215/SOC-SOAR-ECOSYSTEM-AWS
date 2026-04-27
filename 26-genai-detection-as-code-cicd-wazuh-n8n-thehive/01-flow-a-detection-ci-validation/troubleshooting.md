# Flow A Troubleshooting

## Flow A does not trigger

Check that the GitHub trigger is active and subscribed to pull request events. Only opened, reopened, and synchronize actions are allowed.

## PR comments fail

Check GitHub token/credential scope. The workflow needs permission to create issue comments and labels.

## XML validation fails unexpectedly

Run the validator locally against the changed manifest. Confirm the Wazuh XML root elements and custom rule IDs are valid.

## Replay harness fails

Confirm Wazuh API variables are set in `.env.ci`, including API URL, username, password, TLS setting, logtest format, and location.

## Stage result rows missing

Confirm `Code_Build_FlowA_Stage_Result_Rows` is connected from `Code_CI_Decision` and that `flow_a_ci_stage_results` table mapping is selected.
