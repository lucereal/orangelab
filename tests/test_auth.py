import json

import nfc.auth


def _write_maps(tmp_path, scanners, rfid_map):
    scanners_path = tmp_path / "scanners.json"
    rfid_path = tmp_path / "rfid_map.json"
    scanners_path.write_text(json.dumps(scanners))
    rfid_path.write_text(json.dumps(rfid_map))
    return scanners_path, rfid_path


def test_authorize_ok(tmp_path, monkeypatch):
    scanners, rfid = _write_maps(
        tmp_path,
        {"1": {"active": True}},
        {"DEADBEEF": {"name": "sleep token"}},
    )
    monkeypatch.setattr(nfc.auth, "_SCANNERS_PATH", scanners)
    monkeypatch.setattr(nfc.auth, "_RFID_MAP_PATH", rfid)

    ok, reason, code = nfc.auth.authorize("DEADBEEF", 1)
    assert ok is True
    assert reason == "ok"
    assert code == nfc.auth.FAILURE_REASONS["NONE"]


def test_authorize_unknown_scanner(tmp_path, monkeypatch):
    scanners, rfid = _write_maps(tmp_path, {}, {"DEADBEEF": {}})
    monkeypatch.setattr(nfc.auth, "_SCANNERS_PATH", scanners)
    monkeypatch.setattr(nfc.auth, "_RFID_MAP_PATH", rfid)

    ok, reason, code = nfc.auth.authorize("DEADBEEF", 9)
    assert ok is False
    assert "scanner" in reason
    assert code == nfc.auth.FAILURE_REASONS["SCANNER_UNKNOWN"]


def test_authorize_inactive_scanner(tmp_path, monkeypatch):
    scanners, rfid = _write_maps(
        tmp_path,
        {"1": {"active": False}},
        {"DEADBEEF": {}},
    )
    monkeypatch.setattr(nfc.auth, "_SCANNERS_PATH", scanners)
    monkeypatch.setattr(nfc.auth, "_RFID_MAP_PATH", rfid)

    ok, _, code = nfc.auth.authorize("DEADBEEF", 1)
    assert ok is False
    assert code == nfc.auth.FAILURE_REASONS["SCANNER_UNKNOWN"]


def test_authorize_unregistered_uid(tmp_path, monkeypatch):
    scanners, rfid = _write_maps(
        tmp_path,
        {"1": {"active": True}},
        {},
    )
    monkeypatch.setattr(nfc.auth, "_SCANNERS_PATH", scanners)
    monkeypatch.setattr(nfc.auth, "_RFID_MAP_PATH", rfid)

    ok, reason, code = nfc.auth.authorize("UNKNOWN", 1)
    assert ok is False
    assert reason == "uid not registered"
    assert code == nfc.auth.FAILURE_REASONS["UNREGISTERED"]
