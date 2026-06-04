import uuid
from datetime import datetime, timezone
from app.database import Base
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Uuid

class CW_Puzzle(Base):
    __tablename__ = "crossword puzzles"

    puzzle_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    date: Mapped[datetime.date] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc).date())