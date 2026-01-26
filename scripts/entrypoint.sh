#!/bin/sh
set -e

python manage.py collectstatic --noinput
python manage.py migrate --noinput

exec gunicorn GALT.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --timeout 120
