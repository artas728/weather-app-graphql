import pytest
import httpx
from app.main import app
from typing import AsyncIterator

@pytest.fixture()
async def client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

@pytest.fixture()
def anyio_backend() -> str:
    return "asyncio"

@pytest.mark.anyio
async def test_fastapi_graphql_query(client: httpx.AsyncClient) -> None:
    result = await client.post(
        "/graphql",
        json={
            "query": """
                query {
                    weather(city: "London", date: "2020-01-01") {
                        city
                        date
                        temperature
                        humidity
                    }
                }
            """
        }
    )
    assert result.status_code == 200
    response = result.json()
    assert "data" in response
    assert "weather" in response["data"]
    assert "city" in response["data"]["weather"]
    assert response["data"]["weather"]["city"] == "London"
    assert "date" in response["data"]["weather"]
    assert response["data"]["weather"]["date"] == "2020-01-01"
    assert "temperature" in response["data"]["weather"]
    assert "humidity" in response["data"]["weather"]

@pytest.mark.anyio
async def test_fastapi_graphql_mutation(client: httpx.AsyncClient) -> None:
    result = await client.post(
        "/graphql",
        json={
            "query": """
                mutation {
                    createFavorite(city: "London", date: "2020-01-01", temperature: 3.0, humidity: 93.0) {
                        city
                        date
                        temperature
                        humidity
                    }
                }
            """
        }
    )
    assert result.status_code == 200
    assert result.json() == {
        "data": {
            "createFavorite": {
                "city": "London",
                "date": "2020-01-01",
                "temperature": 3.0,
                "humidity": 93.0
            }
        }
    }

@pytest.mark.anyio
async def test_fastapi_graphql_query_favorites(client: httpx.AsyncClient) -> None:
    result = await client.post(
        "/graphql",
        json={
            "query": """
                query {
                    favorites {
                        city
                        date
                        temperature
                        humidity
                    }
                }
            """
        }
    )
    assert result.status_code == 200
    assert result.json() == {
        "data": {
            "favorites": [
                {
                    "city": "London",
                    "date": "2020-01-01",
                    "temperature": 3.0,
                    "humidity": 93.0
                }
            ]
        }
    }