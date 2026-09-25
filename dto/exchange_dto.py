from pydantic import BaseModel
from dto.currency_dto import CurrencyDTO
from decimal import Decimal

class ExchangeDTO(BaseModel):
    baseCurrency: CurrencyDTO
    targetCurrency: CurrencyDTO
    rate: Decimal
    amount: Decimal
    convertedAmount: Decimal

