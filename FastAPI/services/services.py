from datetime import datetime
import aiohttp
import asyncio
from repositories import DatabaseManager
from models import Currency, CurrencyPrice

class CurrencyService:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.session = None

    async def initialize(self):
        await self.db_manager.connect()
        self.session = aiohttp.ClientSession()
        # Здесь просто создаем задачу без await
        await asyncio.create_task(self.fetch_prices())

    async def close(self):
        await self.db_manager.close()
        if self.session:
            await self.session.close()

    async def fetch_prices(self):
        pairs = await self.db_manager.fetch_currency_pairs()
        while True:
            await self.get_prices(pairs)
            await asyncio.sleep(15)

    async def get_prices(self, pairs):
        for pair in pairs:
            currency_pair_id = await self.db_manager.fetch_currency_pair_id(pair)
            if currency_pair_id is None:
                continue

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

            binance_url = await self.db_manager.fetch_exchange_url('Binance')
            price_data = await self.get_bybit_price(pair, binance_url)
            if price_data:
                currency_price = CurrencyPrice(
                    currency_pair_id=currency_pair_id,
                    price=float(price_data['price']),
                    source="Binance",
                    datetime=datetime.now()
                )
                await self.db_manager.save_price(currency_price)

    async def get_binance_price(self, pair: str, binance_url: str):
        params = {'symbol': pair}
        try:
            async with self.session.get(binance_url, params=params, ssl=False) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Failed to fetch data from Binance: {response.status}")
                    return None
        except Exception as e:
            print(f"Error fetching data from Binance: {e}")
            return None

    async def get_bybit_price(self, pair: str, binance_url: str):
        params = {'symbol': pair}
        try:
            async with self.session.get(binance_url, params=params, ssl=False) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Failed to fetch data from Bybit: {response.status}")
                    return None
        except Exception as e:
            print(f"Error fetching data from Bybit: {e}")
            return None

    async def get_currency_pairs(self):
        return await self.db_manager.fetch_currency_pairs()

    async def get_latest_price(self, currency_pair: str):
        # Логика для извлечения последней цены по валютной паре
        pass
