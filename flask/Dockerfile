FROM python:3.9

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --upgrade --no-cache-dir pip && pip install -r requirements.txt

COPY . .

CMD ["python", "pywsgi.py"]