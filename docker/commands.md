# Docker Commands

Run from this directory (`docker/`), or add `-f docker/docker-compose.yml`
from elsewhere.

## List containers

```bash
docker ps                                # running containers
docker ps -a                             # all containers, including stopped
docker ps --filter name=homeassistant    # just the homeassistant container
```

## Compose lifecycle

```bash
docker compose up -d              # start (detached)
docker compose down               # stop
docker compose restart            # restart
docker compose ps                 # status
```

## Logs / health

```bash
docker compose logs -f homeassistant                       # follow logs
docker inspect --format '{{.State.Status}}' homeassistant   # health / state
docker events --filter container=homeassistant --since 1h  # recent events
```

## Shell / update

```bash
docker exec -it homeassistant bash   # shell into the container
docker compose pull                  # pull latest image
docker compose up -d                 # recreate with the pulled image
```
