import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Url(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True, nullable=False)
    short_id = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    clicks = relationship("ClickEvent", back_populates="url", cascade="all, delete-orphan")

class ClickEvent(Base):
    __tablename__ = "clicks"

    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer, ForeignKey("urls.id"))
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    clicked_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    url = relationship("Url", back_populates="clicks")
