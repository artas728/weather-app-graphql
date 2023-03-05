import datetime
import csv
import aiohttp
from app.models import HistoryWeather

class WeatherBitProvider:
    url = "https://api.weatherbit.io/v2.0/history/daily"
    default_cities_filename = "./weatherbit_cities_all.csv"
    date_format = '%Y-%m-%d'

    def __init__(self, api_key, cities_filename=None):
        self.api_key = api_key
        self.cities_map = {}
        if cities_filename:
            self.cities_filename = cities_filename
        else:
            self.cities_filename = self.default_cities_filename
        self._upload_cities_file(self.cities_filename)

    async def get_weather_data(self, city: str, date: str) -> HistoryWeather:
        self._validate_input_params(city, date)
        city_id = self._get_city_id(city)
        params = {
            'city_id': city_id,
            'start_date': date,
            'end_date': (datetime.datetime.strptime(date, self.date_format) + datetime.timedelta(days=1)).strftime(self.date_format),
            'key': self.api_key
        }
        try:
            if not hasattr(self, "session"):
                self.session = self._create_http_session()
            async with self.session.get(self.url, params=params) as resp:
                self._validate_response(resp)
                json = await resp.json()
                parsed = self._parse_json(json)
                return HistoryWeather(city=city, date=date, **parsed)
        except Exception as e:
            print(f"Error getting weather data: {e}")
            return {"error": "Failed! It seems we have problem with weather provider"}

    def _upload_cities_file(self, cities_filename):
        with open(cities_filename, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            for row in csv_reader:
                self.cities_map[row[1]] = row[0]
        return self.cities_map

    async def _create_http_session(self):
        """
        aiohtto required to create session inside a coroutine
        """
        self.session = aiohttp.ClientSession()

    def _validate_input_params(self, city_name, date):
        if not city_name[0].isupper():
            raise Exception("City name should start with capital letter")
        try:
            datetime.datetime.strptime(date, self.date_format)
        except ValueError:
            raise Exception(f"Expected Date in following format: {self.date_format}")

    def _get_city_id(self, city_name):
        if city_name in self.cities_map:
            return self.cities_map[city_name]
        else:
            raise Exception(f"City {city_name} not found")

    def _validate_response(self, resp):
        if resp.status != 200:
            raise Exception(f"Invalid response from API. Code: {resp.status},  Reason: {resp.reason}")

    def _parse_json(self, json):
        return {         # TODO: use dataclass!
            "temperature": json["data"][0]["temp"],
            "humidity": json["data"][0]["rh"]
        }