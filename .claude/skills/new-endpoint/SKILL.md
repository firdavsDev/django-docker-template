---
name: new-endpoint
description: Scaffold a new DRF endpoint inside an existing app under src/apps/, following this template's one-endpoint-per-view-module layout (own view module + callable, re-exported via __init__.py, wired into urls/, enveloped via CustomResponseMixin). Use when the user asks to add/create a new API endpoint, view, or route to an existing app.
---

Add a new endpoint to an existing app. Parse `$ARGUMENTS` as `<app> <name>` (both snake_case; `<name>` is the action, e.g. `change_password`, `list_orders`). Derive `PascalCase` for the class. If the app or intent is unclear, ask before scaffolding. Follow `src/apps/account/views/login.py` as the reference — do NOT add the endpoint to an existing view module.

## Steps

1. **View module** `src/apps/<app>/views/<name>.py`:
   - Define `class <Name>APIView(CustomResponseMixin, APIView)` (import `CustomResponseMixin` from `...common.mixins`).
   - Implement the HTTP method(s) — `get`/`post`/`patch`/`delete`. Pattern for write endpoints: build `serializer = self.serializer_class(data=request.data)` → `serializer.is_valid(raise_exception=True)` → call a **service** for business logic → return `self.success(message=..., data=..., status_code=...)`. Read endpoints: serialize and `self.success(...)`.
   - Set `serializer_class`, and `permission_classes` / `authentication_classes` explicitly when the endpoint is public (`(AllowAny,)` + `authentication_classes = ()`); otherwise the global `IsAuthenticated` + JWT default applies.
   - Append the callable: `<name>_api_view = <Name>APIView.as_view()`.

2. **Serializer** (only if the endpoint needs one not already present) `src/apps/<app>/serializers/<name>.py`: define the input/output serializer; add it to `serializers/__init__.py` re-exports (keep `__all__` sorted). Import it in the view from the package root: `from ..serializers import <Name>Serializer`.

3. **Service** (if there is business logic beyond trivial serialization) `src/apps/<app>/services/<name>.py`: put the logic here, not in the view. Raise DRF exceptions (or a `common.exceptions.CustomException` subclass) for error paths — they auto-envelope via `custom_exception_handler`.

4. **Re-export** in `src/apps/<app>/views/__init__.py`: add `from .<name> import <Name>APIView, <name>_api_view` and extend `__all__` (keep sorted).

5. **Wire the route** in `src/apps/<app>/urls/<app>.py`: add a `path("<url-segment>/", view=views.<name>_api_view, name="<name>")` entry (the file already does `from .. import views`). Pick a RESTful url segment.

6. Match existing style (double quotes, trailing commas, import order). Run `uv run ruff check --fix` + `uv run ruff format` on the touched files.

7. Do NOT run migrations. If a new serializer references a new model field, tell the user to run `make makemigrations` then `make migrate`.

## Verify
- `uv run python manage.py check` is clean.
- `reverse("<app>:<name>")` resolves (or hit the route with an `APIClient`), and the response follows the `{status, message, data}` envelope.
