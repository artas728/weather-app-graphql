import typing
from app.models import HistoryWeatherType
from app.connectors.db.connector import get_db_connection, HistoryWeatherODM
from app.connectors.weather.connector import get_weather_connection


db_connector = get_db_connection()
provider = get_weather_connection()


async def get_weather(city: str, date: str) -> HistoryWeatherType:
    return await provider.get_weather_data(city=city, date=date)

async def get_all_favourites() -> typing.List[HistoryWeatherType]:
    data = await db_connector.get_all_favourites()
    return [HistoryWeatherType(**item.__dict__) for item in data]

async def save_favorite(city: str, date: str, temperature: float, humidity: float) -> HistoryWeatherType:
    result: HistoryWeatherODM = await db_connector.save_favourite(HistoryWeatherODM(
        city=city,
        date=date,
        temperature=temperature,
        humidity=humidity
    ))
    return HistoryWeatherType(**result.__dict__)