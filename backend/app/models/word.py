from sqlalchemy import Integer, String, Float, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from app.database import Base


class Word(Base):
    __tablename__ = "words"
    __table_args__ = (
        UniqueConstraint('text', 'clue', name='uq_word_clue'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    clue: Mapped[str] = mapped_column(String(255), nullable=False)
    elo: Mapped[float] = mapped_column(Float, nullable=False, default=1000.0)  # IRT-based difficulty rating
    usage_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Word(id={self.id}, text={self.text}, clue={self.clue}, elo={self.elo})>"
