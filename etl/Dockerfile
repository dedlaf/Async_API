FROM python:3.10

WORKDIR /opt/app

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/* && apt-get -y install curl;

COPY . .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/bin/sh", "-c", "./entrypoint.sh"]