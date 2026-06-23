from fastapi import APIRouter, Depends, Response, Request, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.schemas.user import UserRead
from app.services import auth_service
from app.services.username_service import generate_unique_username
from app.core.dependencies import require_auth
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=201)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    user = await auth_service.register(db, data.email, data.password, data.username)
    return user

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    user, access_token, refresh_token = await auth_service.login(db, data.identifier, data.password)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="strict",
        max_age=7 * 24 * 3600
    )
    return TokenResponse(access_token=access_token)

@router.post("/refresh", response_model=TokenResponse)
async def refresh(response: Response, refresh_token: str | None = Cookie(default=None), db: AsyncSession = Depends(get_db)):
    if not refresh_token:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="No refresh token")
    new_access, new_refresh = await auth_service.refresh_token(db, refresh_token)
    response.set_cookie(key="refresh_token", value=new_refresh, httponly=True, secure=False, samesite="strict", max_age=7 * 24 * 3600)
    return TokenResponse(access_token=new_access)

@router.post("/logout")
async def logout(response: Response, refresh_token: str | None = Cookie(default=None), db: AsyncSession = Depends(get_db)):
    if refresh_token:
        await auth_service.logout(db, refresh_token)
    response.delete_cookie("refresh_token")
    return {"detail": "Logged out"}

@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(require_auth)):
    return current_user

@router.get("/suggest-username")
async def suggest_username(db: AsyncSession = Depends(get_db)):
    username = await generate_unique_username(db)
    return {"username": username}
