from datetime import datetime
from sqlalchemy import  Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from zoneinfo import ZoneInfo
from database import Base
from message.models import Message

zone = ZoneInfo("Europe/Moscow")

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(zone))

    messages: Mapped[list["Message"]] = relationship(back_populates="user")