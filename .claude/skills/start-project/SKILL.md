---
name: start-project
description: Turn this Django template into a new project by replacing `name` placeholders (Docker image names, container labels, README) with the real project name. Use when starting a new project from this template.
disable-model-invocation: true
---

Rename this template to project `$ARGUMENTS` (ask for the name if not provided; use snake_case for image names).

## Steps

1. Find all placeholder occurrences first — search for `name_django`, `name_postgres`, `name_redis`, and `{name}`/`name` placeholders in:
   - `local.yml` and `production.yml` (`image:` values like `name_django`, `name_postgres`, `name_redis`)
   - `README.md` (title, clone instructions, project references)
   - `.envs/` files (e.g., `POSTGRES_DB` and other values referencing the template name)
   - Any other hits from a repo-wide grep for the placeholder pattern
2. Show the user the full list of files/lines that will change before editing.
3. Replace placeholders with the project name. Do not touch `container_name: django`/`postgres` style values unless the user wants per-project container names (needed to run multiple projects simultaneously — ask).
4. Remind the user to review `.envs/.local/` secrets (SECRET_KEY, postgres password) and the `.envs/.production(example)/` dir, and to update `TIME_ZONE` in `config/settings/base.py` (currently `Asia/Tashkent`) if needed.
5. Verify: `make build` should bring the stack up at http://localhost:8000.
