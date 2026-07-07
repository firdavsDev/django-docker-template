# Using uv & Docker Compose

This project uses [uv](https://docs.astral.sh/uv/) for Python package management. `pyproject.toml` + `uv.lock` are the source of truth; the `requirements/*.txt` files are auto-generated exports — never edit them by hand.

## 1. uv basics

### Install uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# or: brew install uv
```

### Set up the project (no Docker)

```bash
make venv        # = uv sync --group dev  → creates .venv/ from uv.lock
make run-local   # = migrate + runserver via uv run
```

Zero configuration needed: without `POSTGRES_HOST` the local settings fall back to SQLite (`db.sqlite3`), `SECRET_KEY` gets an insecure dev default, and cronitor is skipped when `CRONITOR_API_KEY` is unset.

Run anything inside the project environment with `uv run`:

```bash
uv run python manage.py makemigrations
uv run python manage.py createsuperuser
uv run python manage.py shell_plus
uv run celery -A config worker -l info   # needs redis running (REDIS_HOST=localhost)
```

### Managing dependencies

```bash
uv add django-model-utils          # add a runtime dependency
uv add --group dev ipython         # add a dev-only dependency
uv add --optional production newrelic   # add to the production extra
uv remove requests                 # remove a dependency
uv lock --upgrade                  # upgrade everything within pyproject constraints
```

After **any** dependency change, regenerate the lock and the exported requirements files:

```bash
make lock
```

This runs `uv lock` plus three `uv export` commands that rewrite `requirements/{base,local,production}.txt`. Commit `pyproject.toml`, `uv.lock`, and the regenerated requirements files together.

### Dependency groups in this project

| Group / extra | Contents | Installed by |
|---|---|---|
| default dependencies | Django, DRF, celery, channels, psycopg, … | always |
| `dev` group | django-debug-toolbar, pre-commit | `uv sync --group dev` (local dev, local Docker image) |
| `production` extra | gunicorn, sentry-sdk, daphne | `uv sync --extra production` (production Docker image) |

## 2. Docker Compose

Both Dockerfiles install dependencies with `uv sync --frozen` straight into the container's system interpreter (`UV_PROJECT_ENVIRONMENT=/usr/local`), so there is no `.venv` inside containers — `python manage.py ...` just works. `--frozen` means the build fails if `uv.lock` is out of date with `pyproject.toml`, so always run `make lock` before building.

### Local development (`local.yml`)

```bash
make build    # build + start django, postgres, redis, celery, celery-beat
make up       # start detached
make logs     # follow logs
make down     # stop
make down-v   # stop + delete volumes (wipes local DB!)
```

App: http://localhost:8000 — code is bind-mounted (`.:/app`), so edits reload without rebuild. Rebuild only when dependencies change:

```bash
make lock && make build
```

One-off commands inside the container:

```bash
docker-compose -f local.yml run --rm django python manage.py makemigrations
make migrate
make superuser
make shell
```

### Production (`production.yml`)

```bash
# one-time on the server: writable log dir for the container user
mkdir -p logs && chmod 777 logs

docker-compose -f production.yml up -d --build
```

Key differences from local:

- **No source bind mount** — code is baked into the image at `/home/app/web`. Deploying a code change requires `--build`.
- `static_volume` / `media_volume` are shared with nginx.
- Redis has **no published port** (internal network only).
- Container stdout logs are capped at 5MB × 5 files per service (`x-logging` anchor).
- Requires `.envs/.production/.django` and `.envs/.production/.postgres` (rename `.envs/.production(example)/` and fill in real values).

### Application logs

Django writes rotating logs (5MB × 5 files each) to `logs/` in the **project root** — `access.log` (request activity, INFO+) and `errors.log` (application errors, ERROR+):

- Local (Docker or plain python): `logs/` appears in the repo automatically.
- Production: `./logs` is bind-mounted into django, celery, and celery-beat containers; the entrypoint chowns it to the container user automatically. Read logs on the host with `tail -f logs/errors.log` — no need to enter containers or volumes.

Container stdout (request logs, celery output) is separate — view with `make logs` / `docker-compose -f production.yml logs -f <service>`.

## 3. Cheat sheet

| Task | Command |
|---|---|
| First-time local setup (no Docker) | `make venv && make run-local` |
| First-time local setup (Docker) | `make build` |
| Add a package | `uv add <pkg>` then `make lock` |
| Upgrade all packages | `uv lock --upgrade && make lock` |
| Run tests / manage.py locally | `uv run python manage.py <cmd>` |
| Run manage.py in Docker | `docker-compose -f local.yml run --rm django python manage.py <cmd>` |
| See app error logs | `tail -f logs/errors.log` |
| Deploy production | `mkdir -p logs && chmod 777 logs && docker-compose -f production.yml up -d --build` |
