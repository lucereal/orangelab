# HACS (and how it differs from Docker)

Product shape and phases: `docs/packaging.md`.

**HACS** is the Home Assistant Community Store. It is not part of official
Home Assistant. After a user installs it once, they get a store *inside* HA
for community integrations, Lovelace cards, and themes, with update notices.

Install docs: [hacs.xyz](https://hacs.xyz). Many HA users already have it.

## What a HACS integration is

A custom integration is Python that runs **inside** the Home Assistant
process. The user adds it from HACS (or copies it into
`custom_components/`), then uses **Settings → Devices & services** like any
other integration.

For token dock, that would mean: mappings (UID, dock, time window, script)
live in the HA UI. No venv, no separate container to babysit. HA restart
picks up the integration; backups include its config.

That is a different packaging target than this repo’s `mqtt_listener.py`.
The listener logic could move there later. There is no HACS package in this
repo yet.

## What HACS is not

- Not a replacement for Mosquitto. Users still need an MQTT broker.
- Not a way to flash the ESP32. Firmware stays ESPHome/Arduino (or a
  preflashed dock).
- Not an add-on. Add-ons are **containers** next to HA (Supervisor / HAOS).
  HACS integrations are **Python inside HA**.

## Docker vs HACS vs add-on

Putting `mqtt_listener.py` in Docker **does** help versus a raw venv:

- One image, pinned deps, `restart: unless-stopped`
- Same habit as this lab’s HA compose (`docker/`)
- Env/files mount in; no `pip install` on the host
- A Dockerfile is the usual first step toward a **HA add-on** (add-ons are
  containers with a small wrapper)

It does **not** make the listener HA-native:

- HAOS / supervised users cannot drop an arbitrary compose file next to
  Core. They install add-ons from the HA UI.
- Someone running HA in Docker (this lab) *can* add a `token-dock` service
  beside `homeassistant`. That is a good fit **for this host**, not for
  every HA user.
- They still have a second service to network at the broker, mount
  `rfid_map.json` / `actions.json`, and keep running.

| Package | Who it fits | What they install |
|---------|-------------|-------------------|
| Docker Compose service | People who already run HA (and Mosquitto) in Docker | `docker compose up` |
| HA add-on | HAOS / supervised | Add-on store → start |
| HACS integration | Anyone with HACS | Store → config flow in HA |

**Practical sequence:** Dockerfile for the listener (helps this lab and
Docker users) → optional HA add-on from that image → HACS integration if
the goal is “configure tokens in the HA UI, no extra container.”
