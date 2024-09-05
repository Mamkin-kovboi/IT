from datetime import datetime
from typing import Optional
from config import DATABASE_CONFIG
import asyncpg

class DatabaseManager:
    def __init__(self):
        self.conn = None

    async def connect(self):
        self.conn = await asyncpg.connect(**DATABASE_CONFIG)

    async def close(self):
        await self.conn.close()

    async def fetch_currency_pairs(self):
        query = "SELECT name FROM currency;"
        rows = await self.conn.fetch(query)
        return [row['name'] for row in rows]

    async def fetch_currency_pair_id(self, pair: str) -> Optional[int]:
        query = "SELECT id FROM currency WHERE name = $1;"
        row = await self.conn.fetchrow(query, pair)
        return row['id'] if row else None

    async def fetch_exchange_url(self, exchange_name: str) -> Optional[str]:
        query = "SELECT api_url FROM exchanger WHERE name = $1;"
        row = await self.conn.fetchrow(query, exchange_name)
        return row['api_url'] if row else None

    async def save_price(self, currency_pair_id: int, price: float, source: str):
        query = """
            INSERT INTO currency_price (currency_pair_id, price, source, datetime)
            VALUES ($1, $2, $3, $4);
        """
        await self.conn.execute(query, currency_pair_id, price, source, datetime.datetime.now())
