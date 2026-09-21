FROM python:3.11-slim

# Configuration de l'environnement Python et UV
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Installation des dépendances système (gosu) + copie de l'exécutable uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    gosu \
    && rm -rf /var/lib/apt-get/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Création de l'utilisateur non-root
RUN addgroup --system appuser && adduser --system --group appuser

# Copie des fichiers de dépendances UV (pyproject.toml et uv.lock)
COPY pyproject.toml uv.lock /app/

# Installation des dépendances Python via uv (sans installer le projet principal encore)
RUN uv sync --frozen --no-install-project --no-dev

# Copie du reste du code source
COPY . /app/

# Installation du projet lui-même dans l'environnement virtuel
RUN uv sync --frozen --no-dev

# Création des dossiers pour les volumes et attribution des permissions
RUN mkdir -p /app/staticfiles /app/media /app/data && \
    chown -R appuser:appuser /app

# Rendre le script d'entrée exécutable
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

EXPOSE 8000

CMD ["gunicorn", "portfolio.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]