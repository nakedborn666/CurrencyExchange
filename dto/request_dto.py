from pydantic import BaseModel
from dto.query_dto import QueryDTO

class RequestDTO(BaseModel):
    form: dict[str, str] | None = None
    method: str
    route: str
    parameter: str| list | None = None
    query: QueryDTO | None = None