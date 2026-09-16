# MQTT access (ACLs)

An **ACL** (access control list) is a broker-side allow-list: which MQTT **user** may **publish** or **subscribe** on which **topic**.

This repo cannot enforce that. The dock and listener only connect with a username and password. If the broker allows anonymous clients, or one user can publish every topic, anyone on the network can fake a scan or fire `token/dock/action`.

**Handle it on the broker:**

1. Turn anonymous access off.
2. Create three users: `dock`, `listener`, `homeassistant`.
3. Load the topic grants in `docs/mosquitto/acl`.
4. Put the matching passwords in `arduino/scanner_mqtt/secrets.h` (dock), `.env` (listener), and the Home Assistant MQTT integration.

Copy-paste files: `docs/mosquitto/mosquitto.conf` and `docs/mosquitto/acl`.

## Topics

| Topic | Publisher | Subscriber |
|-------|-----------|------------|
| `token/dock/scan` | dock | listener |
| `token/dock/action` | listener | Home Assistant |
| `token/dock/result/<scanner_id>` | listener | dock |
| `token/dock/unregistered` | listener | optional |

## Create users

```bash
mosquitto_passwd -c /mosquitto/config/passwd dock
mosquitto_passwd /mosquitto/config/passwd listener
mosquitto_passwd /mosquitto/config/passwd homeassistant
```

Home Assistant Mosquitto add-on: use **Logins** for the three users and point the add-on ACL file at the contents of `docs/mosquitto/acl` (rename users if your add-on accounts differ).

If your broker users or topic prefix differ, edit the ACL to match — do not copy these usernames as-is if you already have others.
