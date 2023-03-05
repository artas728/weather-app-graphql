import typing
import strawberry
from app.models import HistoryWeatherType
from app.resolvers import get_weather, get_all_favourites, save_favorite


@strawberry.type
class Query:
    @strawberry.field
    async def weather(self, city: str, date: str) -> HistoryWeatherType:
        return await get_weather(city=city, date=date)

    @strawberry.field
    async def favorites(self) -> typing.List[HistoryWeatherType]:
        return await get_all_favourites()


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_favorite(
            self,
            city: str,
            date: str,
            temperature: float,
            humidity: float
    ) -> HistoryWeatherType:
        return await save_favorite(city, date, temperature, humidity)