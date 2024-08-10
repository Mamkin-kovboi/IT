import aiohttp
import datetime
import asyncio

thisttuple = ("BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "DOGEUSDT")

binance_url = "https://api.binance.com/api/v3/ticker/price"
bybit_url = "https://api.bybit.com/spot/v3/public/quote/ticker/price"

write_file = "crypto_curses.txt"


async def binance_price(session, pair):
    params = {'symbol': pair}
    async with session.get(binance_url, params=params) as response:
        if response.status == 200:
            return await response.json()
        else:
            print(f"Error Binance: {response.status} - {await response.json()}")
            return None


async def bybit_price(session, pair):
    params = {'symbol': pair}
    async with session.get(bybit_url, params=params) as response:
        if response.status == 200:
            return await response.json()
        else:
            print(f"Error Bybit: {response.status} - {await response.json()}")
            return None


async def price():
    async with aiohttp.ClientSession() as session:
        while True:
            prices = []
            for pair in thisttuple:
                binance = await binance_price(session, pair)
                bybit = await bybit_price(session, pair)

                if binance:
                    prices.append(
                        f"Binance: {pair} - Price: {binance['price']}  - Time: {datetime.datetime.now()}\n"
                    )

                if bybit:
                    prices.append(
                        f"Bybit: {pair} - Price: {bybit['lastPrice']}  - Time: {datetime.datetime.now()}\n"
                    )
            with open(write_file, 'a') as file:
                file.writelines(prices)

            print("Prices ready to learn.")

            await asyncio.sleep(15)


if __name__ == "__main__":
    asyncio.run(price())
