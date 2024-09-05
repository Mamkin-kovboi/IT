from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Модель для валюты
class Currency(BaseModel):
    id: int
    name: str

# Модель для цены валюты
class CurrencyPrice(BaseModel):
    currency_pair_id: int
    price: float
    source: str
    datetime: datetime

#Модель для бирж
class Exchanger(BaseModel):
    exchanger_id: int
    name: str
    api_url: str

#Модель для валютных пар
class CurrencyPair(BaseModel):
    currency_pair_id: int
    currency_from_id: int
    currency_to_id: int
    exchanger_id: int


