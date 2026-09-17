# Packaging token dock for other Home Assistant users

Audience: people who already run HA. They can add ESPHome or a HACS
integration. They will not stand up Arduino IDE + a Python venv +
Mosquitto ACLs + three JSON files + a hand-written automation.

**Goal:** token on a dock → their scripts run. No phone.

HACS vs Docker vs add-on: `docs/hacs.md`.

## Decisions (locked)

1. **Default path for others: ESPHome + Home Assistant only.**
   The dock is an ESPHome device. HA owns the mapping and runs the script.
   No required Python listener, no Arduino IDE, no `secrets.h`.
2. **v1 scope: one dock + one action per token.**
   A UID maps to one script. No per-dock rules and no time windows in v1.

Yes: ESPHome + HA only is the recommended default. HA users already flash
ESPHome and already have MQTT. Arduino + Python is more power, more
install, worse first hour.

## Recommended shape (v1)

Keep hardware simple. Move brains into HA.

- **ESPHome firmware** — Wi-Fi and MQTT from the ESPHome / HA flow. Result
  LED is an ESPHome light (or on-board status).
- **HA owns the registry** — UID → one script. Phase 1: blueprint (and
  docs). Phase 2: HACS UI. No JSON required.
- **Blueprint** — token scanned → `script.<id>` they chose. They do not
  paste MQTT YAML.
- **MQTT** — assume they already have a broker (Mosquitto add-on is fine).
  ACL three-user setup is documented, not the install.

## Later (not v1)

Keep these in notes. Do not build them into the default install.

| Later | Where it lives today |
|-------|----------------------|
| Arduino + `secrets.h` firmware | `arduino/scanner_mqtt/` |
| Python listener + JSON maps | `mqtt_listener.py`, `rfid_map.json`, `scanners.json`, `actions.json` |
| Docker sidecar for the listener | `docs/hacs.md` (Compose / add-on path) |
| Multi-dock (same token, different script per dock) | `rfid_map.json` `scanner_id` rules |
| Time windows (including overnight) | `nfc/registry.py` `_in_time_range` |
| Three-user Mosquitto ACL | `docs/mqtt-acls.md`, `docs/mosquitto/` |
| Preflashed hardware kit | Phase 3 |

Lab leftover: HA automation `action event` still passes `[object Object]`
for `uid` / `scanner_id`. Stays open on `docs/open_items/tasks.md`.

## Do not do this in v1

- Do not ask them to run a venv (or a required listener container).
- Do not make Mosquitto ACL the install. Document it; default to “you
  already have MQTT.”
- Do not ship household script ids (`sleep_dave`) as the public example.
  Public maps stay fake (`sleep` / `wake`). Lab `actions.json` may keep
  live ids.
- Do not lead with hardware sales. Lead with “flash this ESP32, add the
  blueprint.”

## Phases

| Phase | What they get |
|-------|----------------|
| **Now (lab)** | This repo: Arduino + Python + JSON. Your house. |
| **1 — HA-native install** | ESPHome dock + blueprint + docs assuming Mosquitto add-on. One dock, one action per token. |
| **2 — UI** | HACS integration: add a token, pick a script. Still one action per token unless we reopen scope. |
| **3 — kit** | Preflashed dock, if we ever ship hardware. |

Phase 1 is the first packageable thing. Phase 2 is Tuesday-night usable.
