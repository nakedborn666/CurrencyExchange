from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from decimal import Decimal
from exceptions.exceptions import NullFormFieldError

class ExchangeRateCreateDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    baseCurrencyCode: str = Field(pattern=r"^[A-Z]{3}$")
    targetCurrencyCode: str = Field(pattern=r"^[A-Z]{3}$")
    rate: Decimal

    @field_validator("baseCurrencyCode", "targetCurrencyCode", mode="before")
    @classmethod
    def validate_code(cls, value):
        if isinstance(value, str):
            return value.upper()

        return value

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