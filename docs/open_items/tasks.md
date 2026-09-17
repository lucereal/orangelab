# Open items

In-repo review work is done. What is left is on the broker, the docks, and matching HA script ids — this repo cannot apply broker/dock config.

## Remaining

- [ ] Broker: turn anonymous access off
- [ ] Broker: create users `dock`, `listener`, `homeassistant` (or rename to match yours)
- [ ] Broker: load `docs/mosquitto/acl` (HA Mosquitto add-on: Logins + ACL file)
- [ ] Listener `.env`: `MQTT_USERNAME=listener` and that user's password
- [ ] Dock `secrets.h`: dock user/password, then install ArduinoJson v7 and reflash
- [ ] Confirm HA MQTT integration uses the `homeassistant` user (subscribe `token/dock/action` only)
- [ ] `actions.json` ids (`sleep`, `wake`, `evening`) don't match the live HA script entity ids (`script.sleep_dave`, `script.wake_dave`, `script.evening_dave`). The `token/dock/action` automation builds `{{ action.type }}.{{ action.id }}` → calls `script.sleep`, which doesn't exist. Either rename the HA scripts or update `actions.json` ids to match. See `docs/home-assistant-config.md`.

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
