from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    product_id: UUID
    customer_id: UUID
    rating: int = Field(ge=1, le=5)
    content: str | None = None


class ReviewUpdate(BaseModel):
    customer_id: UUID
    rating: int = Field(ge=1, le=5)
    content: str | None = None


class ReviewDelete(BaseModel):
    customer_id: UUID


class ReviewPublic(BaseModel):
    id: UUID
    product_id: UUID
    customer_id: UUID
    rating: int
    content: str | None
    created_at: datetime
    updated_at: datetime


class ReviewList(BaseModel):
    reviews: list[ReviewPublic]
    average_rating: float
    review_count: int
