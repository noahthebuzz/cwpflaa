"""Puzzle retrieval and player-state endpoints blueprint."""

from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Query

from ..schemas import MessageResponse, PuzzleResponse, SaveGameStateRequest

router = APIRouter(tags=["puzzles"])


@router.get("/puzzles/daily", response_model=PuzzleResponse)
def get_daily_puzzle(target_date: date | None = Query(default=None)) -> PuzzleResponse:
    """Fetch the queued puzzle for today (or an explicit archive date)."""
    puzzle_date = target_date or date.today()
    return PuzzleResponse(puzzle_date=puzzle_date, payload={"cells": [], "words": []})


@router.post("/game-state/save", response_model=MessageResponse)
def save_game_state(payload: SaveGameStateRequest) -> MessageResponse:
    """Persist trusted client game-state snapshots."""
    _ = payload
    return MessageResponse(message="Game state save endpoint blueprint ready")
