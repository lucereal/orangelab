# Open items

In-repo review work is done. What is left is on the broker, the docks, and matching HA script ids — this repo cannot apply broker/dock config.

## Remaining

- [ ] Broker: turn anonymous access off
- [ ] Broker: create users `dock`, `listener`, `homeassistant` (or rename to match yours)
- [ ] Broker: load `docs/mosquitto/acl` (HA Mosquitto add-on: Logins + ACL file)
- [ ] Listener `.env`: `MQTT_USERNAME=listener` and that user's password
- [ ] Dock `secrets.h`: dock user/password, then install ArduinoJson v7 and reflash
- [ ] Confirm HA MQTT integration uses the `homeassistant` user (subscribe `token/dock/action` only)
- [x] `actions.json` ids match live HA scripts (`sleep_dave`, `wake_dave`, `evening_dave`)
- [ ] HA automation `action event` still passes `uid` / `scanner_id` as `[object Object]`. Use `trigger.payload_json.uid` and `trigger.payload_json.scanner_id`, or drop those fields if the scripts do not use them. See `docs/home-assistant-config.md`.

## Packaging (other HA users)

See `docs/packaging.md`. Lab automation item above stays open.

Decided: ESPHome + HA only for others. v1 is one dock + one action per token. Arduino, Python, multi-dock, and time windows stay in notes for later.

- [x] Decide default path: ESPHome + HA only
- [x] Decide v1 scope: one dock + one action per token
- [x] Phase 1: ESPHome dock firmware (`esphome/token-dock.yaml`)
- [x] Phase 1: HA blueprint (UID → one script)
- [x] Phase 1: install docs that assume Mosquitto add-on (no listener)
- [ ] Phase 2: HACS integration (add a token, pick a script)

See `docs/mqtt-acls.md`.

## Done (in repo)

### Hardening

- [x] Add tests (auth, registry resolve, time windows, handle_uid routing)
- [x] Drop HTTP `/rfid` and serial adapters
- [x] Document expected MQTT ACLs (`docs/mqtt-acls.md`, `docs/mosquitto/`)
- [x] Firmware result payload parsed with ArduinoJson v7

### Bugs

- [x] Remove leftover `from sre_parse import FAILURE` in `nfc/auth.py`
- [x] Serial UID prefix mismatch — serial path removed
- [x] Time windows wrap midnight (`21:00`–`06:00`)

### Firmware

- [x] Non-blocking LED fade so MQTT/NFC keep running

### Cleanup

- [x] Remove REST leftovers (`makeconnection.py`, `actions/sleep.py`, `actions/wake.py`, `presets/`, HA REST client)
- [x] MQTT-only `handle_uid` and slim `requirements.txt`

### Integration

- [x] HA script ids: startup warning + README note; no live HA call
