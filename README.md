# Token dock (Home Assistant NFC POC)

A lab kit: a physical NFC token sits on a dock. The dock reads the tag over I2C, publishes the scan over MQTT, and Home Assistant runs **your** automations. No phone, no companion app.

This is a working proof of concept, not a product.

```
NFC token
    │
    ▼
ESP32 + PN532 dock  ──MQTT──►  token/dock/scan
                                   │
                                   ▼
                          mqtt_listener.py
                                   │
                    ┌──────────────┼──────────────┐
                    ▼              ▼              ▼
           token/dock/action   token/dock/result/<id>
                    │              │
                    ▼              ▼
              Home Assistant    dock LED
```

## Hardware

The MQTT dock sketch (`arduino/scanner_mqtt`) is built around:

| Part | Role |
|------|------|
| ESP32 | Wi-Fi + MQTT client |
| PN532 | NFC reader (I2C) |
| WS2812B strip | Result LED (GPIO 4, 25 LEDs in the sketch) |

Typical I2C wiring on ESP32: SDA → GPIO 21, SCL → GPIO 22. Confirm I2C jumpers on the PN532 module.

## MQTT topics

| Topic | Direction | Purpose |
|-------|-----------|---------|
| `token/dock/scan` | dock → listener | Raw scan |
| `token/dock/action` | listener → Home Assistant | Resolved action |
| `token/dock/result/<scanner_id>` | listener → dock | LED feedback |
| `token/dock/unregistered` | listener → optional | Unknown UID |

`scanner_id` is an integer you assign per dock. The same token can map to different actions on different docks.

### `token/dock/scan`

Published by the ESP32.

```json
{"uid": "DEADBEEF", "scanner_id": 1, "mac": "AA:BB:CC:DD:EE:FF"}
```

`uid` is required. `scanner_id` overrides the listener’s `SCANNER_ID` env default. `mac` is optional (the firmware includes the ESP32 Wi-Fi MAC).

### `token/dock/action`

Published when a registered token matches an action. Home Assistant should subscribe here.

```json
{
  "uid": "DEADBEEF",
  "scanner_id": 1,
  "action": {"label": "Sleep", "type": "script", "id": "sleep"},
  "mac": "AA:BB:CC:DD:EE:FF"
}
```

`action.id` is the script entity suffix you define in Home Assistant (`script.sleep` in this example). Replace it with **your** script ids.

### `token/dock/result/<scanner_id>`

```json
{"scanner_id": 1, "ok": true, "action": "sleep", "reason_code": 10}
```

Firmware LED colors:

| `reason_code` | Meaning | LED |
|---------------|---------|-----|
| `10` | Action matched | green |
| `1` | UID not registered | orange |
| anything else | rejected / no match | red |

## Example configs (fake data)

Replace these with your own UIDs, docks, and script ids.

**`scanners.json`** — every dock the listener will accept. A scan from an unknown or `active: false` dock is rejected.

**`actions.json`** — script ids you create in Home Assistant. This checkout maps to `sleep_dave` / `wake_dave` / `evening_dave` to match the live HA scripts. Use **your** script ids on another install.

**`rfid_map.json`** — UID → action rules. `scanner_id: null` on an action means “any dock.” A numeric `scanner_id` means that action only fires on that dock.

The checked-in examples demonstrate tag + dock uniqueness:

| Example UID | Dock | Action |
|-------------|------|--------|
| `DEADBEEF` | any | Sleep |
| `CAFEBABE` | any | Wake |
| `04AABBCCDDEE01` | scanner `1` only | Evening |
| `04AABBCCDDEE02` | scanner `2` only | Wake until 20:59, Sleep from 21:00 |

Read a token’s UID from the ESP32 serial monitor, then put **your** hex UID in `rfid_map.json`.

## Home Assistant

1. Run an MQTT broker with passwords and topic ACLs (see `docs/mqtt-acls.md`). Enable the MQTT integration. Do not leave the broker anonymous — a client that can publish `token/dock/scan` or `token/dock/action` can trigger your automations.
2. Create **your own** scripts (Settings → Automations & Scenes → Scripts). Name them whatever you want (`script.goodnight`, `script.office_on`, …).
3. Put those script ids (the part after `script.`) into `actions.json`. A typo still publishes `token/dock/action`; Home Assistant will miss. The listener does not call HA to check — it only warns at startup if an entry has no `id`.
4. Add an automation that listens on `token/dock/action` and calls the script in the payload:

```yaml
alias: Token dock → script
trigger:
  - platform: mqtt
    topic: token/dock/action
action:
  - service: script.turn_on
    target:
      entity_id: "script.{{ trigger.payload_json.action.id }}"
```

## Python listener

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:

```
MQTT_BROKER=YOUR_MQTT_BROKER_HOST
MQTT_PORT=1883
MQTT_USERNAME=listener
MQTT_PASSWORD=your_mqtt_password
SCANNER_ID=1
```

Use the **listener** user from `docs/mosquitto/acl`, not the dock user.

```bash
python mqtt_listener.py
```

The listener subscribes to `token/dock/scan`, looks up `rfid_map.json` / `actions.json` / `scanners.json`, then publishes `token/dock/action` and `token/dock/result/<scanner_id>`.

Smoke-test without hardware (use your broker host and credentials):

```bash
mosquitto_sub -h YOUR_MQTT_BROKER_HOST -t token/dock/action -t 'token/dock/result/#'
mosquitto_pub -h YOUR_MQTT_BROKER_HOST -t token/dock/scan \
  -m '{"uid":"DEADBEEF","scanner_id":1}'
```

## Flash the ESP32 dock

Arduino IDE (ESP32 board package installed):

1. Install libraries: **PN532** (Seeed / elechouse — you need `PN532` and `PN532_I2C`), **PubSubClient**, **FastLED**, **ArduinoJson** (v7).
2. Open `arduino/scanner_mqtt/scanner_mqtt.ino`.
3. Copy `arduino/scanner_mqtt/secrets.h.example` to `arduino/scanner_mqtt/secrets.h` (gitignored). Use the **dock** user from `docs/mosquitto/acl`.
4. Select your ESP32 board and port, then Upload.
5. Serial monitor at 9600 baud: Wi-Fi connect, PN532 found, then `Card: …` on a tap.

`secrets.h` must never be committed. Only the `.example` file is in git.

## Repo layout

| Path | Role |
|------|------|
| `arduino/scanner_mqtt/` | ESP32 dock firmware |
| `mqtt_listener.py` | MQTT input adapter |
| `handle_rfid.py` | Auth + action resolve + output routing |
| `ha/mqtt_publisher.py` | Publishes action / result / unregistered |
| `nfc/` | `scanners.json` + `rfid_map.json` lookup |
| `rfid_map.json` / `scanners.json` / `actions.json` | Your mappings (examples only) |
| `.env.example` | Listener environment template |
| `docs/mqtt-acls.md` | Why broker ACLs matter |
| `docs/mosquitto/` | Copy-paste Mosquitto conf + ACL |
| `docs/packaging.md` | How we package this for other HA users |
| `docs/hacs.md` | HACS vs Docker vs add-on |

Internal notes may still say `trialOrange`. The public name for this kit is **token dock**.
