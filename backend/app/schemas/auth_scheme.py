# auth_scheme.py

from pydantic import BaseModel, Field

class AuthCreate(BaseModel):
    id: str
    name: str
    pwd: str

class AuthUpdate(BaseModel):
    id: str
    name: str
    pwd: str

class AuthLogin(BaseModel):
    id: str
    pwd: str

class AuthPublic(BaseModel):
    id: str
    name: str | None = None

class PasswordUpdate(BaseModel):
    current_pwd: str = Field(min_length=1)
    new_pwd: str = Field(min_length=1)