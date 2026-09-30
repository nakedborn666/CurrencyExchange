from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from exceptions.exceptions import NullFormFieldError


class CurrencyCreateDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str = Field(min_length=1)
    code: str = Field(pattern=r"^[A-Z]{3}$")
    sign: str = Field(min_length=1, max_length=3)


    @field_validator("code", mode="before")
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