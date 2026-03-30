#!/bin/sh
set -e

python manage.py migrate --noinput
python manage.py collectstatic --clear --noinput

exec gunicorn psyschologic_backend.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 60
