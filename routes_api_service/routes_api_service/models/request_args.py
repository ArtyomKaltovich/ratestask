from datetime import datetime

from pydantic import BaseModel, validator

from routes_api_service.const import DATE_FORMAT


class RequestArgs(BaseModel):
    origin: str
    destination: str
    date_from: str
    date_to: str

    @validator("date_from", "date_to")
    def date_validator(cls, v):
        return datetime.strptime(v, DATE_FORMAT)
