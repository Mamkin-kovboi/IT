import asyncpg
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

class Database:
    def __init__(self):
        self.conn = None

    async def connect(self):
        dsn = os.getenv("DATABASE_URL")

        # Проверяем, что DSN не пустая строка
        if not dsn:
            raise ValueError("Строка подключения не указана в переменной окружения DATABASE_URL.")

        # Если строка подключения корректна, устанавливаем соединение
        self.conn = await asyncpg.connect(dsn=dsn)

    async def close(self):
        if self.conn:
            await self.conn.close()
