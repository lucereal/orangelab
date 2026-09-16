import datetime
import json

import nfc.registry


def _write_maps(tmp_path, rfid_map, actions):
    rfid_path = tmp_path / "rfid_map.json"
    actions_path = tmp_path / "actions.json"
    rfid_path.write_text(json.dumps(rfid_map))
    actions_path.write_text(json.dumps(actions))
    return rfid_path, actions_path


def _patch_paths(monkeypatch, rfid_path, actions_path):
    monkeypatch.setattr(nfc.registry, "_RFID_MAP_PATH", rfid_path)
    monkeypatch.setattr(nfc.registry, "_ACTIONS_PATH", actions_path)


def test_resolve_same_day_window(tmp_path, monkeypatch):
    rfid, actions = _write_maps(
        tmp_path,
        {
            "DEADBEEF": {
                "actions": [
                    {
                        "action_id": 1,
                        "scanner_id": None,
                        "time_range": {"start": "09:00", "end": "17:00"},
                    }
                ]
            }
        },
        {"1": {"label": "Sleep", "type": "script", "id": "sleep"}},
    )
    _patch_paths(monkeypatch, rfid, actions)

    now = datetime.datetime(2026, 9, 16, 12, 0)
    assert nfc.registry.resolve("DEADBEEF", 1, now=now)["id"] == "sleep"
    assert nfc.registry.resolve("DEADBEEF", 1, now=datetime.datetime(2026, 9, 16, 8, 0)) is None


def test_resolve_overnight_window(tmp_path, monkeypatch):
    rfid, actions = _write_maps(
        tmp_path,
        {
            "CAFEBABE": {
                "actions": [
                    {
                        "action_id": 1,
                        "scanner_id": None,
                        "time_range": {"start": "21:00", "end": "06:00"},
                    }
                ]
            }
        },
        {"1": {"label": "Sleep", "type": "script", "id": "sleep"}},
    )
    _patch_paths(monkeypatch, rfid, actions)

    late = datetime.datetime(2026, 9, 16, 22, 0)
    early = datetime.datetime(2026, 9, 16, 5, 0)
    midday = datetime.datetime(2026, 9, 16, 12, 0)
    assert nfc.registry.resolve("CAFEBABE", 1, now=late)["id"] == "sleep"
    assert nfc.registry.resolve("CAFEBABE", 1, now=early)["id"] == "sleep"
    assert nfc.registry.resolve("CAFEBABE", 1, now=midday) is None


def test_resolve_scanner_specific(tmp_path, monkeypatch):
    rfid, actions = _write_maps(
        tmp_path,
        {
            "04AABBCCDDEE01": {
                "actions": [
                    {
                        "action_id": 3,
                        "scanner_id": 1,
                        "time_range": {"start": "00:00", "end": "23:59"},
                    }
                ]
            }
        },
        {"3": {"label": "Evening", "type": "script", "id": "evening"}},
    )
    _patch_paths(monkeypatch, rfid, actions)

    now = datetime.datetime(2026, 9, 16, 12, 0)
    assert nfc.registry.resolve("04AABBCCDDEE01", 1, now=now)["id"] == "evening"
    assert nfc.registry.resolve("04AABBCCDDEE01", 2, now=now) is None


def test_resolve_unknown_uid(tmp_path, monkeypatch):
    rfid, actions = _write_maps(tmp_path, {}, {"1": {"id": "sleep"}})
    _patch_paths(monkeypatch, rfid, actions)
    assert nfc.registry.resolve("MISSING", 1) is None


def test_warn_incomplete_actions(tmp_path, monkeypatch, capsys):
    rfid, actions = _write_maps(
        tmp_path,
        {},
        {"1": {"label": "Sleep", "type": "script", "id": "sleep"}, "2": {"label": "Broken"}},
    )
    _patch_paths(monkeypatch, rfid, actions)

    problems = nfc.registry.warn_incomplete_actions()
    assert len(problems) == 1
    assert "2" in problems[0]
    assert "missing id" in problems[0]
    assert "Warning:" in capsys.readouterr().out
