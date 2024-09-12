from pydantic import BaseModel, Field
from datetime import datetime

# Модель для валюты
class Currency(BaseModel):
    id: int = Field(..., description="Идентификатор валюты")
    name: str = Field(..., max_length=50, description="Название валюты")

# Модель для цены валюты
class CurrencyPrice(BaseModel):
    currency_pair_id: int = Field(..., description="Идентификатор валютной пары")
    price: float = Field(..., description="Цена", ge=0)
    source: str = Field(..., max_length=150, description="Название биржи")
    datetime: datetime

# Модель для бирж
class Exchanger(BaseModel):
    exchanger_id: int = Field(..., description="Идентификатор биржи")
    name: str = Field(..., max_length=50, description="Название биржи")
    api_url: str = Field(..., max_length=150, description="API биржи")

# Модель для валютных пар
class CurrencyPair(BaseModel):
    currency_pair_id: int = Field(..., description="Идентификатор валютной пары")
    currency_from_id: int = Field(..., description="Идентификатор исходной валюты")
    currency_to_id: int = Field(..., description="Идентификатор целевой валюты")
    exchanger_id: int = Field(..., description="Идентификатор биржи")

