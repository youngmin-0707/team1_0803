# 작성자: 권오현
# 작업 구분: port

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class CustomerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    pwd: str = Field(min_length=8, max_length=100)


class CustomerUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    pwd: str | None = Field(default=None, min_length=8, max_length=100)

    @model_validator(mode="after")
    def require_update_value(self) -> "CustomerUpdate":
        if self.name is None and self.pwd is None:
            raise ValueError("수정할 회원 정보를 하나 이상 입력해야 합니다.")
        return self


class CustomerPublic(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime
