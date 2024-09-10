from typing import Optional

import asyncpg
from config import DATABASE_CONFIG
from models import currencyprice

class DatabaseManager:
    def __init__(self)-> None:
        self.conn = None

    async def connect(self)-> None:
        """Соединие с дб
        """
        self.conn = await asyncpg.connect(**DATABASE_CONFIG)

    async def close(self)-> None:
        """Закрытие бд
        """
        await self.conn.close()

    async def fetch_currency_pairs(self):
        """Получает все валютные пары из базы данных.
        Returns:
            List[str]: Список имен валютных пар.
        """
        query = "SELECT name FROM currency;"
        rows = await self.conn.fetch(query)
        return [row['name'] for row in rows]

    async def fetch_currency_pair_id(self, pair: str) -> Optional[int]:
        """Получает id валютной пары по ее имени.
        Args:
            pair (str): Имя валютной пары.
        Returns:
            Optional[int]: Идентификатор валютной пары или None, если не найдено.
        """
        query = "SELECT id FROM currency WHERE name = $1;"
        row = await self.conn.fetchrow(query, pair)
        return row['id'] if row else None

    async def fetch_exchange_url(self, exchange_name: str) -> Optional[str]:
        """Получает URL API Биржи.
        Args:
            exchange_name (str): Имя биржи.
        Returns:
            Optional[str]: URL API биржи или None, если обменник не найден.
        """
        query = "SELECT api_url FROM exchanger WHERE name = $1;"
        row = await self.conn.fetchrow(query, exchange_name)
        return row['api_url'] if row else None

    async def save_price(self, currency_price: currencyprice)-> None:
        """Сохраняет информацию о ценах валют в базе данных.
        Args:
            currency_price (currencyprice): Объект, содержащий информацию о ценах валют.
        """
        query = """
            INSERT INTO currency_price (currency_pair_id, price, source, datetime)
            VALUES ($1, $2, $3, $4);
        """
        await self.conn.execute(query,
                                 currency_price.currency_pair_id,
                                 currency_price.price,
                                 currency_price.source,
                                 currency_price.datetime)
