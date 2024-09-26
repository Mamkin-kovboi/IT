#!/bin/sh
set -e

# Запуск миграций
yoyo apply "$DATABASE_URL"

# Запуск приложения
exec "$@"