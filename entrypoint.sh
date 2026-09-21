#!/bin/sh
set -e

# Exporter le PATH pour garantir l'accès au .venv dans toutes les sous-commandes
export PATH="/app/.venv/bin:$PATH"

echo "=== Ajustement des permissions sur les volumes ==="
chown -R appuser:appuser /app/staticfiles /app/media /app/data

echo "=== Collecte des fichiers statiques ==="
gosu appuser /app/.venv/bin/python manage.py collectstatic --noinput

echo "=== Application des migrations ==="
gosu appuser /app/.venv/bin/python manage.py migrate --noinput

echo "=== Démarrage de l'application ==="
# Transmettre explicitement le PATH à gosu
exec gosu appuser env PATH="$PATH" "$@"