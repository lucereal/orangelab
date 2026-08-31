import sys
import requests
from pathlib import Path
import json
sys.path.insert(0, str(Path(__file__).parent.parent))
from ha.client import headers, HA_URL

BASE_URL = f"{HA_URL}/api/services/script"


def trigger_script(script_id):
    data={"entity_id": f"script.{script_id}"}
    response = requests.post(
        f"{BASE_URL}/turn_on",
        headers=headers,
        data=json.dumps(data)
        )
    ok = response.status_code == 200
    if ok:
        print(f"trigger {script_id} → Status: {response.status_code}")
    else:
        print(f"trigger {script_id} → Status: {response.status_code} — {response.text}")
    return ok


if __name__ == "__main__":
    trigger_script(sys.argv[1])
