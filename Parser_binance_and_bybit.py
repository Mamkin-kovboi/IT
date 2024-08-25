import aiohttp
import logging
import datetime
import asyncio
import asyncpg
from typing import Optional, Dict, Any, List

# Настройка логгирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("logger")


async def get_exchange_url(conn: asyncpg.Connection, exchange_name: str) -> Optional[str]:
    """Получает URL биржи из базы данных."""
    query = "SELECT api_url FROM exchanger WHERE name = $1;"
    row = await conn.fetchrow(query, exchange_name)
    return row['api_url'] if row else None


async def binance_price(session: aiohttp.ClientSession, pair: str, binance_url: str) -> Optional[Dict[str, Any]]:
    """Получает цену криптовалюты с биржи Binance.

    Args:
        session (aiohttp.ClientSession): Сессия для выполнения HTTP-запросов.
        pair (str): Символ валютной пары, например 'BTCUSDT'.

    Returns:
        Optional[Dict[str, Any]]: Словарь с ценой, если запрос успешен;
                                   иначе None.
    """
    params = {"symbol": pair}
    async with session.get(binance_url, params=params) as response:
        if response.status == 200:
            result = await response.json()
            logger.info(f"Получена цена для {pair} с Binance: {result['price']}")
            return result
        else:
            error_response = await response.json()
            logger.error(f"Ошибка Binance: {response.status} - {error_response}")
            return None


async def bybit_price(session: aiohttp.ClientSession, pair: str,bybit_url :str) -> Optional[Dict[str, Any]]:
    """Получает цену криптовалюты с биржи Bybit.

    Args:
        session (aiohttp.ClientSession): Сессия для выполнения HTTP-запросов.
        pair (str): Символ валютной пары, например 'BTCUSDT'.

    Returns:
        Optional[Dict[str, Any]]: Словарь с ценой, если запрос успешен;
                                   иначе None.
    """
    params = {"symbol": pair}
    async with session.get(bybit_url, params=params) as response:
        if response.status == 200:
            result = await response.json()
            logger.info(f"Получена цена для {pair} с Bybit: {result['price']}")
            return result
        else:
            error_response = await response.json()
            logger.error(f"Ошибка Bybit: {response.status} - {error_response}")
            return None


async def save_price(conn: asyncpg.Connection, currency_pair_id: int, price: float, source: str) -> None:
    """Сохраняет цену в таблицу currency_price.

    Args:
        conn (asyncpg.Connection): Соединение с базой данных.
        currency_pair_id (int): ID валютной пары.
        price (float): Цена валютной пары.
        source (str): Источник цены (например, 'Binance' или 'Bybit').

    Returns:
        None
    """
    query = """
        INSERT INTO currency_price (currency_pair_id, price, source, datetime)
        VALUES ($1, $2, $3, $4);
    """
    await conn.execute(query, currency_pair_id, price, source, datetime.datetime.now())
    logger.info(f"Цена {price} для валютной пары с ID {currency_pair_id} сохранена в таблицу currency_price.")


async def get_currency_pair_id(conn: asyncpg.Connection, pair: str) -> Optional[int]:
    """Получает ID валютной пары из базы данных по её символу.

    Args:
        conn (asyncpg.Connection): Соединение с базой данных.
        pair (str): Символ валютной пары.

    Returns:
        Optional[int]: ID валютной пары, если найдена; иначе None.
    """
    query = "SELECT id FROM currency WHERE name = $1;"
    row = await conn.fetchrow(query, pair)
    return row['id'] if row else None


async def price(conn: asyncpg.Connection, pairs: List[str]) -> None:
    """Запрашивает цены на криптовалюты с бирж Binance и Bybit и сохраняет их в базе данных.

    Args:
        conn (asyncpg.Connection): Соединение с базой данных.
        pairs (List[str]): Список символов валютных пар.

    Returns:
        None
    """
    async with aiohttp.ClientSession() as session:
        while True:
            for pair in pairs:
                currency_pair_id = await get_currency_pair_id(conn, pair)
                if currency_pair_id is None:
                    logger.error(f"Не удалось найти ID для валютной пары {pair}.")
                    continue

                binance_url = await get_exchange_url(conn, 'Binance')
                bybit_url = await get_exchange_url(conn, 'Bybit')

                if binance_url is None or bybit_url is None:
                    logger.error("Не удалось получить URL для Binance или Bybit.")
                    return

                while True:
                    for pair in pairs:
                        currency_pair_id = await get_currency_pair_id(conn, pair)
                        if currency_pair_id is None:
                            logger.error(f"Не удалось найти ID для валютной пары {pair}.")
                            continue

                        binance = await binance_price(session, pair, binance_url)
                        bybit = await bybit_price(session, pair, bybit_url)

                        if binance:
                            await save_price(conn, currency_pair_id, float(binance['price']), "Binance")

                        if bybit:
                            await save_price(conn, currency_pair_id, float(bybit['price']), "Bybit")

                    await asyncio.sleep(15)


async def fetch_data() -> None:
    """Инициализирует соединение с базой данных и запускает процесс получения цен.

    Returns:
        None
    """
    conn = None
    try:
        conn = await asyncpg.connect(user='postgres', password='qwerty', database='parser', host='127.0.0.1')

        # SQL-запрос для получения символов валют
        query = """
            SELECT 
                name 
            FROM 
                currency;
        """
        rows = await conn.fetch(query)
        pairs = [row['name'] for row in rows]

        await price(conn, pairs)

    except Exception as e:
        logger.error(f"Ошибка при получении данных: {e}")
    finally:
        if conn:
            await conn.close()


if __name__ == "__main__":
    asyncio.run(fetch_data())
