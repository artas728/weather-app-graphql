from odmantic import Model

class HistoryWeatherDB(Model):
    city: str
    date: str
    temperature: float
    humidity: float