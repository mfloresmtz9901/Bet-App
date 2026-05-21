# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Football analysis/betting app built with Django 6 + Django Ninja (REST API). Uses Cookiecutter Django as the base, with Docker for all local development.

## Development Commands

All local development runs through Docker. The `justfile` wraps `docker-compose.local.yml`:

```bash
just up          # Start all containers (Django, Postgres, Redis, Celery)
just down        # Stop containers
just build       # Rebuild images
just logs        # Tail logs (append service name to filter, e.g. just logs django)
just manage <cmd>  # Run any manage.py command inside the container
```

**Without Docker** (using the local `.venv` with `uv`):

```bash
uv run python manage.py runserver        # Dev server
uv run pytest                            # Run all tests
uv run pytest bet_app/apps/users/tests/api/test_views.py  # Run a single test file
uv run pytest -k "test_name"             # Run tests matching a pattern
uv run coverage run -m pytest && uv run coverage html  # Coverage report
uv run mypy bet_app                      # Type checking
uv run ruff check .                      # Lint
uv run ruff format .                     # Format
```

Tests use `config.settings.test` and `--reuse-db` by default (configured in `pyproject.toml`).

## Architecture

### App layout

All custom apps live under `bet_app/apps/`:
- `users` — custom `AbstractUser` with `user_type` field (Free/Premium/Admin). Handles both Django-Allauth session auth and JWT cookie auth (`JWTAuthRequired` in `auth.py`).
- `core_data` — reference data synced from an external football API: `Country`, `League`, `Seasons`, `Venue`, `Teams`, `LeagueParticipation`. Models carry a `remote_id` field that maps to the upstream API's IDs.
- `matches` — match data (empty, in progress).

### API layer (`Django Ninja`)

The single `NinjaAPI` instance lives in `config/api.py`. It uses `SessionAuth` globally and restricts the auto-generated docs to staff users. Each app exposes a `Router` and registers it there:

```
/api/users/   → bet_app.apps.users.api.views.router
```

Ninja schemas (request/response shapes) go in `<app>/api/schema.py`. The `users` app also has a legacy `schemas.py` at the app root — new code should use `api/schema.py`.

### Settings

Three-layer settings in `config/settings/`:
- `base.py` — shared config. Reads env vars via `django-environ`.
- `local.py` — adds `debug_toolbar`, `django_extensions`; Celery runs eagerly.
- `test.py` — used by pytest (`--ds=config.settings.test`).
- `production.py` — S3 storage, Mailgun, Sentry, etc.

Env files are in `.envs/.local/` (`.django` and `.postgres`). The `JWT_AUTH_COOKIE_NAME` env var is required even in local/test settings.

### Authentication

Two auth paths coexist:
1. **Session auth** (default on the `NinjaAPI` instance) — used by browser clients, powered by `django-allauth`.
2. **JWT cookie auth** (`JWTAuthRequired` in `bet_app/apps/users/auth.py`) — HS256 tokens stored in a named cookie, decoded with `python-jose`. Use `jwt_auth` as the `auth=` argument on individual routes that need it.

### Background tasks

Celery with Redis broker. Beat scheduler uses `django_celery_beat` (DB-backed). Task modules go in `<app>/tasks.py`.

## Code Conventions

- **Linting/formatting**: `ruff` (configured in `pyproject.toml`). Migrations are excluded. Runs on every commit via pre-commit.
- **HTML templates**: `djlint` for formatting/linting. Profile is `django`.
- **Type checking**: `mypy` with `django-stubs`. Migrations are excluded from checks.
- **Tests**: `pytest-django` with `factory_boy`. Factories live in `<app>/tests/factories.py`. The global `user` fixture in `bet_app/conftest.py` creates a `UserFactory` instance.
- **Imports**: `isort` via ruff with `force-single-line = true`.
- Pre-commit runs ruff, djlint, django-upgrade (targeting Django 6.0), and standard file checks.
