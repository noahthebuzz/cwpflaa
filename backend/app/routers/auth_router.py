import logging
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.auth.hashing import hash_password, verify_password
from app.auth.jwt import create_access_token, get_current_user
from app.schemas.user import RegisterRequest, LoginRequest, TokenResponse, UserResponse, GeneratedUsernameResponse, DeleteUserResponse
from app.auth.generator.username_generator import generate_random_username, generate_unique_username

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/generate-username", response_model=GeneratedUsernameResponse)
def generate_username(db: Session = Depends(get_db)):
    """
    Generate a unique, random username suggestion for a new user.
    
    Returns:
        A unique username that is not yet taken in the database.
    """
    username = generate_unique_username(db)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate a unique username. Please try again."
        )
    
    logger.info(f"[AUTH] new username generated: {username}")
    return GeneratedUsernameResponse(username=username)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    If username is not provided, one will be automatically generated.
    Email must be unique.
    """
    # Check if email is already registered
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    # Generate username if not provided
    username = body.username
    if not username:
        username = generate_unique_username(db)
        if not username:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate a unique username. Please try again."
            )
    
    # Check if provided username is already taken
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    
    user = User(
        username=username,
        email=body.email,
        hashed_password=hash_password(body.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    logger.info(f"[AUTH] New user: {username} - {body.email}")
    return user


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email).first()
    
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": str(user.id)})
    
    logger.info(f"[AUTH] {user.username} logged in")
    return TokenResponse(access_token=access_token)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Get the authenticated user's information.
    
    Requires: Valid JWT token in Authorization header (Bearer <token>)
    Returns: User id, username, and email
    """
    logger.info(f"[AUTH] {current_user.username} accessed /me")
    return current_user


@router.delete("/me", status_code=status.HTTP_200_OK)
async def delete_me(body: DeleteUserResponse, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Delete the authenticated user's account.
    
    Requires: Valid JWT token in Authorization header (Bearer <token>)
    Body: { "password": "current_password" }
    """
    if not verify_password(body.password, current_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    
    db.delete(current_user)
    db.commit()
    
    logger.info(f"[AUTH] {current_user.username} deleted their account")
    return {"detail": "User deleted successfully"}