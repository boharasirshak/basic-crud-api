import enum
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, index=True, unique=True)
    name = Column(String, nullable=True, default="")
    password: str = Column(String, nullable=False)
    height = Column(Integer, nullable=True, default=0)
    weight = Column(Integer, nullable=True, default=0)
    age = Column(Integer, nullable=True, default=0)
    created_at = Column(DateTime(timezone=True), default=func.now())
