import json
import os
import sys
from pathlib import Path

import requests

from ha.client import HA_URL, headers

BASE_URL = f"{HA_URL}/api/services/light"
ENTITY = os.getenv("HA_LIGHT_ENTITY", "light.your_lamp")


def set_preset(preset_name):
    if preset_name == "off":
        response = requests.post(
            f"{BASE_URL}/turn_off", headers=headers, json={"entity_id": ENTITY}
        )
        print(f"turn_off → Status: {response.status_code}")
    else:
        preset_path = Path(__file__).parent / "presets" / f"{preset_name}.json"
        with open(preset_path) as f:
            preset = json.load(f)

        # Step 1: turn on
        requests.post(
            f"{BASE_URL}/turn_on", headers=headers, json={"entity_id": ENTITY}
        )

        # Step 2: set color
        color_keys = {"rgb_color", "color_temp_kelvin", "hs_color", "xy_color"}
        color = {k: v for k, v in preset.items() if k in color_keys}
        if color:
            requests.post(
                f"{BASE_URL}/turn_on",
                headers=headers,
                json={"entity_id": ENTITY, **color},
            )

        # Step 3: set brightness
        brightness_keys = {"brightness", "brightness_pct"}
        brightness = {k: v for k, v in preset.items() if k in brightness_keys}
        if brightness:
            response = requests.post(
                f"{BASE_URL}/turn_on",
                headers=headers,
                json={"entity_id": ENTITY, **brightness},
            )
            print(f"Status: {response.status_code}")


if __name__ == "__main__":
    set_preset(sys.argv[1])
