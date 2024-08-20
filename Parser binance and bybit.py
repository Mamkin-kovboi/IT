import aiohttp
import logging
import datetime
import asyncio
import asyncpg
import psycopg2
from typing import Optional, Dict, Any, List

# Настройка логгирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("logger")

conn = psycopg2.connect(dbname="parser", user="postgres", password="qwerty", host="127.0.0.1")
cursor = conn.cursor()

# создаем таблицу currency
cursor.execute(
    "CREATE TABLE currency (id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL,  symbol VARCHAR(255) NOT NULL)")
conn.commit()
print("Таблица currency успешно создана")

# создаем таблицу exchanger
cursor.execute(
    "CREATE TABLE exchanger (id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL,  api_url VARCHAR(255) NOT NULL)")
conn.commit()
print("Таблица exchanger успешно создана")

# создаем таблицу currency_pair
cursor.execute(
    "CREATE TABLE currency_pair (id SERIAL PRIMARY KEY, currency_from_id INTEGER NOT NULL REFERENCES currency(id),  currency_to_id INTEGER NOT NULL REFERENCES currency(id), exchanger_id INTEGER NOT NULL REFERENCES exchanger(id))")
conn.commit()
print("Таблица currency_pair успешно создана")

# создаем таблицу price
cursor.execute(
    "CREATE TABLE price (id SERIAL PRIMARY KEY, currency_pair_id INTEGER NOT NULL REFERENCES currency_pair(id),  datetime TIMESTAMP NOT NULL, price FLOAT NOT NULL)")
conn.commit()
print("Таблица price успешно создана")

currency = [("Bitcoin", "BTC"), ("Ethereum", "ETH"), ("Solana", "SOL"), ("Dogecoin", "DOGE"), ("Pepe", "PEPE")]
cursor.executemany("INSERT INTO currency (name, symbol) VALUES (%s, %s)", currency)

conn.commit()
print("Данные в таблицу Currency добавлены")

exchanger = [("Binance", "https://api.binance.com/api/v3/ticker/price"),
             ("Bybit", "https://api.bybit.com/spot/v3/public/quote/ticker/price")]
cursor.executemany("INSERT INTO exchanger (name, api_url) VALUES (%s, %s)", exchanger)

conn.commit()
print("Данные в таблицу Exchanger добавлены")


PARAMS = ("BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "DOGEUSDT")

binance_url = "https://api.binance.com/api/v3/ticker/price"
bybit_url = "https://api.bybit.com/spot/v3/public/quote/ticker/price"

write_file = "crypto_curses.txt"


async def binance_price(session: aiohttp.ClientSession, pair: str) -> Optional[Dict[str, Any]]:
    """Получает цену криптовалюты с биржи Binance.

    Args:
        session (aiohttp.ClientSession): Сессия HTTP для выполнения запросов.
        pair (str): Символ криптовалюты (например, 'BTCUSDT').

    Returns:
        Optional[Dict[str, Any]]: JSON-ответ с ценой или None в случае ошибки.
    """
    params = {"symbol": pair}
    async with session.get(binance_url, params=params) as response:
        if response.status == 200:
            result = await response.json()
            logger.info(f"Получена цена для {pair} с Binance: {result["price"]}")
            return result
        else:
            error_response = await response.json()
            logger.error(f"Ошибка Binance: {response.status} - {error_response}")
            return None


async def bybit_price(session: aiohttp.ClientSession, pair: str) -> Optional[Dict[str, Any]]:
    """Получает цену криптовалюты с биржи Bybit.

    Args:
        session (aiohttp.ClientSession): Сессия HTTP для выполнения запросов.
        pair (str): Символ криптовалюты (например, 'BTCUSDT').

    Returns:
        Optional[Dict[str, Any]]: JSON-ответ с ценой или None в случае ошибки.
    """
    params = {"symbol": pair}
    async with session.get(binance_url, params=params) as response:
        if response.status == 200:
            result = await response.json()
            logger.info(f"Получена цена для {pair} с Bybit: {result["price"]}")
            return result
        else:
            error_response = await response.json()
            logger.error(f"Ошибка Bybit: {response.status} - {error_response}")
            return None

# создаем таблицу cryptocurrency
cursor.execute(
    "CREATE TABLE cryptocurrency (id SERIAL PRIMARY KEY, symbol VARCHAR(255) NOT NULL,  exchanger VARCHAR(255) NOT NULL, price INTEGER NOT NULL, datetime TIMESTAMP NOT NULL)")
conn.commit()
print("Таблица cryptocurrency успешно создана")


async def price() -> None:
    """Запрашивает цены на криптовалюты с бирж Binance и Bybit и сохраняет их в текстовый файл.

    Returns:
        None
    """
    async with aiohttp.ClientSession() as session:
        while True:
            prices: List[str] = []
            for pair in PARAMS:
                binance = await binance_price(session, pair)
                bybit = await bybit_price(session, pair)

                if binance:
                    prices.append(
                        f"Binance: {pair} - Price: {binance["price"]}  - Time: {datetime.datetime.now()}\n"
                    )

                if bybit:
                    prices.append(
                        f"Bybit: {pair} - Price: {bybit["price"]}  - Time: {datetime.datetime.now()}\n"
                    )

            if prices:
                with open(write_file, "a") as file:
                    file.writelines(prices)
                logger.info("Цены готовы и сохранены в файл.")

            await asyncio.sleep(15)


cursor.close()
conn.close()

if __name__ == "__main__":
    asyncio.run(price())
