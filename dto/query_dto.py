from pydantic import BaseModel
from decimal import Decimal

class QueryDTO(BaseModel):
    from_: str
    to: str | list
    amount: Decimal

