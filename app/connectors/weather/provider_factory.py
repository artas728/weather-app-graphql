"""
Factory class that creates specific weather providers
"""
from app.connectors.weather.weatherbit_provider import WeatherBitProvider


class WeatherProviderFactory:
    providers = {
        'weatherbit': WeatherBitProvider,
        # Add new providers here
    }

    def get_provider(self, provider_name, **kwargs):
        if provider_name in self.providers:
            return self.providers[provider_name](**kwargs)
        else:
            raise ValueError("Provider not found")