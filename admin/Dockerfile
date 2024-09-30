FROM python:3.11

WORKDIR /opt/app

RUN mkdir -p /var/www/static/ \
     && mkdir -p /var/www/media/ \
     && mkdir -p /data/static/ \
     && mkdir -p /data/media/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240

ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY run_uwsgi.sh run_uwsgi.sh
COPY requirements.txt requirements.txt
COPY uwsgi/uwsgi.ini uwsgi.ini

RUN pip install --upgrade --no-cache-dir pip && pip install -r requirements.txt

RUN apt-get update

COPY . .

ENTRYPOINT ["bash", "run_uwsgi.sh"]
