#!/bin/bash

set -e  # завершать при ошибках

# Ожидание готовности БД
until nc -z db 5433; do
  echo "Ожидание готовности базы данных..."
  sleep 2
done

echo "База данных доступна!"

# Запуск миграций
yoyo migrate --database postgresql://postgres:223456@db:5433/some_db

# Запуск сервера FastAPI
uvicorn main:app --host 0.0.0.0 --port 8000 --reload