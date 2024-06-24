#!/usr/bin/env sh

export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-ods.settings}

celery -A celery_app worker -P gevent -c 4 -l info -E -B
