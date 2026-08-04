from typing import Any

from pydantic import BaseModel


class ApiResponse(BaseModel):
    """표준 응답 모델입니다."""

    success: bool
    message: str
    data: Any | None = None
