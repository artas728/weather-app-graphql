from typing import List, Dict
from app.models import HistoryWeatherType
from app.connectors.db.connector import get_db_connection
from app.connectors.weather.connector import get_weather_connection


db_connector = get_db_connection()
provider = get_weather_connection()


async def get_weather(city: str, date: str) -> HistoryWeatherType:
    weather_data = await provider.get_weather_data(city=city, date=date)
    return HistoryWeatherType(**weather_data)

async def get_all_favourites() -> List[HistoryWeatherType]:
    data = await db_connector.get_all_favorites()
    return [HistoryWeatherType(**item) for item in data]

async def save_favorite(city: str, date: str, temperature: float, humidity: float) -> HistoryWeatherType:
    result: Dict = await db_connector.save_favorite(
        city=city,
        date=date,
        temperature=temperature,
        humidity=humidity
    )
    return HistoryWeatherType(**result)