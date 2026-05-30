from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

_db_url = os.getenv("DATABASE_URL")
DATABASE_URL = _db_url.replace("postgres://", "postgresql://", 1)  # SQLAlchemy expects postgresql://, but Heroku provides postgres://

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()