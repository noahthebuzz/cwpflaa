"""Pydantic request/response schemas for API blueprints."""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=255)
    invitation_code: str = Field(pattern=r"^\d{6}$")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=255)


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PuzzleResponse(BaseModel):
    puzzle_date: date
    payload: dict


class SaveGameStateRequest(BaseModel):
    puzzle_date: date
    elapsed_seconds: int = Field(ge=0)
    timer_hidden: bool = False
    state_payload: dict
    is_completed: bool = False


class CompletedWordTelemetry(BaseModel):
    word_id: int
    attempts: list[str] = Field(default_factory=list)
    flagged_hard: bool = False


class CompletePuzzleTelemetryRequest(BaseModel):
    puzzle_date: date
    completion_seconds: int = Field(ge=0)
    words: list[CompletedWordTelemetry]


class HardWordsFeedbackRequest(BaseModel):
    puzzle_date: date
    hard_word_ids: list[int] = Field(default_factory=list)


class BugReportRequest(BaseModel):
    puzzle_date: date
    description: str = Field(min_length=5, max_length=5000)
    raw_game_state: dict
    grid_coordinates: dict
    active_clue_metadata: dict


class AdminRegeneratePuzzleRequest(BaseModel):
    scheduled_for: date
    force: bool = True


class MessageResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: str
