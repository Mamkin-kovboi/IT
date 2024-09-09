from datetime import datetime
from typing import List, Dict, Any

import aiohttp
import asyncio
import logging

from typing_extensions import Optional

from repositories import DatabaseManager
from models import currency, currencyprice

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class currencyservice:
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
        await asyncio.create_task(self.fetch_prices())

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
                currency_price = currencyprice(
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
                currency_price = currencyprice(
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

    async def get_bybit_price(self, pair: str, bybit_url: str)-> Optional[Dict[str, Any]]:
        """Получаем цену криптовалюты с биржи Bybit
        Arg:
            param pair: Список строк, представляющих валютные пары, для которых нужно получить цены.
            param bybit_url: Ссылка на API для биржи Bybit
        Return:
            Optional[Dict[str, Any]]: Словарь с информацией о валюте и последней цене по бирже Bybit,
            или None, если цена не доступна.
        """
        params = {'symbol': pair}
        try:
            async with self.session.get(bybit_url, params=params, ssl=False) as response:
                if response.status == 200:
                    data = await response.json()
                    # Проверка на ключ 'result'
                    if 'result' in data and isinstance(data['result'], dict):
                        # Проверка наличия ключа 'price' в 'result'
                        if 'price' in data['result']:
                            return data['result']
                        else:
                            logger.error("Response does not contain 'price': %s", data['result'])
                            return None
                    else:
                        logger.error("Response does not contain 'result' or it is invalid: %s", data)
                        return None
                else:
                    logger.error("Failed to fetch data from Bybit: %s", response.status)
                    return None
        except Exception as e:
            logger.error("Error fetching data from Bybit: %s", e)
            return None

    async def get_currency_pairs(self) -> List[str]:
        """Получение списка валютных пар из базы данных.
        Returns:
            List[str]: Список строк, представляющих валютные пары.
        """
        return await self.db_manager.fetch_currency_pairs()

    async def get_latest_price(self, currency_pair: str)-> Optional[Dict[str, Any]]:
        """Получение последней цены для заданной валютной пары
        Arg:
            param currency_pair: Код валютной пары
        Return:
            Optional[Dict[str, Any]]: Словарь с информацией о последней цене,
            или None, если цена не доступна.
        """
        # Логика для извлечения последней цены по валютной паре
        pass
