# Используем официальный образ Python
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы requirements.txt и устанавливаем зависимости
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем все файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости для тестов
RUN pip install --no-cache-dir pytest

# Копируем и делаем исполняемым скрипт entrypoint.sh
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Устанавливаем скрипт entrypoint.sh как точку входа
ENTRYPOINT ["/app/entrypoint.sh"]
