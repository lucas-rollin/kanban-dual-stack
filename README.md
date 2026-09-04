# Kanban Dual Stack

A full‑stack application designed for agile project management, featuring two backend implementations:

- Django REST Framework
- FastAPI + SQLAlchemy

Both backends are powered by PostgreSQL and consumed by a React + TypeScript frontend.

## Prerequisites

- Docker and Docker Compose installed
- Git (optional)

## Quick Start

1. Clone the repository:

    ```bash
    git clone https://github.com/lucas-rollin/kanban-dual-stack.git
    ```

2. Copy and configure environment variables:

    ```bash
    cp .env.example .env
    # Edit .env with your preferred credentials
    ```

3. Start the database:

    ```bash
    docker compose up -d db adminer
    ```

4. Verify everything is working:

    ```bash
    docker compose ps
    # You should see both db and adminer containers running
    ```

5. Access Adminer at [http://localhost:8080](http://localhost:8080)
