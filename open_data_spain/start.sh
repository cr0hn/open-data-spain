#!/usr/bin/env sh

export DJANGO_SETTINGS_MODULE=ods.settings

python manage.py migrate

python manage.py loaddata users github_oauth geopolitico
