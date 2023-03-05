"""
Interface class that calls a specific weather provider
"""
from app.connectors.weather.provider_factory import WeatherProviderFactory
from app.settings import settings

def get_weather_connection():
    factory = WeatherProviderFactory()
    connector = WeatherConnector(factory)
    return connector.get_provider('weatherbit', api_key=settings.WEATHER_API_KEY, cities_filename=settings.CITIES_FILENAME)

class WeatherConnector:
    # Initialize with a factory object
    def __init__(self, provider_factory):
        self.provider_factory = provider_factory

    # Use the factory to get a specific weather provider
    def get_provider(self, provider_name, *args, **kwargs):
        return self.provider_factory.get_provider(provider_name, *args, **kwargs)