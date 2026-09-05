# Kanban Dual Stack

A full‑stack application designed for agile project management, featuring two backend implementations:

- Django REST Framework
- FastAPI + SQLAlchemy

Both backends are powered by separate PostgreSQL databases and consumed by a React + TypeScript frontend.

## Prerequisites

- Docker and Docker Compose installed
- Git (optional)

## Quick Start

1. Clone the repository:

    ```bash
    git clone https://github.com/lucas-rollin/kanban-dual-stack.git
    ```

2. Copy and configure environment variables. There are **two separate `.env` files**, one per level:

    ```bash
    # Root: Postgres superuser credentials, shared by db + adminer
    cp .env.example .env

    # Django: app secrets
    cp backend-django/.env.example backend-django/.env
    ```

    Edit both with your preferred values. Django's `DATABASE_URL` reads the same values via Docker Compose.

3. Start the database and admin UI:

    ```bash
    docker compose up -d db adminer
    ```

4. Start the Django backend (dev mode, with live reload):

    ```bash
    docker compose up backend-django
    ```

5. Verify everything is working:

    ```bash
    docker compose ps
    # db, adminer, and backend-django should all be running
    ```

    - Django API: [http://localhost:8000](http://localhost:8000)
    - Adminer: [http://localhost:8080](http://localhost:8080) (server: `db`, using the credentials from your root `.env`)

## Databases

A single Postgres instance hosts two databases, created automatically on first startup via `postgres/init-db.sql`:

- `kanban_django` — used by the Django backend
- `kanban_fastapi` — used by the FastAPI backend

Changing `postgres/init-db.sql` after the container has already run once won't re-apply automatically. Reset with:

```bash
docker compose down -v   # deletes all Postgres data
docker compose up -d db
```

## Dev vs. Prod Images (Django)

- **`Dockerfile.dev`** (used by default in `docker-compose.yml`): single-stage, runs `manage.py runserver`, source code is bind-mounted for live reload.
- **`Dockerfile.prod`**: multi-stage build, runs via `gunicorn` as a non-root user, runs `collectstatic` at build time.
