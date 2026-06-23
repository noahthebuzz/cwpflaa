from pydantic import BaseModel, EmailStr
import uuid
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str | None = None

class UserRead(BaseModel):
    id: uuid.UUID
    email: str
    username: str
    is_active: bool
    is_verified: bool
    is_superadmin: bool
    created_at: datetime

    model_config = {"from_attributes": True}

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
