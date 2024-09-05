from fastapi import FastAPI
from asyncio import run

app = FastAPI()
currency_service = CurrencyService()

@app.get("/currencies/")
async def get_currency_pairs():
    return await currency_service.get_currency_pairs()

@app.get("/prices/{currency_pair}")
async def get_latest_price(currency_pair: str):
    return await currency_service.get_latest_price(currency_pair)
