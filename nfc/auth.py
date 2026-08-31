import json
from pathlib import Path
from sre_parse import FAILURE

_BASE = Path(__file__).parent.parent
_SCANNERS_PATH = _BASE / "scanners.json"
_RFID_MAP_PATH = _BASE / "rfid_map.json"

FAILURE_REASONS = {"UNREGISTERED": 1, "UNKNOWN": 2, "SCANNER_UNKNOWN": 3, "NONE": 0}


def authorize(uid, scanner_id):
    with open(_SCANNERS_PATH) as f:
        scanners = json.load(f)

    scanner = scanners.get(str(scanner_id))
    if not scanner or not scanner.get("active"):
        return False, "scanner inactive or unknown", FAILURE_REASONS["SCANNER_UNKNOWN"]

    with open(_RFID_MAP_PATH) as f:
        rfid_map = json.load(f)

    if uid not in rfid_map:
        return False, "uid not registered", FAILURE_REASONS["UNREGISTERED"]

    return True, "ok", FAILURE_REASONS["NONE"]
