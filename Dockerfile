FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /app

RUN apt-get update && apt-get install -y gcc python3-dev
RUN apt-get update && apt-get install -y netcat-openbsd

# Копируем входной скрипт
COPY entrypoint.py /usr/local/bin/entrypoint.py
RUN chmod +x /usr/local/bin/entrypoint.py

# Копируем файлы
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY ./app ./app
COPY .env ./

# Устанавливаем yoyo-migrate
RUN pip install yoyo-migrations

# Команда для запуска сервера с миграцией
ENTRYPOINT ["python", "/usr/local/bin/entrypoint.py"]