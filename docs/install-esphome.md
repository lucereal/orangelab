# Install token dock (ESPHome + Home Assistant)

v1: one dock, one action per token. You already run Home Assistant. You do
not run `mqtt_listener.py`. Your PC OS (Windows, macOS, Linux) only
matters for the browser and the USB cable.

Lab Arduino + Python path: README.md and `docs/packaging.md`.

## What you need

- Home Assistant **OS or Supervised** (so you have the Add-on store). HA
  Container / Docker-only on Windows does **not** have Mosquitto or
  ESPHome add-ons — use the HA machine that already has Supervisor.
- **Mosquitto** add-on and the **MQTT** integration
- **ESPHome** add-on
- Chrome or Edge (Web Serial). Firefox will not flash from the browser.
- Hardware: ESP32, PN532 (I2C), optional WS2812B strip on GPIO 4
- USB cable that carries data (not charge-only)

Typical I2C: SDA → GPIO 21, SCL → GPIO 22. Set the PN532 I2C jumpers
(usually switch 1 ON, switch 2 OFF).

## Windows notes

- First flash: plug the ESP32 into **this PC**. In ESPHome click
  **Install → Plug into this computer**. Windows may need a USB-UART
  driver (CP210x or CH340, depending on the board).
- `.local` names often fail on Windows and on ESP32. In `secrets.yaml`
  set `mqtt_broker` to the HA machine's **LAN IP** (example
  `192.168.1.50`), not `homeassistant.local` and not `core-mosquitto`.
- You do not need `openssl` or `mosquitto_sub` on Windows. Generate the
  API key in the ESPHome UI (or any base64 32-byte key). Listen for
  scans in **Settings → Devices & services → MQTT → Configure → Listen
  to a topic** → `token/dock/scan`.
- Blueprint file: File Editor / Studio Code Server in HA, or Samba
  `\\HOMEASSISTANT\config\blueprints\automation\`. Do not look for
  `/config` on the Windows disk.

## 1. MQTT

If Mosquitto is not installed: **Settings → Add-ons → Mosquitto broker →
Install → Start**. Then **Settings → Devices & services → MQTT** and
connect it.

Create an MQTT user the dock can use (Mosquitto add-on **Logins**). You
already have MQTT; a three-user ACL is optional — see `docs/mqtt-acls.md`.

## 2. Flash the dock

1. On the HA machine: install the **ESPHome** add-on. Open it from a
   Chrome or Edge window (Windows is fine).
2. New device, or paste / copy `esphome/token-dock.yaml` into the
   add-on's config (`/config/esphome/` on the HA host).
3. Copy `esphome/secrets.yaml.example` to `secrets.yaml` next to it. Set
   Wi-Fi, MQTT broker (**HA LAN IP**), MQTT user, API encryption key,
   OTA password.
4. Plug the ESP32 into this PC. **Install → Plug into this computer**
   and pick the COM port.

On a tap, ESPHome logs something like `Found new tag '74-10-37-94'`. The
dock publishes MQTT `token/dock/scan` with `"uid":"74103794"` (hyphens
stripped, uppercase). The strip flashes green when a tag is read.

## 3. Blueprint

Copy
`homeassistant/blueprints/automation/token_dock_run_script.yaml` to
`/config/blueprints/automation/` on the HA host (File Editor, Studio
Code Server, or Samba). Reload automations or restart HA.

**Settings → Automations → Create automation → Token dock — run a script.**

- **Token UID:** the hex from the log or from MQTT (`74103794` or
  `74-10-37-94`).
- **Script:** one of **your** scripts.

One automation per token. Repeat for each tag.

## 4. Smoke test

In HA: **MQTT → Listen to a topic** → `token/dock/scan`. Tap a token.
You should see `{"uid":"...","scanner_id":1}`. The blueprint automation
should run the script.

Optional, if you have a Mosquitto client:

```bash
mosquitto_sub -h YOUR_HA_HOST -t token/dock/scan -u YOUR_MQTT_USER -P YOUR_MQTT_PASSWORD
```

## Pins (defaults)

| Part | Pin / notes |
|------|-------------|
| PN532 SDA | GPIO 21 |
| PN532 SCL | GPIO 22 |
| WS2812B data | GPIO 4 (25 LEDs in the yaml) |

Change `led_pin`, `num_leds`, and `scanner_id` in the substitutions at the
top of `esphome/token-dock.yaml`.
