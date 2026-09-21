# ── Stage 1: Build dependencies ────────────────────────────────
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps for compiling Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    && rm -rf /var/lib/apt/lists/*

# Install UV from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY . .
RUN uv sync --frozen --no-dev

# ── Stage 2: Final image ───────────────────────────────────────
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"\
    HOME=/app
    

# Runtime deps for Pillow + gosu for entrypoint
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg62-turbo \
    zlib1g \
    libwebp7 \
    gosu \
    && rm -rf /var/lib/apt/lists/*

# Copy virtualenv from builder
COPY --from=builder /app/.venv /app/.venv

WORKDIR /app

# Create appuser
RUN addgroup --system appuser && \
    adduser --system --ingroup appuser --home /app appuser

# Copy source + entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY . /app/

# Create directories and fix ownership
RUN mkdir -p /app/data /app/staticfiles /app/media && \
    chown -R appuser:appuser /app

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["python", "-m", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]