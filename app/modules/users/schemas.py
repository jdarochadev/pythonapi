from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional
import re

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]{3,50}$', v):
            raise ValueError('Username must be 3-50 characters and contain only letters, numbers, and underscores')
        return v

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str
