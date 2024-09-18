# Используем официальный образ Python
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /app


RUN pip install poetry

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости
RUN poetry install --no-dev -vvv

# Копируем все файлы приложения
COPY . .


RUN poetry config virtualenvs.create false \
    && poetry install --only main

# Указываем команду для запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
