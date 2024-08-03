# Используем базовый образ Python
FROM python:3.10

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /usr/src/etl

# Копируем зависимости (requirements.txt) в контейнер
COPY requirements.txt .
COPY elt.py .
COPY config.py .
COPY get_lists_for_redis.py .

# Устанавливаем зависимости
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# Запускаем ETL-скрипт при запуске контейнера
CMD ["python", "elt.py"]
