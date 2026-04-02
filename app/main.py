import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager

from app.api.endpoints import router
from app.db.database import engine, Base
from app.db.redis import redis_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables automatically on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield

    # Cleanup connections on shutdown
    await redis_client.aclose()
    await engine.dispose()

app = FastAPI(
    title="URL Shortener API",
    description="High-throughput URL shortener with Redis caching and SQLite analytics",
    version="1.0.0",
    lifespan=lifespan
)

# Mount static folder
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", include_in_schema=False)
async def serve_frontend():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend not found."}

app.include_router(router)
