import nfc.auth
import nfc.registry
from ha import mqtt_publisher


def handle_uid(uid, scanner_id=1, mac=None):
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

    mqtt_publisher.publish_action(uid, scanner_id, action, mac=mac)
    return {"ok": True, "action": action.get("id"), "reason_code": 10}
