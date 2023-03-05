import strawberry
import uvicorn
from fastapi import FastAPI
from strawberry.asgi import GraphQL
from app.schema import Query, Mutation





schema = strawberry.Schema(query=Query, mutation=Mutation)

# Create the FastAPI app
app = FastAPI()

# Add the GraphQL endpoint
app.add_route("/graphql", GraphQL(schema=schema))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)