from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.core.security import decode_token
from app.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db)
) -> User | None:
    if not credentials:
        return None
    try:
        payload = decode_token(credentials.credentials)
        if payload.get("type") != "access":
            return None
        user_id = payload.get("sub")
    except Exception:
        return None

    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def get_current_active_user(user: User | None = Depends(get_current_user)) -> User | None:
    if user and not user.is_active:
        return None
    return user

async def require_auth(user: User | None = Depends(get_current_user)) -> User:
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated", headers={"WWW-Authenticate": "Bearer"})
    return user

async def require_superadmin(user: User = Depends(require_auth)) -> User:
    if not user.is_superadmin:
        raise HTTPException(status_code=403, detail="Superadmin required")
    return user
