# ── Build stage ──────────────────────────────────────────────
FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY app/ app/
COPY alembic/ alembic/
COPY alembic.ini ./

RUN uv sync --frozen --no-dev

# ── Production stage ─────────────────────────────────────────
FROM python:3.12-slim

RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid appuser --no-create-home appuser

WORKDIR /app

# Copy virtual env and source from builder
COPY --from=builder /app /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/docs')"]

# Gunicorn + Uvicorn workers
CMD [".venv/bin/gunicorn", "app.main:app", \
    "--worker-class", "uvicorn.workers.UvicornWorker", \
    "--workers", "2", \
    "--bind", "0.0.0.0:8000", \
    "--timeout", "120", \
    "--graceful-timeout", "30", \
    "--keep-alive", "5", \
    "--access-logfile", "-", \
    "--error-logfile", "-"]
