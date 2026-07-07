# Setup & Run Guide

How to turn this template into a project and run it locally (with or without Docker) and in production.

Stack: Python 3.12 · Django 5.2 LTS · DRF · PostgreSQL · Redis (cache, sessions, celery broker) · Celery · uv · Docker Compose · nginx (prod).

## 1. Initial template setup

1. Clone and rename:

   ```bash
   git clone <this-repo> myproject && cd myproject
   ```

2. Replace the `name` placeholders (image names `name_django` / `name_postgres` / `name_redis` in `local.yml` + `production.yml`, values in `.envs/`). With Claude Code just run `/start-project myproject`.

3. Review `.envs/.local/.django` and `.envs/.local/.postgres` — committed values are dev-only placeholders; change `SECRET_KEY` and the postgres password for anything beyond local dev.

4. Adjust `TIME_ZONE` in `config/settings/base.py` (default `Asia/Tashkent`) if needed.

## 2. Run locally WITHOUT Docker (fastest)

Needs only [uv](https://docs.astral.sh/uv/) (`brew install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`).

```bash
make venv        # uv sync — installs everything from uv.lock into .venv/
make run-local   # migrate + runserver on http://127.0.0.1:8000
```

No env vars, no services required. Without `POSTGRES_HOST` set, local settings automatically fall back to:

- **SQLite** (`db.sqlite3`) instead of PostgreSQL
- **In-memory cache** + DB sessions instead of Redis
- Insecure default `SECRET_KEY`

Useful commands:

```bash
uv run python manage.py createsuperuser
uv run python manage.py shell_plus
uv run python manage.py makemigrations
```

Want real Postgres/Redis without Docker? Run them natively and export `POSTGRES_HOST=localhost`, `POSTGRES_DB=...`, `POSTGRES_USER=...`, `POSTGRES_PASSWORD=...`, `REDIS_HOST=localhost`.

## 3. Run locally WITH Docker

Needs Docker + Docker Compose. Uses `local.yml`: django (runserver, hot-reload via `.:/app` bind mount), postgres, redis, celery worker, celery-beat.

```bash
make build       # build images + start stack (foreground)
# or
make up          # start detached
make logs        # follow container logs
```

App: http://localhost:8000 · Admin: http://localhost:8000/admin/panel/ · API docs: http://localhost:8000/api/docs/

Day-to-day:

```bash
make migrate           # apply migrations
make makemigrations
make superuser
make shell             # shell_plus inside the container
make down              # stop
make down-v            # stop + DELETE volumes (wipes DB)
```

Code changes reload automatically. Rebuild only after dependency changes: `make lock && make build`.

## 4. Production

Uses `production.yml`: django (gunicorn), postgres, redis (no public port), nginx (80/443, serves static/media, TLS), celery, celery-beat.

### One-time server setup

```bash
git clone <repo> && cd <repo>

# real production env files (required — django won't start without them)
cp -r ".envs/.production(example)" .envs/.production
# edit .envs/.production/.django  → SECRET_KEY, DEBUG=False, SERVER_IP, SERVER_DOMAIN, SENTRY_DSN
# edit .envs/.production/.postgres → real DB name/user/password, POSTGRES_HOST=postgres

# TLS certs for nginx (see compose/production/nginx/)
```

Required env vars in production (startup crashes without them — intentional): `SECRET_KEY`, `SERVER_IP`, `SERVER_DOMAIN`, `POSTGRES_HOST/DB/PORT/USER/PASSWORD`.

### Deploy / redeploy

```bash
docker compose -f production.yml up -d --build
```

Code is baked into the image (no source bind mount) — every code change needs `--build`. The start script runs `collectstatic` + `migrate` automatically.

### Logs

Application logs live in `./logs/` at the project root on the host (bind-mounted, rotating 5MB × 5 files each):

```bash
tail -f logs/access.log   # request activity
tail -f logs/errors.log   # application errors
```

The container entrypoint chowns `./logs` automatically (starts as root, then drops to the `django` user via gosu). Container stdout is capped at 5MB × 5 files per service:

```bash
docker compose -f production.yml logs -f django
```

### Backups

```bash
make backup        # create postgres backup
make backups       # list backups
make copy-backups  # copy backups out of the container
make restore       # restore (edit file name in Makefile)
```

## 5. Dependency changes (any environment)

```bash
uv add <package>            # or: uv add --group dev / --optional production
make lock                   # regenerate uv.lock + requirements/*.txt
make build                  # rebuild Docker images if you use them
```

See [uv-and-docker.md](./uv-and-docker.md) for the full uv guide.
