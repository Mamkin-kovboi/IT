FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем входной скрипт
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Копируем файлы
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY ./app ./app
COPY .env ./

# Устанавливаем yoyo-migrate
RUN pip install yoyo-migrate

# Команда для запуска сервера с миграцией
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]