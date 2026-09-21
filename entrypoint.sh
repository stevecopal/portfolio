#!/bin/sh
set -e

echo "=== Ajustement des permissions sur les volumes ==="
chown -R appuser:appuser /app/staticfiles /app/media /app/data

echo "=== Collecte des fichiers statiques ==="
gosu appuser python manage.py collectstatic --noinput

echo "=== Application des migrations ==="
gosu appuser python manage.py migrate --noinput

echo "=== Démarrage de l'application ==="
exec gosu appuser "$@"