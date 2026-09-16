# Home Assistant Docker Setup

`docker-compose.yml` in this folder is a copy of the live compose file at
`/home/dave/homeassistant/davelab/docker-compose.yml` on the host running
Home Assistant. Keep both in sync if either is edited.

## What it runs

- `ghcr.io/home-assistant/home-assistant:stable`, `restart: unless-stopped`
- `network_mode: host`, config volume at `/home/dave/homeassistant:/config`
- USB/RFKill device passthrough (`/dev/bus/usb`, `/dev/rfkill`) — needed for
  the RFID/Zigbee-type hardware
- `apparmor=unconfined` + `NET_ADMIN` / `SYS_ADMIN` / `NET_RAW` caps

This is a single-container setup (no clustering/failover) — `restart:
unless-stopped` just gets it auto-restarted by the Docker daemon on crash or
host reboot.

## Commands

See [`commands.md`](./commands.md).
