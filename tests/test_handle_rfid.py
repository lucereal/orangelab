import handle_rfid


def test_handle_uid_rejects_unregistered(monkeypatch):
    published = {}

    monkeypatch.setattr(
        handle_rfid.nfc.auth,
        "authorize",
        lambda uid, scanner_id: (False, "uid not registered", 1),
    )
    monkeypatch.setattr(
        handle_rfid.mqtt_publisher,
        "publish_unregistered_uid",
        lambda uid, scanner_id, mac=None: published.update(
            {"uid": uid, "scanner_id": scanner_id, "mac": mac}
        ),
    )

    result = handle_rfid.handle_uid("UNKNOWN", scanner_id=1, mac="AA")
    assert result["ok"] is False
    assert result["reason_code"] == 1
    assert published == {"uid": "UNKNOWN", "scanner_id": 1, "mac": "AA"}


def test_handle_uid_mqtt_publishes_action(monkeypatch):
    published = {}
    action = {"label": "Sleep", "type": "script", "id": "sleep"}

    monkeypatch.setattr(
        handle_rfid.nfc.auth,
        "authorize",
        lambda uid, scanner_id: (True, "ok", 0),
    )
    monkeypatch.setattr(
        handle_rfid.nfc.registry,
        "resolve",
        lambda uid, scanner_id: action,
    )
    monkeypatch.setattr(
        handle_rfid.mqtt_publisher,
        "publish_action",
        lambda uid, scanner_id, resolved, mac=None: published.update(
            {"uid": uid, "action": resolved, "mac": mac}
        ),
    )

    result = handle_rfid.handle_uid("DEADBEEF", scanner_id=1, mac="AA")
    assert result == {"ok": True, "action": "sleep", "reason_code": 10}
    assert published["action"] == action


def test_handle_uid_no_action(monkeypatch):
    monkeypatch.setattr(
        handle_rfid.nfc.auth,
        "authorize",
        lambda uid, scanner_id: (True, "ok", 0),
    )
    monkeypatch.setattr(handle_rfid.nfc.registry, "resolve", lambda uid, scanner_id: None)

    result = handle_rfid.handle_uid("DEADBEEF", scanner_id=1)
    assert result["ok"] is False
    assert result["reason"] == "no_action"
