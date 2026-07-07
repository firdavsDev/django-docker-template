---
name: new-app
description: Scaffold a new Django app under src/apps/ following this template's sub-package layout (models/, managers/, serializers/, services/, views/, urls/) and wire it into settings and v1 URLs. Use when the user asks to create/add a new Django app.
---

Create a new Django app named `$ARGUMENTS` (snake_case; derive `PascalCase` for the config class) following the `src/apps/account/` reference layout exactly.

## Steps

1. Create `src/apps/<name>/` with:
   - `__init__.py`
   - `apps.py` — `class <Name>Config(AppConfig)` with `default_auto_field = "django.db.models.BigAutoField"` and `name = "src.apps.<name>"`
   - `admin.py` (empty registrations, just the import)
   - `migrations/__init__.py`
   - Sub-packages, each with `__init__.py` re-exporting its module: `models/<name>.py`, `managers/<name>.py`, `serializers/<name>.py`, `services/` (empty init), `views/<name>.py`, `urls/<name>.py`
   - `<name>.py` at app root — app-level URL module: sets `app_name = "<name>"` and includes `("src.apps.<name>.urls.<name>", "src.apps.<name>.urls.<name>")` with `namespace="<name>"`, mirroring `src/apps/account/account.py`

2. Register in `config/settings/base.py` `LOCAL_APPS`: `"src.apps.<name>.apps.<Name>Config"`.

3. Wire into `src/apps/v1.py`: add a `path("<name>/", include(("src.apps.<name>.<name>", "src.apps.<name>.<name>"), namespace="<name>"))` entry, mirroring the existing `account/` entry.

4. Match existing code style in the account app (imports, double quotes, trailing commas). Business logic belongs in `services/`, not views.

5. Do NOT run migrations automatically. Tell the user to run `make makemigrations` then `make migrate` once they add model fields.
