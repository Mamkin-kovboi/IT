import aiohttp
import logging
import datetime
import asyncio
from typing import Optional, Dict, Any, List

# Настройка логгирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("logger")

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
    async with session.get(bybit_url, params=params) as response:
        if response.status == 200:
            result = await response.json()
            logger.info(f"Получена цена для {pair} с Bybit: {result["lastPrice"]}")
            return result
        else:
            error_response = await response.json()
            logger.error(f"Ошибка Bybit: {response.status} - {error_response}")
            return None

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
                        f"Bybit: {pair} - Price: {bybit["lastPrice"]}  - Time: {datetime.datetime.now()}\n"
                    )
            
            if prices:
                with open(write_file, "a") as file:
                    file.writelines(prices)
                logger.info("Цены готовы и сохранены в файл.")

            await asyncio.sleep(15)

if __name__ == "__main__":
    asyncio.run(price())
