import aiohttp
import certifi
from fastapi import FastAPI
from services import currencyservice

app = FastAPI()
currency_service = currencyservice()

@app.get("/")
async def root():
    return {"message": "Welcome to the currency prices API!"}

async def lifespan(app: FastAPI):
    await currency_service.initialize()
    yield # работа между открытием и закрытием

    await currency_service.close()

app = FastAPI(lifespan=lifespan)

@app.get("/currencies/")
async def get_currency_pairs():
    return await currency_service.get_currency_pairs()

@app.get("/prices/{currency_pair}")
async def get_latest_price(currency_pair: str):
    return await currency_service.get_latest_price(currency_pair)
