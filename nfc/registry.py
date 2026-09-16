import json
import datetime
from pathlib import Path

_BASE = Path(__file__).parent.parent
_RFID_MAP_PATH = _BASE / "rfid_map.json"
_ACTIONS_PATH = _BASE / "actions.json"


def _parse_time(s):
    h, m = s.split(":")
    return datetime.time(int(h), int(m))


def _in_time_range(start, end, current):
    if start <= end:
        return start <= current <= end
    return current >= start or current <= end


def warn_incomplete_actions():
    with open(_ACTIONS_PATH) as f:
        actions = json.load(f)

    problems = []
    for key, action in actions.items():
        if not isinstance(action, dict):
            problems.append(f"actions.json {key!r} is not an object")
            continue
        if not action.get("id"):
            problems.append(f"actions.json {key!r} is missing id — HA will not run a script")

    for problem in problems:
        print(f"Warning: {problem}")
    return problems


def resolve(uid, scanner_id, now=None):
    if now is None:
        now = datetime.datetime.now()

    current_time = now.time()

    with open(_RFID_MAP_PATH) as f:
        rfid_map = json.load(f)

    with open(_ACTIONS_PATH) as f:
        actions = json.load(f)

    entry = rfid_map.get(uid)
    if not entry:
        return None

    for candidate in entry.get("actions", []):
        entry_scanner = candidate.get("scanner_id")
        if entry_scanner is not None and entry_scanner != scanner_id:
            continue

        time_range = candidate.get("time_range", {})
        start = _parse_time(time_range.get("start", "00:00"))
        end = _parse_time(time_range.get("end", "23:59"))
        if not _in_time_range(start, end, current_time):
            continue

        action_id = str(candidate["action_id"])
        action = actions.get(action_id)
        if action:
            return action

    return None
