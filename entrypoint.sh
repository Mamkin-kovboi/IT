#!/bin/bash

set -e  # завершить при ошибках

# Ожидание готовности БД
while ! nc -z db 5433; do
  echo "Ожидание готовности базы данных..."
  sleep 2
done

echo "База данных доступна!"

# Запуск миграций
yoyo list --database postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@db:5433/$POSTGRES_DATABASE_NAME&lt;br&gt;&lt;br&gt;# Запуск сервера FastAPI&lt;br&gt;exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload&lt;br&gt;</code></pre>
