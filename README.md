# Kanban Dual Stack

A full-stack agile project management application featuring two backend implementations (**Django REST Framework** and **FastAPI + SQLAlchemy**) powered by a shared PostgreSQL instance and a React + TypeScript frontend.

## Architecture

- **Frontend:** React + TypeScript
- **Backends:**
  - Django REST Framework (`http://localhost:8000`)
  - FastAPI + SQLAlchemy (`http://localhost:8001`)
- **Database:** PostgreSQL (single instance hosting databases `kanban_django` & `kanban_fastapi`)
- **Database UI:** Adminer (`http://localhost:8080`)

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose installed
- Git (optional, for cloning)

## Quick Start

### 1. Clone & Configure Environment Variables

```bash
git clone https://github.com/lucas-rollin/kanban-dual-stack.git
cd kanban-dual-stack

# Root config (Postgres superuser credentials for DB & Adminer)
cp .env.example .env

# Backend configs
cp backend-django/.env.example backend-django/.env
cp backend-fastapi/.env.example backend-fastapi/.env
```

*(Update these files with your preferred local values before continuing).*

### 2. Start Services

```bash
# Start the database and admin UI
docker compose up -d db adminer

# Start both backends (dev mode with live reload)
docker compose up -d backend-django backend-fastapi
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
- **Adminer:** [http://localhost:8080](http://localhost:8080) *(Server: `db`)*

## Database Management

Databases are initialized automatically on first startup via `postgres/init-db.sql`.

To completely reset the database volumes (e.g., after modifying initialization scripts):

```bash
docker compose down -v
docker compose up -d db
```

## Docker Environments

Both backends include separate Dockerfiles for development and production:

| Component | Development (`Dockerfile.dev`) | Production (`Dockerfile.prod`) |
| --- | --- | --- |
| **Django** | Single-stage, bind-mounted, `manage.py runserver` | Multi-stage, non-root, `gunicorn` + `collectstatic` |
| **FastAPI** | Single-stage, bind-mounted, `fastapi dev` | Multi-stage, non-root, `uvicorn` |

## Production Deployment

To run the application using the production-optimized multi-stage Dockerfiles (`Dockerfile.prod`), use the dedicated production compose file:

```bash
docker compose -f docker-compose.prod.yml up -d --build
```
