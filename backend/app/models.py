"""SQLAlchemy models for the crossword platform domain."""

from __future__ import annotations

from datetime import UTC, date, datetime

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    invitation_code_used: Mapped[str] = mapped_column(String(6), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    leaderboard_entries: Mapped[list[Leaderboard]] = relationship(back_populates="user")
    game_state_sessions: Mapped[list[GameStateSession]] = relationship(back_populates="user")
    bug_reports: Mapped[list[BugReport]] = relationship(back_populates="user")


class WordPool(Base):
    __tablename__ = "word_pool"
    __table_args__ = (
        UniqueConstraint("normalized_answer", name="uq_word_pool_normalized_answer"),
        CheckConstraint("length(normalized_answer) > 0", name="ck_word_not_empty"),
        CheckConstraint(
            "normalized_answer NOT GLOB '*[^A-Z]*'",
            name="ck_word_upper_latin_only",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    clue: Mapped[str] = mapped_column(Text, nullable=False)
    normalized_answer: Mapped[str] = mapped_column(String(64), nullable=False)

    difficulty_rating: Mapped[float] = mapped_column(Float, default=1000.0, nullable=False)
    times_seen: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_solves: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    first_try_successes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    typo_tolerant_successes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    hard_feedback_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_used_on: Mapped[date | None] = mapped_column(Date)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), nullable=False
    )


class PuzzleQueue(Base):
    __tablename__ = "puzzle_queue"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scheduled_for: Mapped[date] = mapped_column(Date, unique=True, nullable=False)
    puzzle_payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    regenerated_by_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class Leaderboard(Base):
    __tablename__ = "leaderboard"
    __table_args__ = (
        UniqueConstraint("user_id", "puzzle_date", name="uq_leaderboard_user_puzzle"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    puzzle_date: Mapped[date] = mapped_column(Date, nullable=False)

    completion_seconds: Mapped[int] = mapped_column(Integer, nullable=False)
    first_try_word_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    typo_tolerant_word_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    finished_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    user: Mapped[User] = relationship(back_populates="leaderboard_entries")


class GameStateSession(Base):
    __tablename__ = "game_state_sessions"
    __table_args__ = (
        UniqueConstraint("user_id", "puzzle_date", name="uq_game_state_user_puzzle"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    puzzle_date: Mapped[date] = mapped_column(Date, nullable=False)

    state_payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    elapsed_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    timer_hidden: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), nullable=False
    )

    user: Mapped[User] = relationship(back_populates="game_state_sessions")


class BugReport(Base):
    __tablename__ = "bug_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    puzzle_date: Mapped[date] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    raw_game_state: Mapped[dict] = mapped_column(JSON, nullable=False)
    grid_coordinates: Mapped[dict] = mapped_column(JSON, nullable=False)
    active_clue_metadata: Mapped[dict] = mapped_column(JSON, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    resolved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user: Mapped[User | None] = relationship(back_populates="bug_reports")
