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
- Lint: `pre-commit run --all-files` (autoflake is the only active hook; black/isort are intentionally commented out)
- No tests, by design. CI's "pytest" job only builds and runs migrations — do not add test setup unless asked.

## Environment / gotchas

- Target Python 3.9 (Docker image); CI linter's 3.11 is not the target. Django 3.2 + DRF.
- Settings split: `config/settings/{base,local,production}.py`. `manage.py` reads `DJANGO_SETTINGS_MODULE` from env directly — KeyError if unset (local compose sets `config.settings.local`).
- Env files live in `.envs/.local/` (`.django`, `.postgres`). Committed secrets/certs there are intentional local placeholders.
- Settings KeyError without: `SECRET_KEY`, `DEBUG`, `POSTGRES_HOST/DB/PORT/USER/PASSWORD`. `config/celery.py` reads `CRONITOR_API_KEY` unconditionally — Celery won't start without it set (empty is fine).
- `DEBUG` is read as a raw string, so `"False"` is still truthy — known quirk, don't "fix" without asking.
- Custom user model: `account.User` (`AUTH_USER_MODEL`).

## Structure conventions

- Apps live in `src/apps/<name>/`, sub-packaged: `models/`, `managers/`, `serializers/`, `services/`, `views/`, `urls/` (one module per concern, re-exported via `__init__.py`). Follow `src/apps/account/` as the reference.
- App registration: full path in `LOCAL_APPS` (`"src.apps.<name>.apps.<Name>Config"`), `apps.py` `name = "src.apps.<name>"`.
- URL wiring chain: `config/urls.py` → `src/apps/v1.py` → `src/apps/<name>/<name>.py` (app-level, sets `app_name`) → `src/apps/<name>/urls/<name>.py`.
- Business logic goes in `services/`, not views.
- flake8: `max-complexity = 10`; migrations/templates/scripts excluded. Spellcheck plugin active — add new jargon to `whitelist.txt` if flagged.
