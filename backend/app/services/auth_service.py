import hashlib
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_token
from app.core.config import settings
from app.services.username_service import generate_unique_username

async def register(db: AsyncSession, email: str, password: str, username: str | None = None) -> User:
    result = await db.execute(select(User).where(User.email == email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered", headers={"code": "EMAIL_EXISTS"})

    if not username:
        username = await generate_unique_username(db)
    else:
        result2 = await db.execute(select(User).where(User.username == username))
        if result2.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Username already taken", headers={"code": "USERNAME_EXISTS"})

    user = User(email=email, username=username, hashed_password=get_password_hash(password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def login(db: AsyncSession, identifier: str, password: str) -> tuple[User, str, str]:
    from sqlalchemy import or_
    result = await db.execute(
        select(User).where(or_(User.email == identifier, User.username == identifier))
    )
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials", headers={"code": "INVALID_CREDENTIALS"})
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account disabled", headers={"code": "ACCOUNT_DISABLED"})

    access_token = create_access_token(str(user.id))
    refresh_token_str = create_refresh_token(str(user.id))

    token_hash = hashlib.sha256(refresh_token_str.encode()).hexdigest()
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    rt = RefreshToken(user_id=user.id, token_hash=token_hash, expires_at=expires_at)
    db.add(rt)
    await db.commit()

    return user, access_token, refresh_token_str

async def refresh_token(db: AsyncSession, token: str) -> tuple[str, str]:
    try:
        payload = decode_token(token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    token_hash = hashlib.sha256(token.encode()).hexdigest()
    result = await db.execute(
        select(RefreshToken).where(
            RefreshToken.token_hash == token_hash,
            RefreshToken.revoked == False,
            RefreshToken.expires_at > datetime.now(timezone.utc)
        )
    )
    rt = result.scalar_one_or_none()
    if not rt:
        raise HTTPException(status_code=401, detail="Refresh token invalid or expired")

    rt.revoked = True
    new_access = create_access_token(user_id)
    new_refresh = create_refresh_token(user_id)
    new_hash = hashlib.sha256(new_refresh.encode()).hexdigest()
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    new_rt = RefreshToken(user_id=rt.user_id, token_hash=new_hash, expires_at=expires_at)
    db.add(new_rt)
    await db.commit()
    return new_access, new_refresh

async def logout(db: AsyncSession, token: str) -> None:
    try:
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        result = await db.execute(select(RefreshToken).where(RefreshToken.token_hash == token_hash))
        rt = result.scalar_one_or_none()
        if rt:
            rt.revoked = True
            await db.commit()
    except Exception:
        pass
