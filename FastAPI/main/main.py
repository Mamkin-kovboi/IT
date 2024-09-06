import aiohttp
import certifi
from fastapi import FastAPI
from asyncio import run
from services import CurrencyService

app = FastAPI()
currency_service = CurrencyService()

@app.on_event("startup")
async def startup_event():
    await currency_service.initialize()

@app.on_event("shutdown")
async def shutdown_event():
    await currency_service.close()


@app.get("/currencies/")
async def get_currency_pairs():
    return await currency_service.get_currency_pairs()

@app.get("/prices/{currency_pair}")
async def get_latest_price(currency_pair: str):
    return await currency_service.get_latest_price(currency_pair)







