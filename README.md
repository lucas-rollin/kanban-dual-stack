# Scrumban Dual Stack

*Status: Active Development. Django domain modeling in progress, FastAPI implementation coming next.*

A comparative full-stack project management application implemented with **Django REST Framework** and **FastAPI + SQLAlchemy**, sharing the same PostgreSQL instance and consumed by the same React + TypeScript frontend.

This project is a **practical reference for developers who know one Python web stack and want to learn the other**. Rather than a lightweight demo, both backends implement identical application capabilities using the idiomatic patterns, testing strategies, and ORM conventions of their respective ecosystems.

## Why This Project?

Most tutorials present Django or FastAPI in isolation, often relying on flat project structures. **Scrumban Dual Stack** demonstrates how both ecosystems grow into production-ready architectures featuring non-trivial domain logic, query optimization, authentication, and database integrity.

The project aims for:

- **Feature & Architectural Parity:** both backends implement the same application capabilities and equivalent concerns are easy to locate across the two codebases.
- **Framework idiomacy:** Django stays idiomatic Django; FastAPI leverages idiomatic Pydantic models, dependency injection, and Async/SQLAlchemy patterns.
- **Direct Side-by-Side Comparison:** Clear documentation comparing ORMs, validation, permissions, migrations (Django vs. Alembic), and request lifecycles.

## Docker Architecture & Environments

Every service uses a **single multi-stage `Dockerfile`** with dedicated `development` and `production` build targets. Dependency management is handled by **`uv`** for Python backends and **`pnpm`** for the React frontend.

| Service | Development Target (`development`) | Production Target (`production`) | Package Manager |
| --- | --- | --- | --- |
| **Django** (`backend-django`) | Live reload (`runserver`), bind-mounted source, anonymous volume for `/app/.venv` | Multi-stage, non-root `appuser`, `gunicorn`, static asset collection | `uv` (`pyproject.toml` + `uv.lock`) |
| **FastAPI** (`backend-fastapi`) | Live reload (`fastapi dev`), bind-mounted source, anonymous volume for `/app/.venv` | Multi-stage, non-root `appuser`, `uvicorn` | `uv` (`pyproject.toml` + `uv.lock`) |
| **Frontend** (`frontend`) | Live reload (`vite`), bind-mounted source, anonymous volume for `/app/node_modules` | Multi-stage, static bundle built with `pnpm build` and served via Nginx Alpine | `pnpm` (`package.json` + `pnpm-lock.yaml`) |

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose installed
- Git (optional, for cloning)

## Quick Start

### 1. Clone & Configure Environment Variables

```bash
git clone https://github.com/lucas-rollin/scrumban-dual-stack.git
cd scrumban-dual-stack

# Root config (Postgres superuser credentials for DB & Adminer)
cp .env.example .env

# Backend configs
cp backend-django/.env.example backend-django/.env
cp backend-fastapi/.env.example backend-fastapi/.env
cp frontend/.env.example frontend/.env
```

*(Update these files with your preferred local values before continuing).*

### 2. Start Services

```bash
# Start the database and admin UI
docker compose up -d db adminer

# Start both backends (dev mode with live reload)
docker compose up -d backend-django backend-fastapi

# Start React frontend
docker compose up -d frontend
```

### 3. Run Database Migrations

Once the containers are running, apply the database schemas:

- **Django:**

    ```bash
    docker compose exec backend-django python manage.py migrate
    ```

- **FastAPI:**

    ```bash
    docker compose exec backend-fastapi alembic upgrade head
    ```

### 4. Verify

Run `docker compose ps` to ensure all containers are running. Access the endpoints at:

- **Django:** [http://localhost:8000](http://localhost:8000)
- **FastAPI:** [http://localhost:8001](http://localhost:8001)
- **React:** [http://localhost:5173](http://localhost:5173)
- **Adminer:** [http://localhost:8080](http://localhost:8080) *(Server: `db`)*

## Database Management

Databases are initialized automatically on first startup via `postgres/init-db.sql`.

To completely reset the database volumes (e.g., after modifying initialization scripts):

```bash
docker compose down -v
docker compose up -d db
```

### Python Backends (uv)

Dependencies are managed using pyproject.toml and locked with uv.lock.

- Install / sync local environment:

    ```bash
    cd backend-django   # or cd backend-fastapi
    uv sync
    ```

- Add a runtime dependency:

    ```bash
    uv add <package_name>
    ```

- Add a development dependency:

    ```bash
    uv add --dev <package_name>
    ```

- Update lockfile:

    ```bash
    uv lock --upgrade
    ```

> **Note:** During development with Docker Compose, an anonymous volume (`/app/.venv`) protects the container's virtual environment from host mounts. If you add or remove packages via `uv` on your host machine, rebuild the development containers
> so Docker updates the internal virtual environment:
>
> ```bash
> docker compose up -d --build
> ```

## Production Deployment

To run the full application using the production targets (`target: production`):

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

In production mode:

- Backends run under a non-root user (`appuser`) using production WSGI/ASGI servers (`gunicorn` / `uvicorn`).
- No host source directories are mounted into `/app`.
- Static files for Django are collected into WhiteNoise storage during image build.
- The React frontend is compiled to static files and served directly by Nginx.
