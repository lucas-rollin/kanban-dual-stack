# --- Stage 1: Shared base ---
FROM python:3.14-slim AS base
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy
COPY pyproject.toml uv.lock ./

# --- Stage 2: Development target ---
FROM base AS development
RUN uv sync --frozen
COPY . .
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# --- Stage 3: Build layer ---
FROM base AS builder
RUN uv sync --frozen --no-dev
COPY . .
ENV PATH="/app/.venv/bin:$PATH"
RUN SECRET_KEY=build-dummy-key \
    DATABASE_URL=sqlite:///build.db \
    DEBUG=False \
    CORS_ALLOWED_ORIGINS=localhost \
    python manage.py collectstatic --noinput

# --- Stage 4: Production target ---
FROM python:3.14-slim AS production
RUN useradd -m -r appuser && mkdir /app && chown -R appuser /app
WORKDIR /app
COPY --from=builder --chown=appuser:appuser /app /app
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
USER appuser
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "config.wsgi:application"]