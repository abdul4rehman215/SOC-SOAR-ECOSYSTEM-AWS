#!/usr/bin/env bash
set -euo pipefail
DRY_RUN="${DRY_RUN:-true}"
if [ "$DRY_RUN" = "true" ]; then
  echo "DRY_RUN=true; would run wazuh-analysisd -t and restart wazuh-manager"
  exit 0
fi
sudo /var/ossec/bin/wazuh-analysisd -t
sudo systemctl restart wazuh-manager
sudo systemctl status wazuh-manager --no-pager -l | tail -n 20
