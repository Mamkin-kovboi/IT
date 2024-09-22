import os
from typing import Optional, List
import asyncpg
import logging
from config import Database
from models import CurrencyPrice

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    def __init__(self) -> None:
        self.conn = None

    async def connect(self) -> None:
        """Соединение с дб"""
        try:
            self.conn = await asyncpg.connect(dsn=os.getenv("DATABASE_URL"))
            logger.info("Успешное соединение с базой данных.")
        except Exception as e:
            logger.error(f"Ошибка при соединении с базой данных: {e}")

    async def close(self) -> None:
        """Закрытие бд"""
        if self.conn:
            await self.conn.close()
            logger.info("Соединение с базой данных закрыто.")

    async def fetch_currency_pairs(self) -> List[str]:
        """Получает все валютные пары из базы данных.

        Returns:
            List[str]: Список имен валютных пар.
        """
        query = "select name from currency;"
        rows = await self.conn.fetch(query)
        logger.info("Получены валютные пары из базы данных.")
        return [row['name'] for row in rows]

    async def fetch_currency_pair_id(self, pair: str) -> Optional[int]:
        """Получает id валютной пары по ее имени.

        Args:
            pair (str): Имя валютной пары.

        Returns:
            Optional[int]: Идентификатор валютной пары или None, если не найдено.
        """
        query = "select id from currency where name = $1;"
        row = await self.conn.fetchrow(query, pair)
        if row:
            logger.info(f"Валютная пара '{pair}' найдена, ID: {row['id']}.")
            return row['id']
        else:
            logger.warning(f"Валютная пара '{pair}' не найдена.")
            return None

    async def fetch_exchange_url(self, exchange_name: str) -> Optional[str]:
        """Получает URL API Биржи.

        Args:
            exchange_name (str): Имя биржи.

        Returns:
            Optional[str]: URL API биржи или None, если обменник не найден.
        """
        query = "select api_url from exchanger where name = $1;"
        row = await self.conn.fetchrow(query, exchange_name)
        if row:
            logger.info(f"URL API для биржи '{exchange_name}' получен.")
            return row['api_url']
        else:
            logger.warning(f"Биржа '{exchange_name}' не найдена.")
            return None

    async def save_price(self, currency_price: CurrencyPrice) -> None:
        """Сохраняет информацию о ценах валют в базе данных.

        Args:
            currency_price (CurrencyPrice): Объект, содержащий информацию о ценах валют.
        """
        query = """
            insert into currency_price (currency_pair_id, price, source, datetime)
            values ($1, $2, $3, $4);
        """
        await self.conn.execute(query,
                                currency_price.currency_pair_id,
                                currency_price.price,
                                currency_price.source,
                                currency_price.datetime)
        logger.info(f"Цены валют сохранены: {currency_price}")

    async def fetch_latest_price(self, currency_pair_id: int) -> Optional[CurrencyPrice]:
        """Получает последнюю сохраненную цену для заданной валютной пары.

        Args:
            currency_pair_id: ID валютной пары.

        Returns:
            Объект CurrencyPrice с последней ценой или None, если цена не найдена.
        """
        query = """
            select price, source, datetime
            from currency_price
            where currency_pair_id = $1 
            order by datetime DESC 
            limit 1;
        """
        row = await self.conn.fetchrow(query, currency_pair_id)
        if row:
            logger.info(f"Последняя цена для валютной пары ID '{currency_pair_id}' получена.")
            return CurrencyPrice(currency_pair_id=currency_pair_id, price=row["price"], source=row["source"],
                                 datetime=row["datetime"])
        logger.warning(f"Цены для валютной пары ID '{currency_pair_id}' не найдены.")
        return None
