import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_TITLE: str = "FastApi GraphQL Strawberry Weather App"
    PROJECT_VERSION: str = "0.0.1"
    HOST_HTTP: str = os.environ.get("HOST_HTTP" ,"http://")
    HOST_URL: str = os.environ.get("HOST_URL")
    HOST_PORT: int = int(os.environ.get("HOST_PORT"))
    BASE_URL: str = HOST_HTTP + HOST_URL +": " +str(HOST_PORT)

    WEATHER_API_KEY = os.environ.get("WEATHERBIT_API_KEY")
    CITIES_FILENAME = os.environ.get("CITIES_FILENAME")

    MONGO_USER: str = os.environ.get("MONGO_USERNAME")
    MONGO_PASSWORD: str = os.environ.get("MONGO_PASSWORD")
    MONGO_DB: str = os.environ.get("MONGO_DATABASE")
    MONGO_SERVER: str = os.environ.get("MONGO_SERVER")
    MONGO_PORT: int = int(os.environ.get("MONGO_PORT", 5432))
    DATABASE_URL: str = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}" \
                        f"@{MONGO_SERVER}:{MONGO_PORT}" if MONGO_USER and MONGO_PASSWORD \
                        else f"{MONGO_SERVER}:{MONGO_PORT}"

settings = Settings()