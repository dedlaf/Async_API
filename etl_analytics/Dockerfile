FROM python:3.10

WORKDIR /opt/app

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

RUN apt-get update;

COPY . .

CMD ["python", "etl_analytics_process.py"]