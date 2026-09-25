from pydantic import BaseModel, model_validator
from exceptions.exceptions import NullFormFieldError
from decimal import Decimal

class ExchangeRatePatchDTO(BaseModel):
    rate: Decimal

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, data):
        if isinstance(data, dict):
            for name, info in cls.model_fields.items():
                if not info.is_required():
                    continue
                value = data.get(name)
                if value is None or not str(value).strip():
                    raise NullFormFieldError
        return data