from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50, examples=["의류"])

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("카테고리 이름을 입력해 주세요.")
        return value


class CategoryUpdate(CategoryCreate):
    pass


class CategoryPublic(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime
