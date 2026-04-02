from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse
import redis.asyncio as redis

from app.db import schemas, crud
from app.db.database import get_db
from app.db.redis import get_redis
from app.core.config import settings

router = APIRouter()

@router.post("/api/shorten", response_model=schemas.UrlResponse)
async def create_short_url(
    url_req: schemas.UrlCreate,
    db: AsyncSession = Depends(get_db)
):
    db_url = await crud.create_short_url(db, str(url_req.url))
    return {
        "original_url": db_url.original_url,
        "short_id": db_url.short_id,
        "short_url": f"{settings.BASE_URL}{db_url.short_id}"
    }

@router.get("/{short_id}")
async def redirect_to_url(
    short_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis)
):
    # Try getting from Redis first
    cache_key = f"url:{short_id}"
    cache_val = await redis_client.get(cache_key)

    url_id = None
    original_url = None

    if cache_val:
        parts = cache_val.split("||", 1)
        if len(parts) == 2:
            url_id = int(parts[0])
            original_url = parts[1]
    
    if not original_url:
        # Cache miss, fetch from DB
        db_url = await crud.get_url_by_short_id(db, short_id)
        if db_url is None:
            raise HTTPException(status_code=404, detail="URL not found")
        original_url = db_url.original_url
        url_id = db_url.id

        # Populate cache
        await redis_client.set(cache_key, f"{url_id}||{original_url}", ex=3600*24)
        
    if url_id:
        client_ip = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        await crud.create_click_event(db, url_id, client_ip, user_agent)

    return RedirectResponse(original_url, status_code=307)

@router.get("/api/analytics/{short_id}", response_model=schemas.AnalyticsResponse)
async def get_analytics(
    short_id: str,
    db: AsyncSession = Depends(get_db)
):
    db_url = await crud.get_url_by_short_id(db, short_id)
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    
    analytics = await crud.get_url_analytics(db, db_url.id)
    return analytics
