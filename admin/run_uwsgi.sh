#!/usr/bin/env bash
set -e
python manage.py collectstatic --noinput
python manage.py migrate
chown www-data:www-data /var/log
uwsgi --strict --ini uwsgi.ini