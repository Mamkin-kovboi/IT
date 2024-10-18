from app.models import CurrencyPrice
from app.services import CurrencyService
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Инициализация сервиса
currency_service = CurrencyService()
resource = {}

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    await currency_service.initialize()
    yield  # Работа между открытием и закрытием
    await currency_service.close()

# Создание приложения FastAPI с lifespan
app = FastAPI(lifespan=app_lifespan)

@app.get("/")
async def root():
    return {"message": "Welcome to the currency prices API!"}

@app.get("/prices/{currency_pair}",response_model=CurrencyPrice)
async def get_latest_price(currency_pair: str):
    return await currency_service.get_latest_price(currency_pair)


# if __name__ == "__main__":
#     uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
