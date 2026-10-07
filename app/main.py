from fastapi import FastAPI

from .database import Base, engine
from .routes import router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Bulk Certificate Generator API",
    description="API for generating certificates in bulk"
)


app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Bulk Certificate Generator API is running"
    }