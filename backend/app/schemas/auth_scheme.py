# auth_scheme.py

from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class AuthCreate(BaseModel):
    id: UUID
    name: str
    pwd: str

class AuthUpdate(BaseModel):
    id: UUID
    name: str
    pwd: str

class AuthLogin(BaseModel):
    id: UUID
    pwd: str

class AuthPublic(BaseModel):
    id: UUID
    name: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

class PasswordUpdate(BaseModel):
    current_pwd: str = Field(min_length=1)
    new_pwd: str = Field(min_length=1)
