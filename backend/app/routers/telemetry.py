"""Telemetry and player feedback endpoints blueprint."""

from __future__ import annotations

from fastapi import APIRouter

from ..schemas import (
    BugReportRequest,
    CompletePuzzleTelemetryRequest,
    HardWordsFeedbackRequest,
    MessageResponse,
)

router = APIRouter(prefix="/telemetry", tags=["telemetry"])


@router.post("/complete", response_model=MessageResponse)
def submit_completed_puzzle(payload: CompletePuzzleTelemetryRequest) -> MessageResponse:
    """Ingest end-of-game telemetry used for dynamic Elo-like difficulty updates."""
    _ = payload
    return MessageResponse(message="Completion telemetry endpoint blueprint ready")


@router.post("/word-feedback", response_model=MessageResponse)
def submit_hard_word_feedback(payload: HardWordsFeedbackRequest) -> MessageResponse:
    """Collect explicit 'Schwere Wörter' feedback."""
    _ = payload
    return MessageResponse(message="Hard word feedback endpoint blueprint ready")


@router.post("/bug-report", response_model=MessageResponse)
def submit_bug_report(payload: BugReportRequest) -> MessageResponse:
    """Capture bug report payload with game-state and clue context."""
    _ = payload
    return MessageResponse(message="Bug report endpoint blueprint ready")
