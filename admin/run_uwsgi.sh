#!/usr/bin/env bash

set -e

python manage.py collectstatic --noinput

#while ! nc -z $DB_HOST $DB_PORT; do
#      sleep 0.1
#done

#python manage.py migrate

chown www-data:www-data /var/log

uwsgi --strict --ini uwsgi.ini
