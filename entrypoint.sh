#!/bin/sh

# Запуск миграций
echo "Применение миграций..."
if ! yoyo apply --database "$DB_URL" "$MIGRATION_PATH"; then
    echo "Ошибка при применении миграций."
    exit 1
fi

echo "Миграции успешно применены."

# Установка рабочей директории
cd ./ || exit

# Запуск приложения
echo "Запуск приложения..."
if ! poetry run   uvicorn app.main:app --host 0.0.0.0 --port 8000; then
    echo "Ошибка при запуске приложения."
    exit 1
fi

echo "Приложение успешно запущено."