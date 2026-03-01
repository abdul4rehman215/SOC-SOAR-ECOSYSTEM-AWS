#!/var/ossec/framework/python/bin/python3

###########################################################
## Place this file at:
# /var/ossec/integrations/custom-w2thive.py
## Make executable after saving:
# chmod +x /var/ossec/integrations/custom-w2thive.py
###########################################################

import json
import sys
import os
import re
import logging
import uuid
from thehive4py.api import TheHiveApi
from thehive4py.models import Alert, AlertArtifact

###########################################################
# USER CONFIGURATION
###########################################################

# Minimum Wazuh rule level threshold
lvl_threshold = 0

# Suricata severity threshold
suricata_lvl_threshold = 3

debug_enabled = False
info_enabled = True

###########################################################
# LOGGING SETUP
###########################################################

pwd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
log_file = f"{pwd}/logs/integrations.log"

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

if info_enabled:
    logger.setLevel(logging.INFO)

if debug_enabled:
    logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(log_file)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

###########################################################
# MAIN FUNCTION
###########################################################

def main(args):

    alert_file_location = args[1]
    thive_api_key = args[2]
    thive_url = args[3]

    thive_api = TheHiveApi(thive_url, thive_api_key)

    w_alert = json.load(open(alert_file_location))

    alt = flatten_json(w_alert, '', [])
    formatted_description = markdown_format(alt)

    artifacts_dict = detect_artifacts(formatted_description)

    alert = generate_alert(formatted_description, artifacts_dict, w_alert)

    # Threshold filtering
    if w_alert['rule']['groups'] == ['ids', 'suricata']:
        if 'data' in w_alert and 'alert' in w_alert['data']:
            if int(w_alert['data']['alert']['severity']) <= suricata_lvl_threshold:
                send_alert(alert, thive_api)
    elif int(w_alert['rule']['level']) >= lvl_threshold:
        send_alert(alert, thive_api)

###########################################################
# JSON FLATTENING
###########################################################

def flatten_json(data, prefix, alt):
    for key, value in data.items():
        if hasattr(value, 'keys'):
            flatten_json(value, prefix + '.' + str(key), alt)
        else:
            alt.append(prefix + '.' + str(key) + '|||' + str(value))
    return alt

###########################################################
# FORMAT DESCRIPTION FOR THEHIVE
###########################################################

def markdown_format(alt):

    md_title_dict = {}
    formatted = ""

    for entry in alt:
        entry = entry[1:]
        dot = entry.split('|||')[0].find('.')

        if dot == -1:
            md_title_dict.setdefault(entry.split('|||')[0], []).append(entry)
        else:
            md_title_dict.setdefault(entry[0:dot], []).append(entry)

    for section in md_title_dict.keys():
        formatted += f"### {section.capitalize()}\n"
        formatted += "| Key | Value |\n|------|-------|\n"

        for item in md_title_dict[section]:
            key, val = item.split('|||')
            formatted += f"| **{key}** | {val} |\n"

    return formatted

###########################################################
# ARTIFACT DETECTION
###########################################################

def detect_artifacts(formatted_description):

    artifacts_dict = {}

    artifacts_dict['ip'] = re.findall(r'\d+\.\d+\.\d+\.\d+', formatted_description)

    artifacts_dict['url'] = re.findall(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        formatted_description
    )

    artifacts_dict['domain'] = []

    for url in artifacts_dict['url']:
        artifacts_dict['domain'].append(url.split('//')[1].split('/')[0])

    return artifacts_dict

###########################################################
# GENERATE THEHIVE ALERT
###########################################################

def generate_alert(description, artifacts_dict, w_alert):

    source_ref = str(uuid.uuid4())[0:6]
    artifacts = []

    if 'agent' not in w_alert:
        w_alert['agent'] = {'id': 'no agent id', 'name': 'no agent name', 'ip': 'no agent ip'}
    elif 'ip' not in w_alert['agent']:
        w_alert['agent']['ip'] = 'no agent ip'

    for key, values in artifacts_dict.items():
        for value in values:
            artifacts.append(AlertArtifact(dataType=key, data=value))

    alert = Alert(
        title=w_alert['rule']['description'],
        tlp=2,
        tags=[
            'wazuh',
            f"rule={w_alert['rule']['id']}",
            f"agent_name={w_alert['agent']['name']}",
            f"agent_id={w_alert['agent']['id']}",
            f"agent_ip={w_alert['agent']['ip']}"
        ],
        description=description,
        type='wazuh_alert',
        source='wazuh',
        sourceRef=source_ref,
        artifacts=artifacts
    )

    return alert

###########################################################
# SEND ALERT TO THEHIVE
###########################################################

def send_alert(alert, thive_api):

    response = thive_api.create_alert(alert)

    if response.status_code == 201:
        logger.info("TheHive alert created successfully")
    else:
        logger.error(f"Failed to create alert: {response.status_code} - {response.text}")

###########################################################
# ENTRY POINT
###########################################################

if __name__ == "__main__":
    try:
        main(sys.argv)
    except Exception as e:
        logger.exception("Integration error occurred")

###########################################################
## ✅ What This Script Does

# ✔ Reads Wazuh JSON alert
# ✔ Converts it into formatted markdown
# ✔ Extracts artifacts (IP, URL, domain)
# ✔ Applies severity thresholds
# ✔ Sends alert to TheHive via API
# ✔ Logs result
###########################################################
