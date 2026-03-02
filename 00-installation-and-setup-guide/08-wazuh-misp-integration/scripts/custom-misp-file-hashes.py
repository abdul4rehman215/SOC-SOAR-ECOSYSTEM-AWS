#!/var/ossec/framework/python/bin/python3
# ==============================================================
# WAZUH ↔ MISP FILE HASH INTEGRATION SCRIPT
# Author: Abdul Rehman (SOC Lab)
# Based on official MISP integration concept
# License: AGPL-3.0
# ==============================================================

import json
import os
import sys
import urllib3
from socket import AF_UNIX, SOCK_DGRAM, socket

# Disable SSL warnings (for self-signed lab environments only)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --------------------------------------------------------------
# Exit Codes
# --------------------------------------------------------------
ERR_NO_REQUEST_MODULE = 1
ERR_BAD_ARGUMENTS = 2
ERR_BAD_HASHES = 3
ERR_NO_RESPONSE_MISP = 4
ERR_SOCKET_OPERATION = 5
ERR_FILE_NOT_FOUND = 6
ERR_INVALID_JSON = 7

# --------------------------------------------------------------
# Import requests safely
# --------------------------------------------------------------
try:
    import requests
except Exception:
    print("Missing requests module")
    sys.exit(ERR_NO_REQUEST_MODULE)

# --------------------------------------------------------------
# Global Configuration
# --------------------------------------------------------------
debug_enabled = False
timeout = 10
retries = 3

pwd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
LOG_FILE = f"{pwd}/logs/integrations.log"
SOCKET_ADDR = f"{pwd}/queue/sockets/queue"

ALERT_INDEX = 1
APIKEY_INDEX = 2
MISP_URL_INDEX = 3


# --------------------------------------------------------------
# Debug Logger
# --------------------------------------------------------------
def debug(message):
    if debug_enabled:
        with open(LOG_FILE, "a") as f:
            f.write(message + "\n")


# --------------------------------------------------------------
# Main Entry
# --------------------------------------------------------------
def main(args):
    global debug_enabled

    if len(args) < 4:
        sys.exit(ERR_BAD_ARGUMENTS)

    if len(args) > 4 and args[4] == "debug":
        debug_enabled = True

    process_args(args)


# --------------------------------------------------------------
# Process Arguments
# --------------------------------------------------------------
def process_args(args):
    alert_file = args[ALERT_INDEX]
    api_key = args[APIKEY_INDEX]
    misp_url = args[MISP_URL_INDEX]

    alert = get_json_alert(alert_file)

    result = request_misp_info(alert, misp_url, api_key)

    if result:
        send_msg(result, alert.get("agent"))


# --------------------------------------------------------------
# Extract Hashes and Query MISP
# --------------------------------------------------------------
def request_misp_info(alert, misp_url, api_key):
    if "syscheck" not in alert:
        return None

    syscheck = alert["syscheck"]
    hashes = {}

    if "md5_after" in syscheck:
        hashes["md5"] = syscheck["md5_after"]

    if "sha1_after" in syscheck:
        hashes["sha1"] = syscheck["sha1_after"]

    if "sha256_after" in syscheck:
        hashes["sha256"] = syscheck["sha256_after"]

    if not hashes:
        sys.exit(ERR_BAD_HASHES)

    data = query_api(hashes, misp_url, api_key)

    attributes = data.get("response", {}).get("Attribute")

    if not attributes:
        return None

    attr = attributes[0]

    return {
        "integration": "misp_file_hashes",
        "misp_file_hashes": {
            "found": 1,
            "type": attr["type"],
            "value": attr["value"],
            "event_uuid": attr["Event"]["uuid"],
            "attribute_uuid": attr["uuid"],
            "permalink": f"{misp_url}/events/view/{attr['Event']['uuid']}"
        }
    }


# --------------------------------------------------------------
# MISP REST API Query
# --------------------------------------------------------------
def query_api(hashes, misp_url, api_key):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": api_key,
    }

    payload = {
        "value": list(hashes.values()),
        "type": list(hashes.keys()),
        "to_ids": 1,
        "limit": 1
    }

    try:
        response = requests.post(
            f"{misp_url}/attributes/restSearch",
            headers=headers,
            json=payload,
            timeout=timeout,
            verify=False  # Disable only in lab
        )
    except requests.exceptions.RequestException:
        sys.exit(ERR_NO_RESPONSE_MISP)

    if response.status_code != 200:
        return {
            "integration": "misp_file_hashes",
            "misp_file_hashes": {
                "error": response.status_code,
                "description": response.text
            }
        }

    return response.json()


# --------------------------------------------------------------
# Send Message Back to Wazuh
# --------------------------------------------------------------
def send_msg(message, agent=None):
    if not agent or agent.get("id") == "000":
        string = f"1:misp_file_hashes:{json.dumps(message)}"
    else:
        location = f"[{agent['id']}] ({agent['name']})"
        string = f"1:{location}->misp_file_hashes:{json.dumps(message)}"

    try:
        sock = socket(AF_UNIX, SOCK_DGRAM)
        sock.connect(SOCKET_ADDR)
        sock.send(string.encode())
        sock.close()
    except Exception:
        sys.exit(ERR_SOCKET_OPERATION)


# --------------------------------------------------------------
# Load Alert JSON
# --------------------------------------------------------------
def get_json_alert(path):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        sys.exit(ERR_FILE_NOT_FOUND)
    except json.JSONDecodeError:
        sys.exit(ERR_INVALID_JSON)


# --------------------------------------------------------------
# Script Execution
# --------------------------------------------------------------
if __name__ == "__main__":
    main(sys.argv)
