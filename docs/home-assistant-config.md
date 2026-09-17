# Home Assistant & MQTT broker — live config reference

Snapshot of the actual infra this project talks to, pulled from the HA host
for reference. Credentials are placeholders — never commit real values here.

## MQTT broker

Mosquitto, run via Docker Compose from `~/lab/mosquitto/` (separate repo/host
path, not this one).

```yaml
services:
  mosquitto:
    image: eclipse-mosquitto
    container_name: mosquitto
    restart: unless-stopped
    ports:
      - "1883:1883"
    volumes:
      - ./config:/mosquitto/config
      - ./data:/mosquitto/data
      - ./log:/mosquitto/log
```

`mosquitto.conf`:

```
listener 1883
allow_anonymous false
password_file /mosquitto/config/passwd
persistence true
persistence_location /mosquitto/data/
log_dest file /mosquitto/log/mosquitto.log
```

- Auth is required (`allow_anonymous false`) — user/password created via
  `mosquitto_passwd`, stored in `config/passwd` (not this repo).
- Set `MQTT_BROKER` / `MQTT_PORT` / `MQTT_USERNAME` / `MQTT_PASSWORD` in your
  local `.env` (see `.env.example`) to point at this broker. Never put the
  real host/credentials in git.
- In HA: **Settings → Devices & Services → MQTT** integration, broker host is
  the machine running the Mosquitto container (not `localhost` — HA runs in
  its own container).

## HA automation (`automations.yaml`)

The live automation that bridges MQTT → HA scripts:

```yaml
- id: '1772950006733'
  alias: action event
  description: ''
  triggers:
    - trigger: mqtt
      options:
        topic: token/dock/action
  conditions: []
  actions:
    - action: '{{ trigger.payload_json.action.type }}.{{ trigger.payload_json.action.id }}'
      metadata: {}
      data:
        uid: '[object Object]'
        scanner_id: '[object Object]'
  mode: single
```

Builds the HA service call dynamically from the MQTT payload's
`action.type` + `action.id` (e.g. `script.sleep_dave`). This is why the
`actions.json` ids must exactly match real HA script entity ids — see the
mismatch noted in `docs/open_items/tasks.md`.

## HA scripts (`scripts.yaml`, relevant subset)

```yaml
wake_dave:
  alias: wake dave
  sequence:
    - action: switch.turn_on
      target:
        entity_id:
          - switch.sunroom_ps_plug_2
          - switch.sunroom_ps_plug_1
        device_id: 68e2f565ee4cf546ff5db11b014d7dd2

sleep_dave:
  alias: sleep dave
  sequence:
    - action: light.turn_off
      target:
        device_id:
          - e600f3d0834639409a8e16c130f8273e
    - action: switch.turn_off
      target:
        entity_id:
          - switch.sunroom_ps_plug_2
          - switch.sunroom_ps_plug_1
        device_id: 68e2f565ee4cf546ff5db11b014d7dd2

evening_dave:
  alias: evening dave
  sequence:
    - action: switch.turn_on
      target:
        entity_id:
          - switch.sunroom_ps_plug_2
          - switch.sunroom_ps_plug_1
    - action: switch.turn_on
      target:
        device_id: 68e2f565ee4cf546ff5db11b014d7dd2
```

`actions.json` currently maps to ids `sleep` / `wake` / `evening`, but the
real script entities are `script.sleep_dave` / `script.wake_dave` /
`script.evening_dave` — this is the mismatch tracked in
`docs/open_items/tasks.md`.
