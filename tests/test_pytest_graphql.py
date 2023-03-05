import asyncio

import pytest
import strawberry
from app.schema import Query, Mutation
from app.connectors.db.connector import get_db_connection


db_connector = get_db_connection()
db_connector.engine.client.get_io_loop = asyncio.get_event_loop

schema = strawberry.Schema(query=Query, mutation=Mutation)

@pytest.mark.asyncio
async def test_graphql_query():
    result = await schema.execute(
        """
        query {
            weather(city: "London", date: "2020-01-01") {
                city
                date
                temperature
                humidity
            }
        }
        """
    )
    assert result.data["weather"]["city"] == "London"
    assert result.data["weather"]["date"] == "2020-01-01"
    assert -20.0 <= result.data["weather"]["temperature"] <= 100.0
    assert 20.0 <= result.data["weather"]["humidity"] <= 100.0

@pytest.mark.asyncio
async def test_graphql_query_wrong_city():
    result = await schema.execute(
        """
        query {
            weather(city: "london", date: "2020-01-01") {
                city
                date
                temperature
                humidity
            }
        }
        """
    )
    assert result.errors[0].message == "City name should start with capital letter"

@pytest.mark.asyncio
async def test_graphql_query_wrong_date():
    result = await schema.execute(
        """
        query {
            weather(city: "London", date: "2020-01-01-01") {
                city
                date
                temperature
                humidity
            }
        }
        """
    )
    assert result.errors[0].message == "Expected Date in following format: %Y-%m-%d"

@pytest.mark.asyncio
async def test_graphql_query_wrong_city_name():
    result = await schema.execute(
        """
        query {
            weather(city: "Lond", date: "2020-01-01") {
                city
                date
                temperature
                humidity
            }
        }
        """
    )
    assert result.errors[0].message == "City Lond not found"

# @pytest.mark.asyncio
# async def test_graphql_query_wrong_api_key():
#     result = await schema.execute(
#         """
#         query {
#             weather(city: "London", date: "2020-01-01") {
#                 city
#                 date
#                 temperature
#                 humidity
#             }
#         }
#         """
#     )
#     assert result.errors[0].message == "Invalid response from API. Code: 401,  Reason: Unauthorized"

@pytest.mark.asyncio
async def test_graphql_mutation():
    result = await schema.execute(
        """
        mutation {
            createFavorite(city: "London", date: "2020-01-01", temperature: 3.0, humidity: 93.0) {
                city
                date
                temperature
                humidity
            }
        }
        """
    )
    assert result.data["createFavorite"]["city"] == "London"
    assert result.data["createFavorite"]["date"] == "2020-01-01"
    assert result.data["createFavorite"]["temperature"] == 3.0
    assert result.data["createFavorite"]["humidity"] == 93.0