from pydantic import BaseModel
import json
from decimal import Decimal


def json_default(value):
    if isinstance(value, Decimal):
        return float(value)
    return str(value)


def serialize_data_to_json(data):
    if isinstance(data, BaseModel):
        data = data.model_dump()
    elif isinstance(data, list):
        data = [elem.model_dump() if isinstance(elem, BaseModel) else elem for elem in data]
    return json.dumps(data, default=json_default, ensure_ascii=False)


