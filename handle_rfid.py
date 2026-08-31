import nfc.auth
import nfc.registry
from ha import mqtt_publisher
from ha.trigger_script import trigger_script
from makeconnection import set_preset


def handle_uid(uid, scanner_id=1, source="serial", mac=None):
    ok, reason, failure_reason = nfc.auth.authorize(uid, scanner_id)
    if not ok:
        print(
            f"Scan rejected [{reason}]: uid={uid} scanner={scanner_id} failure reason={failure_reason}"
        )
        if failure_reason == 1:
            mqtt_publisher.publish_unregistered_uid(uid, scanner_id, mac=mac)
            return {"ok": False, "reason": reason, "reason_code": failure_reason}

        return {"ok": False, "reason": reason, "reason_code": failure_reason}

    action = nfc.registry.resolve(uid, scanner_id)
    if not action:
        print(f"No action matched: uid={uid} scanner={scanner_id}")
        return {"ok": False, "reason": "no_action", "reason_code": failure_reason}

    if source == "mqtt":
        mqtt_publisher.publish_action(uid, scanner_id, action, mac=mac)
        return {"ok": True, "action": action.get("id"), "reason_code": 10}
    elif action["type"] == "preset":
        ok = set_preset(action["name"])
        return {"ok": ok, "action": action.get("id"), "reason_code": 10}
    elif action["type"] == "script":
        ok = trigger_script(action["id"])
        return {"ok": ok, "action": action.get("id"), "reason_code": 10}
    else:
        print(f"Unknown action type: {action['type']}")
        return {"ok": False, "reason": "unknown_action_type", "reason_code": 40}
