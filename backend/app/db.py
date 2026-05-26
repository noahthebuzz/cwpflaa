"""Database primitives for the lightweight monolith."""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLITE_URL = "sqlite:///./cwpflaa.db"


class Base(DeclarativeBase):
    """Base declarative model class."""


engine = create_engine(SQLITE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
