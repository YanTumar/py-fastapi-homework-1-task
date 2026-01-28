from contextlib import asynccontextmanager
from fastapi import FastAPI

from database.session import init_db, close_db
from routes.movies import router as movie_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()

app = FastAPI(lifespan=lifespan)

app.include_router(movie_router, prefix="/api/v1/theater/movies", tags=["Movies"])

@app.get("/")
async def root():
    return {"message": "Movie API is running"}
