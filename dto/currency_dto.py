from pydantic import BaseModel

class CurrencyDTO(BaseModel):
    id: int
    code: str
    name: str
    sign: str

