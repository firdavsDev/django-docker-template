ifneq (,$(wildcard ./.env))
	include .env
	export
	ENV_FILE_PARAM = --env-file .envs
endif


build:
	docker compose -f local.yml up --build --remove-orphans

# ---- Plain-python local run via uv (no Docker; SQLite fallback) ----

venv:
	uv sync --group dev

run-local:
	uv run python manage.py migrate
	uv run python manage.py runserver

lock:
	uv lock
	uv export --no-dev --no-hashes -o requirements/base.txt
	uv export --group dev --no-hashes -o requirements/local.txt
	uv export --extra production --no-dev --no-hashes -o requirements/production.txt

# ---- Docker Compose ----

up:
	docker compose -f local.yml up

down:
	docker compose -f local.yml down

down-v:
	docker compose -f local.yml down -v

logs:
	docker compose -f local.yml logs -f

makemigrations:
	docker compose -f local.yml run --rm django python manage.py makemigrations

migrate:
	docker compose -f local.yml run --rm django python manage.py migrate --no-input

superuser:
	docker compose -f local.yml run --rm django python manage.py createsuperuser

shell:
	docker compose -f local.yml run --rm django python manage.py shell_plus

restart:
	docker compose -f local.yml restart

backup:
	docker compose -f local.yml exec postgres backup

backups:
	docker compose -f local.yml exec postgres backups

copy-backups:
	docker cp $(docker compose -f local.yml ps -q postgres):/backups ./backups

restore:
	docker compose -f local.yml exec postgres restore file_name.sql.gz
