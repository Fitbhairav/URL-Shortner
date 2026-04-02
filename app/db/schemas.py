from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime

class UrlCreate(BaseModel):
    url: HttpUrl

class UrlResponse(BaseModel):
    original_url: str
    short_id: str
    short_url: str

class ClickResponse(BaseModel):
    ip_address: Optional[str]
    user_agent: Optional[str]
    clicked_at: datetime

    class Config:
        from_attributes = True

class AnalyticsResponse(BaseModel):
    total_clicks: int
    clicks: List[ClickResponse]
