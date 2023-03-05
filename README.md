# weather-app-graphql

## How to run

1. Add WEATHERBIT_API_KEY to envs/.env.container

2. `docker-compose up`

## How to use

1. Open http://localhost:8000/graphql

2. Run queries:

```
query {
  weather(city: "Portland", date: "2020-01-01") {
    city
    date
    temperature
    humidity
  }
}
```

```
mutation {
  createFavorite(city: "Portland", date: "2020-01-01", temperature: -1, humidity: 0.5) {
    city
    date
    temperature
    humidity
  }
}
```

```
query {
  favorites {
    city
    date
    temperature
    humidity
  }
}
```