import strawberry
from pydantic import BaseModel


class HistoryWeather(BaseModel):
    city: str
    date: str
    temperature: float
    humidity: float
    id: str = None

class HistoryWeatherRequest(BaseModel):
    city: str
    date: str


@strawberry.experimental.pydantic.type(model=HistoryWeather, all_fields=True)
class HistoryWeatherType:
    pass

