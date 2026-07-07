# Django Docker Template

Production-ready Django template: Django 5.2 LTS · DRF · PostgreSQL · Redis (cache, sessions, celery) · Celery · uv · Docker Compose · nginx.

## Folder structure

    .
    ├── .envs                   # Environment variables (.local/ + .production(example)/)
    ├── compose                 # Dockerfiles and start/entrypoint scripts
    ├── config                  # Django project (settings/, celery, urls, wsgi/asgi)
    ├── src                     # Apps live in src/apps/<name>/ (account = reference app)
    ├── docs                    # Setup & usage guides
    ├── pyproject.toml          # Dependencies (uv) — uv.lock is the lockfile
    ├── requirements            # Generated exports from uv.lock (do not edit)
    ├── local.yml               # Docker Compose for local development
    ├── production.yml          # Docker Compose for production
    └── Makefile                # Shortcuts for everything below

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (for running without Docker, and for dependency management)
- Docker + Docker Compose (for the containerized setups)

## Quick start

**Without Docker** (SQLite + in-memory cache fallbacks, zero config):

```bash
make venv        # uv sync
make run-local   # migrate + runserver → http://127.0.0.1:8000
```

**With Docker** (full stack: postgres, redis, celery, celery-beat):

```bash
make build       # → http://localhost:8000
```

Useful targets: `make up`, `make down`, `make logs`, `make migrate`, `make makemigrations`, `make superuser`, `make shell`, `make lock` (relock deps after editing pyproject.toml).

## Documentation

- [Setup & run guide](docs/setup-and-run.md) — template setup, local (with/without Docker), production deploy, logs, backups
- [uv & Docker guide](docs/uv-and-docker.md) — dependency management workflow, compose details

API docs (staff login required): http://localhost:8000/api/docs/ · Admin: http://localhost:8000/admin/panel/

## Linting & formatting

[ruff](https://docs.astral.sh/ruff/) handles linting, import sorting, and formatting (config in pyproject.toml):

```bash
uv run pre-commit install         # run on every commit
uv run pre-commit run --all-files # run manually
```

## Production

See [docs/setup-and-run.md](docs/setup-and-run.md#4-production). Short version: fill `.envs/.production/` (copy from `.envs/.production(example)/`, generate secrets with `openssl rand -hex 32`), add TLS certs, then:

```bash
docker compose -f production.yml up -d --build
```

Deployment repo: https://github.com/firdavsDev/docker-template-deployment
