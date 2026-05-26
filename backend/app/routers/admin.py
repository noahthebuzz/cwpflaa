"""Admin operational dashboard endpoint blueprints."""

from __future__ import annotations

from fastapi import APIRouter

from ..schemas import AdminRegeneratePuzzleRequest, MessageResponse

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/queue", response_model=dict)
def get_queue_overview() -> dict:
    """Preview the 6-day puzzle queue for QA play-testing."""
    return {"queue": []}


@router.post("/puzzles/regenerate", response_model=MessageResponse)
def regenerate_queued_puzzle(payload: AdminRegeneratePuzzleRequest) -> MessageResponse:
    """Force regenerate a puzzle in the forward queue."""
    _ = payload
    return MessageResponse(message="Admin regenerate endpoint blueprint ready")
