import uuid
from datetime import datetime, date
from sqlalchemy import String, Date, JSON, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
import enum

class PuzzleType(str, enum.Enum):
    wordle = "wordle"
    sudoku = "sudoku"
    crossword = "crossword"

class Difficulty(str, enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"

class Puzzle(Base):
    __tablename__ = "puzzles"
    __table_args__ = (UniqueConstraint("puzzle_type", "date", name="uq_puzzle_type_date"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    puzzle_type: Mapped[str] = mapped_column(String(20), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    content: Mapped[dict] = mapped_column(JSON, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(10), nullable=False, default="medium")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
