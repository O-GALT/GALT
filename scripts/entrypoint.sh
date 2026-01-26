#!/bin/sh
set -e

python manage.py collectstatic --noinput
python manage.py migrate --noinput

celery -A GALT worker -l info > logs/celery_worker.log 2>&1 &
celery -A GALT beat -l info > logs/celery_beat.log 2>&1 &

exec gunicorn GALT.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --timeout 120
