# trialOrange — token dock (Home Assistant)

Internal name: trialOrange. Public name: token dock. See README.md for the kit write-up.

## Architecture

```
ESP32 dock ──MQTT token/dock/scan──► mqtt_listener.py ──► handle_rfid.py
                                                      │
                    ┌─────────────────────────────────┼─────────────────────┐
                    ▼                                 ▼                     ▼
           token/dock/action                 token/dock/result/<id>   token/dock/unregistered
                    │                                 │
                    ▼                                 ▼
              Home Assistant                       dock LED
```

## Data files

- `rfid_map.json` — UID → action mappings with time-based rules
- `scanners.json` — active scanner definitions
- `actions.json` — action definitions (HA script ids)

## Environment

Copy `.env.example` to `.env`. Used keys: `MQTT_BROKER`, `MQTT_PORT`, `MQTT_USERNAME`, `MQTT_PASSWORD`, `SCANNER_ID`.

Broker ACLs: `docs/mqtt-acls.md` and `docs/mosquitto/`.

Packaging: `docs/packaging.md`. HACS vs Docker vs add-on: `docs/hacs.md`.
