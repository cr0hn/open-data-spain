#!/usr/bin/env sh

GUNICORN_LOG_LEVEL=${LOG_LEVEL:-INFO}

export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-ods.settings}

# Apply database migrations
python manage.py migrate

# Start gunicorn
exec gunicorn --log-level "${GUNICORN_LOG_LEVEL}" -c /gunicorn.conf.py --bind ":8080" -w 4 -k gevent --timeout 0 --backlog 512 --worker-connections 512 ods.wsgi
