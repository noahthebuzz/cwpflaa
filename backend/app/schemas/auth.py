from pydantic import BaseModel, EmailStr, field_validator
import re

_SPECIAL = re.compile(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?`~]')


def validate_password_strength(password: str) -> str:
    errors = []
    if len(password) < 12:
        errors.append("at least 12 characters")
    if len(password) > 128:
        errors.append("at most 128 characters")
    if not re.search(r'[A-Z]', password):
        errors.append("one uppercase letter")
    if not re.search(r'[a-z]', password):
        errors.append("one lowercase letter")
    if not re.search(r'\d', password):
        errors.append("one digit")
    if not _SPECIAL.search(password):
        errors.append("one special character (!@#$%^&* …)")
    if errors:
        raise ValueError("Password must contain " + ", ".join(errors))
    return password


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    username: str | None = None

    @field_validator("password")
    @classmethod
    def strong_password(cls, v: str) -> str:
        return validate_password_strength(v)


class LoginRequest(BaseModel):
    identifier: str  # email or username
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str | None = None
