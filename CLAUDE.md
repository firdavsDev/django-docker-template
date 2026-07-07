# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

Reusable Django + Docker template, not a live app. `name` placeholders (image names in `local.yml`/`production.yml`, README) get replaced per-project — use `/start-project <name>`. Scaffold new apps with `/new-app <name>`.

## Commands

Everything runs through Docker Compose (`local.yml`), wrapped by the Makefile:

- `make build` — build + run stack (django, postgres, redis, celery, celery-beat) at http://localhost:8000
- `make up` / `make down` / `make down-v` (wipes volumes) / `make logs`
- `make makemigrations` / `make migrate` / `make superuser` / `make shell` (shell_plus)
- One-off commands: `docker-compose -f local.yml run --rm django python manage.py <cmd>` (legacy hyphenated `docker-compose`)
- No-Docker local run: `make venv` (uv sync) then `make run-local` — zero env vars needed (SQLite fallback kicks in when `POSTGRES_HOST` unset; insecure default `SECRET_KEY`; cronitor skipped without `CRONITOR_API_KEY`).
- Dependencies: managed by **uv** — `pyproject.toml` + `uv.lock` are the source of truth (`production` extra, `dev` group). `requirements/*.txt` are generated artifacts — never edit by hand; run `make lock` after changing pyproject.toml.
- Lint/format: **ruff** (config in pyproject.toml — line length 120, isort + pyupgrade + django rules, max-complexity 10). `uv run ruff check --fix` + `uv run ruff format`, or `pre-commit run --all-files`. Replaces black/isort/autoflake/flake8.
- No tests, by design. CI's "pytest" job only builds and runs migrations — do not add test setup unless asked.

## Environment / gotchas

- Python 3.12 (Docker image `python:3.12-slim-bookworm`), Django 5.2 LTS + DRF.
- Settings split: `config/settings/{base,local,production}.py`. `manage.py` defaults `DJANGO_SETTINGS_MODULE` to `config.settings.local`.
- Env files live in `.envs/.local/` (`.django`, `.postgres`). Committed secrets/certs there are intentional local placeholders.
- base/local settings have safe env defaults (SQLite, localhost Redis via `REDIS_HOST`); production.py requires `SECRET_KEY`, `SERVER_IP`, `SERVER_DOMAIN`, `POSTGRES_*` and crashes without them — intentional.
- Cache + sessions are Redis-backed (`cached_db` sessions, Redis DB 1; celery uses DB 0); no-Docker local falls back to LocMemCache + DB sessions.
- App logs: rotating `logs/access.log` + `logs/errors.log` (5MB x 5), config in `config/settings/logging_conf.py`; production bind-mounts `./logs`, entrypoint chowns it (root → gosu django).
- Setup/run guides: `docs/setup-and-run.md`, `docs/uv-and-docker.md`.
- Custom user model: `account.User` (`AUTH_USER_MODEL`).

## Structure conventions

- Apps live in `src/apps/<name>/`, sub-packaged: `models/`, `managers/`, `serializers/`, `services/`, `views/`, `urls/` (one module per concern, re-exported via `__init__.py`). Follow `src/apps/account/` as the reference.
- App registration: full path in `LOCAL_APPS` (`"src.apps.<name>.apps.<Name>Config"`), `apps.py` `name = "src.apps.<name>"`.
- URL wiring chain: `config/urls.py` → `src/apps/v1.py` → `src/apps/<name>/<name>.py` (app-level, sets `app_name`) → `src/apps/<name>/urls/<name>.py`.
- Business logic goes in `services/`, not views.
