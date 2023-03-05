from typing import Dict
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from app.models import HistoryWeatherRequest
from app.connectors.db.db_models import HistoryWeatherDB
from app.settings import settings


class DBConnector:
    def __init__(self, url: str, database: str):
        client = AsyncIOMotorClient(url)
        self.engine = AIOEngine(client=client, database=database)

    async def save_favorite(self, city: str, date: str, temperature: float, humidity: float) -> Dict:
        history_weather = HistoryWeatherDB(
            city=city,
            date=date,
            temperature=temperature,
            humidity=humidity
        )
        if await self._check_if_exist_in_db(history_weather):
            return history_weather.dict()
        return (await self.engine.save(history_weather)).dict()

    async def get_weather_data(self, weather_request: HistoryWeatherRequest) -> HistoryWeatherDB:
        data = await self.engine.find_one(
            HistoryWeatherDB,
            HistoryWeatherDB.city == weather_request.city,
            HistoryWeatherDB.date == weather_request.date
        )
        if data:
            return data.dict()

    async def _check_if_exist_in_db(self, history_weather: HistoryWeatherDB) -> int:
        return await self.engine.count(
            HistoryWeatherDB,
            HistoryWeatherDB.city == history_weather.city,
            HistoryWeatherDB.date == history_weather.date
        )

    async def get_all_favourites(self):
        return [item.dict() for item in await self.engine.find(HistoryWeatherDB)]


def get_db_connection() -> DBConnector:
    return DBConnector(url=settings.DATABASE_URL, database=settings.MONGO_DB)