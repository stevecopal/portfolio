FROM python:3.11-slim

# Empêche Python d'écrire des fichiers .pyc et d'utiliser un tampon de sortie
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Installation des dépendances système + gosu
RUN apt-get update && apt-get install -y --no-install-recommends \
    gosu \
    && rm -rf /var/lib/apt-get/lists/*

# Création d'un utilisateur non-root sans privilèges
RUN addgroup --system appuser && adduser --system --group appuser

# Installation des dépendances Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . /app/

# Création des répertoires pour les static, media et SQLite avec attribution des droits
RUN mkdir -p /app/staticfiles /app/media /app/data && \
    chown -R appuser:appuser /app

# Rendre le script d'entrée exécutable
RUN chmod +x /app/entrypoint.sh

# Le conteneur démarre en root pour corriger les permissions des volumes
ENTRYPOINT ["/app/entrypoint.sh"]

EXPOSE 8000

CMD ["gunicorn", "portfolio.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]