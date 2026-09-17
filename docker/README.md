# Home Assistant Docker Setup

Reference compose for a single Home Assistant container. On the HA host, set
`HA_CONFIG_DIR` to that machine's config directory (do not commit the live path).

```bash
# docker/.env (gitignored) or export before compose
HA_CONFIG_DIR=/path/to/homeassistant/config
```

Keep this file and the host compose in sync if either is edited.

## What it runs

- `ghcr.io/home-assistant/home-assistant:stable`, `restart: unless-stopped`
- `network_mode: host`, config volume from `HA_CONFIG_DIR`
- USB/RFKill device passthrough (`/dev/bus/usb`, `/dev/rfkill`) — needed for
  the RFID/Zigbee-type hardware
- `apparmor=unconfined` + `NET_ADMIN` / `SYS_ADMIN` / `NET_RAW` caps

This is a single-container setup (no clustering/failover) — `restart:
unless-stopped` just gets it auto-restarted by the Docker daemon on crash or
host reboot.

## Commands

See [`commands.md`](./commands.md).
