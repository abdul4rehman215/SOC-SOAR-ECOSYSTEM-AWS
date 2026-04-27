# Flow B Deployment Scripts

These scripts are run from n8n command nodes to deploy Wazuh content safely.

Order:

1. `backup_current_wazuh_content.sh`
2. `checkout_approved_commit.sh`
3. `stage_new_rules_and_decoders.sh`
4. `predeploy_xml_check.sh`
5. `predeploy_smoke_logtest.sh`
6. `activate_content.sh`
7. `restart_wazuh_manager.sh`
8. `postdeploy_test.py`
9. `rollback_from_backup.sh` when needed

All scripts expect environment variables from `.env.ci` or the n8n runtime environment.
