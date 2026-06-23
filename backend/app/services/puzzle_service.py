from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.puzzle import Puzzle

async def get_today_puzzle(db: AsyncSession, puzzle_type: str) -> Puzzle:
    today = date.today()
    result = await db.execute(
        select(Puzzle).where(Puzzle.puzzle_type == puzzle_type, Puzzle.date == today)
    )
    puzzle = result.scalar_one_or_none()
    if not puzzle:
        raise HTTPException(status_code=404, detail=f"No {puzzle_type} puzzle for today")
    return puzzle

async def get_puzzle_by_date(db: AsyncSession, puzzle_date: date, puzzle_type: str) -> Puzzle:
    result = await db.execute(
        select(Puzzle).where(Puzzle.puzzle_type == puzzle_type, Puzzle.date == puzzle_date)
    )
    puzzle = result.scalar_one_or_none()
    if not puzzle:
        raise HTTPException(status_code=404, detail=f"No {puzzle_type} puzzle for {puzzle_date}")
    return puzzle

async def seed_puzzle(db: AsyncSession, puzzle_date: date, puzzle_type: str, content: dict, difficulty: str = "medium") -> Puzzle:
    # Check if already exists
    result = await db.execute(
        select(Puzzle).where(Puzzle.puzzle_type == puzzle_type, Puzzle.date == puzzle_date)
    )
    existing = result.scalar_one_or_none()
    if existing:
        return existing
    puzzle = Puzzle(puzzle_type=puzzle_type, date=puzzle_date, content=content, difficulty=difficulty)
    db.add(puzzle)
    await db.commit()
    await db.refresh(puzzle)
    return puzzle
