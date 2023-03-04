from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from app.models import HistoryWeatherRequest
from app.settings import settings
from odmantic import Model

class HistoryWeatherODM(Model):
    city: str
    date: str
    temperature: float
    humidity: float

def get_db_connection():
    return DBConnector(url=settings.DATABASE_URL, database=settings.MONGO_DB)

class DBConnector():
    def __init__(self, url: str, database: str):
        client = AsyncIOMotorClient(url)
        self.engine = AIOEngine(client=client, database=database)

    async def save_favourite(self, history_weather: HistoryWeatherODM):
        if await self._check_if_exist_in_db(history_weather):
            return history_weather
        return await self.engine.save(history_weather)

    async def get_weather_data(self, weather_request: HistoryWeatherRequest) -> HistoryWeatherODM:
        return await self.engine.find_one(
            HistoryWeatherODM,
            HistoryWeatherODM.city == weather_request.city,
            HistoryWeatherODM.date == weather_request.date
        )

    async def _check_if_exist_in_db(self, history_weather: HistoryWeatherODM) -> int:
        return await self.engine.count(
            HistoryWeatherODM,
            HistoryWeatherODM.city == history_weather.city,
            HistoryWeatherODM.date == history_weather.date
        )

    async def get_all_favourites(self):
        return await self.engine.find(HistoryWeatherODM)