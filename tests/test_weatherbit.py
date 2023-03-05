import pytest
import asyncio
from app.connectors.weather.connector import WeatherConnector
from app.connectors.weather.provider_factory import WeatherProviderFactory

factory = WeatherProviderFactory()
connector = WeatherConnector(factory)
provider = connector.get_provider('weatherbit', api_key="3a290c76151141ff8de61e3553617df9", cities_filename="../app/weatherbit_cities_all.csv")

@pytest.mark.asyncio
async def test_get_weather_data():
    result = await provider.get_weather_data(city="London", date="2020-01-01")
    assert result.city == "London"
    assert result.date == "2020-01-01"
    assert -20.0 <= result.temperature <= 100.0
    assert 20.0 <= result.humidity <= 100.0


@pytest.mark.asyncio
async def test_get_weather_data_wrong_city():
    with pytest.raises(Exception) as e:
        await provider.get_weather_data(city="london", date="2020-01-01")
    assert str(e.value) == "City name should start with capital letter"

@pytest.mark.asyncio
async def test_get_weather_data_wrong_date():
    with pytest.raises(Exception) as e:
        await provider.get_weather_data(city="London", date="2020-01-01-01")
    assert str(e.value) == "Expected Date in following format: %Y-%m-%d"

@pytest.mark.asyncio
async def test_get_weather_data_wrong_city_name():
    with pytest.raises(Exception) as e:
        await provider.get_weather_data(city="Lond", date="2020-01-01")
    assert str(e.value) == "City Lond not found"

# TODO
# @pytest.mark.asyncio
# async def test_get_weather_data_wrong_api_key():
#     provider = connector.get_provider('weatherbit', api_key="3a290c76151141ff8de61e3553617df9_", cities_filename="../app/weatherbit_cities_all.csv")
#     with pytest.raises(Exception) as e:
#         await provider.get_weather_data(city="London", date="2020-01-01")
#     assert str(e.value) == "Invalid response from API. Code: 401,  Reason: Unauthorized"