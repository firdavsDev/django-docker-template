# Django Docker Template Project Guidelines

## Overview

Reusable Django 5.2 LTS + DRF template using Docker Compose (local development) and uv for dependency management. This is a template for new projects—not a live app. Read `CLAUDE.md` for project context and gotchas.

## App Structure

Apps live in `src/apps/<name>/` with this sub-package layout. Always follow the `account` app as your reference:

```
src/apps/<name>/
  ├── models/              # ORM models, grouped by concern
  │   └── __init__.py      # Re-export for clean imports
  ├── managers/            # Custom QuerySet and Manager classes
  ├── serializers/         # DRF serializers
  ├── services/            # Business logic (NOT in views)
  ├── views/               # Viewsets and APIViews
  ├── urls/                # URL patterns (one module per concern)
  ├── migrations/          # Auto-generated
  ├── __init__.py          # Re-export models, serializers
  ├── apps.py              # name = "src.apps.<name>"
  └── admin.py             # Django admin configuration
```

**Registration:**

- Add to `LOCAL_APPS` in settings: `"src.apps.<name>.apps.<Name>Config"`
- Set `apps.py` name: `name = "src.apps.<name>"`

**URL Wiring Chain:**

1. `config/urls.py` → `src/apps/v1.py` (includes all v1 apps)
2. `src/apps/v1.py` → `src/apps/<name>/__init__.py` (re-exports urls)
3. `src/apps/<name>/__init__.py` → `src/apps/<name>/urls/<name>.py`
4. Each `urls/<name>.py` must set `app_name = "<name>"`

## Code Style & Linting

**Ruff** is the sole linter/formatter (replaces black, isort, flake8, autoflake). Config in `pyproject.toml`:

- Line length: 120
- Includes isort, pyupgrade, and Django rules
- Max complexity: 10

```bash
uv run ruff check --fix    # Fix issues
uv run ruff format          # Format code
pre-commit run --all-files  # Both + other checks
```

Never edit `requirements/*.txt` by hand—these are generated from `pyproject.toml`. After modifying dependencies: `make lock` (runs `uv lock`).

## Development & Deployment

**Environment Defaults:**

- Base settings have safe defaults (SQLite DB, localhost Redis)
- Local: `POSTGRES_HOST`, `REDIS_HOST` unset → SQLite + LocMemCache fallback
- Production: Requires `SECRET_KEY`, `SERVER_IP`, `SERVER_DOMAIN`, `POSTGRES_*`

**Commands (All via Docker Compose via Makefile):**

```bash
make build              # Build + start stack (django, postgres, redis, celery, celery-beat)
make up / make down     # Container lifecycle
make down-v             # Wipe volumes
make logs               # Tail logs
make migrate            # Run migrations
make makemigrations     # Create migrations
make superuser          # Create admin user
make shell              # Django shell_plus
make venv               # Create uv venv locally (no Docker)
make run-local          # Run Django locally (requires venv)
```

**No-Docker Local:** After `make venv`, Django runs with SQLite and insecure defaults—for development only.

## Database & Custom User Model

- Custom user: `account.User` (set as `AUTH_USER_MODEL` in settings)
- Cache + sessions: Redis-backed (DB 1 for sessions; DB 0 for Celery)
- Local fallback: LocMemCache + DB sessions (when `REDIS_HOST` unset)
- Log files: Rotating `logs/access.log` + `logs/errors.log` (5MB × 5)

## Python & Dependencies

- Python 3.12 (Docker image: `python:3.12-slim-bookworm`)
- Dependency manager: **uv** (faster than pip, lock file in version control)
- Source of truth: `pyproject.toml` + `uv.lock`
- Extras: `[production]` for prod, `[dev]` group for development
- Never commit `requirements/*.txt` edits—run `make lock` after pyproject changes

## Project-Specific Patterns

- Settings split: `config/settings/{base,local,production}.py`
- Entrypoint: `manage.py` defaults to `DJANGO_SETTINGS_MODULE=config.settings.local`
- Env files (committed local placeholders): `.envs/.local/{.django,.postgres}`
- Business logic lives in `services/`, not views
- Viewsets preferred over raw APIViews (DRF standard)

## When to Create New Files

- **New App:** Use `/new-app <name>` command (scaffolds structure + wires routing)
- **New Service:** `src/apps/<name>/services/<concern>.py`
- **New Serializer:** `src/apps/<name>/serializers/<model_or_concern>.py`
- **New View:** `src/apps/<name>/views/<concern>.py`

## Gotchas & Common Errors

1. **Migrations tied to app**: Always run from `src.apps.<name>.migrations`; Django auto-detects via app registry
2. **URL wiring broken**: If new app doesn't appear at `/api/v1/`: verify `v1.py` include, check `app_name` is set in app's urls
3. **Custom user not recognized**: Verify `AUTH_USER_MODEL = "account.User"` in `config/settings/base.py`
4. **Redis connection fails locally**: Either start Docker (`make build`) or set `REDIS_HOST` env var; fallback to LocMemCache works without Redis
5. **Dependency issues**: Edit `pyproject.toml`, then `make lock`; never edit `.txt` files directly

## Learn More

- Setup & run: `docs/setup-and-run.md`
- Dependency & Docker: `docs/uv-and-docker.md`
- Deployment: `docs/DEPLOY.md`
- CLAUDE.md: Project context, env gotchas, command reference
