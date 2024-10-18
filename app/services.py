from datetime import datetime
from typing import List, Dict, Any

import aiohttp
import asyncio
import logging

from typing_extensions import Optional

from app.repositories import DatabaseManager
from app.models import CurrencyPrice

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CurrencyService:
    def __init__(self):

        self.db_manager = DatabaseManager()
        self.session = None

    async def initialize(self):
        """Соединение с бд
        Return:
            None
        """
        await self.db_manager.connect()
        self.session = aiohttp.ClientSession()
        asyncio.create_task(self.fetch_prices())

    async def close(self):
        """Закрытие бд
        Return:
            None
        """
        await self.db_manager.close()
        if self.session:
            await self.session.close()

    async def fetch_prices(self):
        """Получение валютных пар и цены с периодичностью в 15 секунд
        Return:
            None
        """
        pairs = await self.db_manager.fetch_currency_pairs()
        logger.info(f"Starting price fetch for pairs: {pairs}")
        while True:
            await self.get_prices(pairs)
            logger.info("Prices fetched successfully, sleeping for 15 seconds...")
            await asyncio.sleep(15)

    async def get_prices(self, pairs: List[str])-> None:
        """Получаем цены с бирж для указанных валютных пар и сохраняем их в базу данных.
        Arg:
            param pairs: Список строк, представляющих валютные пары, для которых нужно получить цены.
        Return:
            None
        """
        for pair in pairs:
            logger.info(f"Fetching prices for pair: {pair}")
            currency_pair_id = await self.db_manager.fetch_currency_pair_id(pair)
            if currency_pair_id is None:
                logger.warning(f"Currency pair ID for {pair} not found, skipping...")
                continue

            # Получаем цену с Binance
            binance_url = await self.db_manager.fetch_exchange_url('Binance')
            price_data = await self.get_binance_price(pair, binance_url)
            if price_data:
                currency_price = CurrencyPrice(
                    currency_pair_id=currency_pair_id,
                    price=float(price_data['price']),
                    source="Binance",
                    datetime=datetime.now()
                )
                await self.db_manager.save_price(currency_price)
                logger.info(f"Saved price from Binance for {pair}: {currency_price.price}")

            # Получаем цену с Bybit
            bybit_url = await self.db_manager.fetch_exchange_url('Bybit')
            price_data = await self.get_bybit_price(pair, bybit_url)
            if price_data:
                currency_price = CurrencyPrice(
                    currency_pair_id=currency_pair_id,
                    price=float(price_data['price']),
                    source="Bybit",
                    datetime=datetime.now()
                )
                await self.db_manager.save_price(currency_price)
                logger.info(f"Saved price from Bybit for {pair}: {currency_price.price}")

    async def get_binance_price(self, pair: str, binance_url: str)-> Optional[Dict[str, Any]]:
        """Получает цену криптовалюты с биржи Binance.
        Arg:
            param pair: Список строк, представляющих валютные пары, для которых нужно получить цены.
            param binance_url: Ссылка на API для биржи Binance
        Return:
            Optional[Dict[str, Any]]: Словарь с информацией о валюте и последней цене по бирже Binance,
            или None, если цена не доступна.
        """
        params = {'symbol': pair}
        try:
            logger.info(f"Sending request to Binance for pair: {pair} with URL: {binance_url}")
            async with self.session.get(binance_url, params=params, ssl=False) as response:
                if response.status == 200:
                    logger.info(f"Successfully fetched data from Binance for {pair}")
                    return await response.json()
                else:
                    logger.error(f"Failed to fetch data from Binance for {pair}: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Error fetching data from Binance for {pair}: {e}")
            return None

    async def get_bybit_price(self, pair: str, bybit_url: str) -> Optional[Dict[str, Any]]:
        """Получаем цену криптовалюты с биржи Bybit.

        Arg:
            param pair: Строка, представляющая валютную пару, для которой нужно получить цену.
            param bybit_url: Ссылка на API для биржи Bybit.

        Return:
            Optional[Dict[str, Any]]: Словарь с информацией о валюте и последней цене по бирже Bybit,
            или None, если цена недоступна.
        """
        params = {'symbol': pair}

        try:
            async with self.session.get(bybit_url, params=params, ssl=False) as response:
                if response.status == 200:
                    data = await response.json()

                    if 'result' in data:
                        result = data['result']  # Достаем результат

                        if 'price' in result:
                            logger.info(f"Получена цена для пары {pair}: {result['price']}")
                            return result  # Возвращаем весь результат, о цене и других полях

                        logger.error("Response does not contain 'price': %s", result)
                    else:
                        logger.error("Response does not contain 'result' or it is invalid: %s", data)
                else:
                    logger.error("Failed to fetch data from Bybit: %s", response.status)

        except Exception as e:
            logger.error("Error fetching data from Bybit: %s", e)

        return None

    async def get_currency_pairs(self) -> List[str]:
        """Получение списка валютных пар из базы данных.
        Returns:
            List[str]: Список строк, представляющих валютные пары.
        """
        return await self.db_manager.fetch_currency_pairs()

    async def get_latest_price(self, currency_pair: str) -> Optional[CurrencyPrice]:
        """Получает последнюю цену для заданной валютной пары.

        Arg:
            currency_pair: Строка, представляющая валютную пару (например, 'BTCUSDT').
        Return:
            Объект CurrencyPrice с последней ценой или None, если цена не найдена.
        """
        logger.info(f"Запрос последней цены для валютной пары: {currency_pair}")

        # Получаем ID валютной пары из базы данных
        currency_pair_id = await self.db_manager.fetch_currency_pair_id(currency_pair)
        if currency_pair_id is None:
            logger.warning(f"Валютная пара {currency_pair} не найдена в базе данных.")
            return None

        # Получаем последнюю цену из базы данных
        latest_price = await self.db_manager.fetch_latest_price(currency_pair_id)  # Получаем последнюю цену

        if latest_price is None:
            logger.warning(f"Последняя цена для валютной пары {currency_pair} не найдена.")
        else:
            logger.info(f"Последняя цена для {currency_pair}: {latest_price.price}")

        return latest_price
