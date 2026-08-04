from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50, examples=["바지"])
    price: int = Field(ge=1, examples=[10000])
    stock: int = Field(ge=0, examples=[100])
    category_id: UUID | None = None


class ProductUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=50, examples=["청바지"])
    price: int = Field(ge=1, examples=[20000])
    stock: int = Field(ge=0, examples=[50])
    category_id: UUID | None = None


class ProductPublic(BaseModel):
    id: UUID
    name: str
    price: int
    stock: int
    category_id: UUID | None = None
    created_at: datetime
    updated_at: datetime
