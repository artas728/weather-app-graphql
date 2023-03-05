import pytest
import asyncio
from app.connectors.db.db_models import HistoryWeatherDB
from app.models import HistoryWeatherRequest
from app.connectors.db.connector import get_db_connection


db_connector = get_db_connection()
db_connector.engine.client.get_io_loop = asyncio.get_event_loop


@pytest.mark.asyncio
async def test_save_favorite():
    result = await db_connector.save_favorite(
        city="London",
        date="2020-01-01",
        temperature=3.0,
        humidity=93.0
    )
    assert result["city"] == "London"
    assert result["date"] == "2020-01-01"
    assert result["temperature"] == 3.0
    assert result["humidity"] == 93.0

@pytest.mark.asyncio
async def test_get_all_favourites():
    result = await db_connector.get_all_favorites()
    assert len(result) == 1
    assert result[0]["city"] == "London"
    assert result[0]["date"] == "2020-01-01"
    assert result[0]["temperature"] == 3.0
    assert result[0]["humidity"] == 93.0

@pytest.mark.asyncio
async def test_get_weather_data():
    result = await db_connector.get_weather_data(HistoryWeatherRequest(
        city="London",
        date="2020-01-01"
    ))
    assert result["city"] == "London"
    assert result["date"] == "2020-01-01"
    assert result["temperature"] == 3.0
    assert result["humidity"] == 93.0

@pytest.mark.asyncio
async def test_get_weather_data_not_found():
    result = await db_connector.get_weather_data(HistoryWeatherRequest(
        city="London",
        date="2020-01-02"
    ))
    assert result is None

@pytest.mark.asyncio
async def test_check_if_exist_in_db():
    result = await db_connector._check_if_exist_in_db(HistoryWeatherDB(
        city="London",
        date="2020-01-01",
        temperature=1.0,
        humidity=60.0,
    ))
    assert result == 1

@pytest.mark.asyncio
async def test_check_if_exist_in_db_not_found():
    result = await db_connector._check_if_exist_in_db(HistoryWeatherDB(
        city="London",
        date="2020-01-02",
        temperature=1.0,
        humidity=60.0,
    ))
    assert result == 0