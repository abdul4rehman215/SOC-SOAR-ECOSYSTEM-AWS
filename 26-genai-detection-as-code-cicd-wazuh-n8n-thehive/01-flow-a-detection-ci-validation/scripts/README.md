# Flow A Scripts

These scripts are executed by n8n command nodes during Flow A.

- `validate_wazuh_xml.py` validates Wazuh XML and rule ID range expectations.
- `validate_sigma.py` validates Sigma YAML and optionally invokes sigma-cli if available.
- `validate_metadata.py` checks required metadata fields and mapping consistency.
- `stage_validation_wazuh.sh` stages validation content on the Wazuh manager.
- `run_replay_harness.py` calls Wazuh logtest/replay logic for expected rule validation.
