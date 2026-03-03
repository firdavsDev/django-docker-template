ifneq (,$(wildcard ./.env))
	include .env
	export
	ENV_FILE_PARAM = --env-file .envs
endif


build:
	docker compose -f local.yml up --build --remove-orphans

up:
	docker compose -f local.yml up -d

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
