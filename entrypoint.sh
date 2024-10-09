#!/bin/bash

set -e  # завершать при ошибках

# Ожидание готовности БД
until nc -z db 5433; do
  echo "Ожидание готовности базы данных..."
  sleep 2
done

echo "База данных доступна!"

# Запуск миграций с использованием переменных окружения
yoyo list --database postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@db:5433/$POSTGRES_DATABASE_NAME&lt;br&gt;&lt;br&gt;# Запуск сервера FastAPI&lt;br&gt;uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload&lt;br&gt;</code></pre>

### 3. Подключение переменных окружения в Docker

Если вы используете Docker Compose, вам нужно указать, что ваш сервис будет использовать переменные окружения из файла <code>.env</code>. Вот пример файла <code>docker-compose.yml</code>:

<pre><code class="language-yaml">&lt;br&gt;version: '3.8'&lt;br&gt;&lt;br&gt;services:&lt;br&gt;  web:&lt;br&gt;    build: .&lt;br&gt;    env_file:&lt;br&gt;      - .env&lt;br&gt;    ports:&lt;br&gt;      - "8000:8000"&lt;br&gt;    depends_on:&lt;br&gt;      - db&lt;br&gt;&lt;br&gt;  db:&lt;br&gt;    image: postgres:latest&lt;br&gt;    environment:&lt;br&gt;      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}&lt;br&gt;      POSTGRES_DB: ${POSTGRES_DATABASE_NAME}
    ports:
      - "5433:5432"  # Убедитесь, что порты настроены правильно