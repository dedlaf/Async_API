FROM python:3.10-alpine

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

WORKDIR /app

CMD python3 spammer.py
