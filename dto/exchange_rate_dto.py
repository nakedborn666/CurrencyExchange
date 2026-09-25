from pydantic import BaseModel
from dto.currency_dto import CurrencyDTO
from typing import Optional
from decimal import Decimal

class ExchangeRateDTO(BaseModel):
    id: Optional[int] = None
    baseCurrency: CurrencyDTO
    targetCurrency: CurrencyDTO
    rate: Decimal

