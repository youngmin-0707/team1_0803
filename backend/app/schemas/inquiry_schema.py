from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class InquiryCreate(BaseModel):
    """문의 작성 시 사용자가 입력하는 값입니다."""

    product_id: UUID
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)


class InquiryUpdate(BaseModel):
    """문의 작성자가 제목과 내용을 수정할 때 사용하는 값입니다."""

    title: str = Field(min_length=1)
    content: str = Field(min_length=1)


class InquiryAnswerUpdate(BaseModel):
    """답변 권한이 있는 사용자가 답변을 등록하거나 수정할 때 사용합니다."""

    answer: str = Field(min_length=1)


class Inquiry(BaseModel):
    """DB가 자동으로 만든 값까지 포함한 문의 응답입니다."""

    id: UUID
    product_id: UUID
    customer_id: UUID
    title: str
    content: str
    answer: str | None = None
    answered_at: datetime | None = None
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
