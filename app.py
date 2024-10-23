from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import strawberry
from utils.database import engine, SessionLocal
from models import Base

# Create the FastAPI application
app = FastAPI()


# Create a GraphQL schema
@strawberry.type
class Query:
    hello: str

    @strawberry.field
    def resolve_hello(self) -> str:
        return "Hello, World!"


schema = strawberry.Schema(query=Query)

# Create a GraphQL router
graphql_app = GraphQLRouter(schema)

# Include the GraphQL router in the FastAPI app
app.include_router(graphql_app, prefix="/graphql")


# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize the database
def init_db():
    Base.metadata.create_all(bind=engine)


# Run database initialization (create tables)
init_db()


# You can add more routes as needed
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
