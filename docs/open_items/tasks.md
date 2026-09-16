# Open items

From the repo review. Lab-grade kit; these are the rough edges.

## Hardening

- [ ] Add tests (auth, registry resolve, time windows, handle_uid routing)
- [ ] Auth on Flask `/rfid` (or bind it locally / drop the HTTP path)
- [ ] MQTT topic access depends entirely on broker config — document expected ACLs
- [ ] Replace firmware `indexOf("\"reason_code\":")` JSON parse with a real parser or a simpler payload

## Bugs

- [ ] Remove leftover `from sre_parse import FAILURE` in `nfc/auth.py`
- [ ] Serial path mismatch: RC522 sketch prints `UID: AABBCCDD`; `detect_rfid.py` passes the whole line into `handle_uid`
- [ ] Time windows do not wrap midnight (`21:00`–`06:00` never matches because of `start <= now <= end`)

## Firmware

- [ ] `flashFade` blocks the ESP32 loop (~2s), so MQTT/NFC polling pauses during the LED flash

## Cleanup

- [ ] REST leftovers still in the tree: `makeconnection.py`, `actions/sleep.py`, `actions/wake.py`, `presets/`
- [ ] `HA_URL` in `ha/client.py` is hardcoded to `http://localhost:8123`

## Integration

- [ ] HA script ids in `actions.json` are not validated against a live instance — wrong id publishes successfully, then HA misses
