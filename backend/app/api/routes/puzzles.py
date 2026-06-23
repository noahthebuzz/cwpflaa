from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from app.db.session import get_db
from app.services.puzzle_service import get_today_puzzle, get_puzzle_by_date
from app.services.wordle_service import validate_guess
from app.models.puzzle import Puzzle
from app.models.user_progress import UserProgress
from app.core.dependencies import get_current_active_user
from app.models.user import User
import uuid
from datetime import date

router = APIRouter(prefix="/puzzles", tags=["puzzles"])

def strip_solution(puzzle):
    content = dict(puzzle.content)
    content.pop("word", None)
    content.pop("solution", None)
    return {
        "id": str(puzzle.id),
        "puzzle_type": puzzle.puzzle_type,
        "date": str(puzzle.date),
        "difficulty": puzzle.difficulty,
        "content": content,
    }

@router.get("/today")
async def get_today_puzzles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Puzzle).where(Puzzle.date == date.today()))
    puzzles = result.scalars().all()
    return [strip_solution(p) for p in puzzles]

@router.get("/today/{puzzle_type}")
async def get_today_puzzle_by_type(puzzle_type: str, db: AsyncSession = Depends(get_db)):
    puzzle = await get_today_puzzle(db, puzzle_type)
    return strip_solution(puzzle)

class WordleGuessRequest(BaseModel):
    guess: str

@router.post("/{puzzle_id}/wordle/guess")
async def wordle_guess(
    puzzle_id: str,
    body: WordleGuessRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_current_active_user),
):
    result = await db.execute(select(Puzzle).where(Puzzle.id == uuid.UUID(puzzle_id)))
    puzzle = result.scalar_one_or_none()
    if not puzzle or puzzle.puzzle_type != "wordle":
        raise HTTPException(status_code=404, detail="Puzzle not found")

    target_word = puzzle.content["word"].upper()
    guess = body.guess.upper().strip()

    if len(guess) != len(target_word):
        raise HTTPException(status_code=400, detail=f"Guess must be {len(target_word)} letters")

    feedback = validate_guess(guess, target_word)
    is_correct = guess == target_word

    # Save progress if authenticated
    if current_user:
        prog_result = await db.execute(
            select(UserProgress).where(
                UserProgress.user_id == current_user.id,
                UserProgress.puzzle_id == puzzle.id,
            )
        )
        progress = prog_result.scalar_one_or_none()
        if not progress:
            progress = UserProgress(
                user_id=current_user.id,
                puzzle_id=puzzle.id,
                status="pending",
                attempts=0,
                solution_state={"guesses": []},
            )
            db.add(progress)

        progress.attempts += 1
        guesses = progress.solution_state.get("guesses", [])
        guesses.append({"guess": guess, "feedback": feedback})
        progress.solution_state = {"guesses": guesses}

        if is_correct:
            from datetime import datetime, timezone
            progress.status = "completed"
            progress.completed_at = datetime.now(timezone.utc)
        elif progress.attempts >= puzzle.content.get("max_attempts", 6):
            progress.status = "failed"

        await db.commit()

    return {
        "guess": guess,
        "feedback": feedback,
        "is_correct": is_correct,
    }
