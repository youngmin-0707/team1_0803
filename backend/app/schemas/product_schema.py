# 작성자: 권오현
# 작업 구분: port

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: int = Field(ge=0)
    stock: int = Field(ge=0)
    category_id: UUID | None = None


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    price: int | None = Field(default=None, ge=0)
    stock: int | None = Field(default=None, ge=0)
    category_id: UUID | None = None

    @model_validator(mode="after")
    def require_update_value(self) -> "ProductUpdate":
        if not self.model_fields_set:
            raise ValueError("수정할 상품 정보를 하나 이상 입력해야 합니다.")
        return self


class ProductPublic(BaseModel):
    id: UUID
    name: str
    price: int
    stock: int
    category_id: UUID | None = None
    created_at: datetime
    updated_at: datetime
