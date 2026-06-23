#!/usr/bin/env python3
"""Seed Wordle puzzles for the next 30 days."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date, timedelta
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from app.models.puzzle import Puzzle
from app.db.base_all import Base
from app.core.config import settings

WORDS = [
    "HAUS", "BAUM", "HUND", "BUCH", "TISCH", "STUHL", "BRIEF", "BLUME",
    "GLAS", "LAMPE", "MUSIK", "NACHT", "PFERD", "REGEN", "SCHAF", "STERN",
    "TIGER", "VOGEL", "WAGEN", "ZEBRA", "APFEL", "BIRNE", "BUSCH", "DACHS",
    "EIMER", "FISCH", "GABEL", "IGEL", "JOKER", "KAMEL", "LACHS",
    "MAUER", "NEBEL", "OSTEN", "PALME",
]

def seed():
    sync_url = settings.DATABASE_URL.replace("+asyncpg", "")
    engine = create_engine(sync_url)
    today = date.today()

    with Session(engine) as db:
        for i in range(30):
            puzzle_date = today + timedelta(days=i)
            word = WORDS[i % len(WORDS)]
            # skip if already exists
            existing = db.execute(
                select(Puzzle).where(
                    Puzzle.puzzle_type == "wordle",
                    Puzzle.date == puzzle_date
                )
            ).scalar_one_or_none()
            if existing:
                print(f"  skip {puzzle_date} (already seeded)")
                continue
            puzzle = Puzzle(
                puzzle_type="wordle",
                date=puzzle_date,
                content={"word": word, "word_length": len(word), "max_attempts": 6},
                difficulty="medium",
            )
            db.add(puzzle)
            print(f"  seeded {puzzle_date}: {word}")
        db.commit()
    print("Done.")

if __name__ == "__main__":
    seed()
