# trialOrange — token dock (Home Assistant)

Internal name: trialOrange. Public name: token dock. See README.md for the kit write-up.

## Architecture

```
Input adapters              Core logic             Output adapters
───────────────────         ──────────────         ──────────────────────
detect_rfid.py  (serial) ─┐                   ┌──→ ha/trigger_script.py  (REST)
rfid_server.py  (http)   ─┼─→ handle_rfid.py ─┤    makeconnection.py     (REST)
mqtt_listener.py (mqtt)  ─┘   source param     └──→ ha/mqtt_publisher.py  (MQTT)
                              routes output
```

## Input adapters

- **`detect_rfid.py`** — reads Arduino RC522 over USB serial (`/dev/ttyACM0`)
- **`rfid_server.py`** — Flask HTTP server, accepts POST `/rfid` with `{"uid": "...", "scanner_id": 1}`
- **`mqtt_listener.py`** — subscribes to `token/dock/scan`, payload `{"uid": "...", "scanner_id": 2}`

## Output routing

| Source  | Output                              |
|---------|-------------------------------------|
| serial  | HA REST API (trigger_script / set_preset) |
| http    | HA REST API (trigger_script / set_preset) |
| mqtt    | MQTT `token/dock/action`            |

## Data files

- `rfid_map.json` — UID → action mappings with time-based rules
- `scanners.json` — active scanner definitions
- `actions.json` — action definitions (scripts and presets)
- `presets/` — light preset configs

## Environment

Copy `.env.example` to `.env`. Used keys: `HOME_LAB_TOKEN`, `MQTT_BROKER`, `MQTT_PORT`, `MQTT_USERNAME`, `MQTT_PASSWORD`, `SCANNER_ID`.
