import strawberry
from pydantic import BaseModel


class HistoryWeatherRequest(BaseModel):
    city: str
    date: str


class HistoryWeatherBase(BaseModel):
    city: str
    date: str
    temperature: float
    humidity: float
    id: str or None = None
    error: str or None = None


@strawberry.experimental.pydantic.type(model=HistoryWeatherBase, all_fields=True)
class HistoryWeatherType:
    pass

