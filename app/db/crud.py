from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.db import models
from app.core import shortener

async def create_short_url(db: AsyncSession, original_url: str) -> models.Url:
    short_id = shortener.generate_random_short_id()
    db_url = models.Url(original_url=original_url, short_id=short_id)
    db.add(db_url)
    await db.commit()
    await db.refresh(db_url)
    return db_url

async def get_url_by_short_id(db: AsyncSession, short_id: str) -> models.Url:
    result = await db.execute(select(models.Url).where(models.Url.short_id == short_id))
    return result.scalars().first()

async def create_click_event(db: AsyncSession, url_id: int, ip_address: str, user_agent: str) -> models.ClickEvent:
    click = models.ClickEvent(url_id=url_id, ip_address=ip_address, user_agent=user_agent)
    db.add(click)
    await db.commit()
    await db.refresh(click)
    return click

async def get_url_analytics(db: AsyncSession, url_id: int):
    # Get total clicks
    total_clicks_stmt = select(func.count(models.ClickEvent.id)).where(models.ClickEvent.url_id == url_id)
    total_clicks_result = await db.execute(total_clicks_stmt)
    total_clicks = total_clicks_result.scalar_one()

    # Get click history
    clicks_stmt = select(models.ClickEvent).where(models.ClickEvent.url_id == url_id).order_by(models.ClickEvent.clicked_at.desc())
    clicks_result = await db.execute(clicks_stmt)
    clicks = clicks_result.scalars().all()

    return {"total_clicks": total_clicks, "clicks": clicks}
