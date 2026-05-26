"""Authentication endpoints blueprint."""

from __future__ import annotations

from fastapi import APIRouter

from ..schemas import AuthResponse, LoginRequest, MessageResponse, RegisterRequest

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=MessageResponse)
def register_user(payload: RegisterRequest) -> MessageResponse:
    """Register a user with invitation-code-gated access."""
    _ = payload
    return MessageResponse(message="Registration endpoint blueprint ready")


@router.post("/login", response_model=AuthResponse)
def login_user(payload: LoginRequest) -> AuthResponse:
    """Issue a session token for authenticated access."""
    _ = payload
    return AuthResponse(access_token="replace-with-real-token")


@router.post("/logout", response_model=MessageResponse)
def logout_user() -> MessageResponse:
    """Invalidate active session for the current user."""
    return MessageResponse(message="Logout endpoint blueprint ready")
