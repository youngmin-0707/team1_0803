from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Header, HTTPException, status

from app.core.api_response import ApiResponse
from app.schemas.inquiry_schema import (
    InquiryAnswerUpdate,
    InquiryCreate,
    InquiryUpdate,
)
from app.services import inquiry_service
from app.services.customer_service import customers.id as CurrentCustomerId
from app.products.product_service import products.id as CurrentProductId


inquiry_router = APIRouter(prefix="/inquiries", tags=["Inquiry"])


# 현재 프로젝트에는 백엔드 인증 토큰이 없으므로 로그인한 회원 정보를
# 임시로 헤더에서 받습니다. 토큰 인증이 추가되면 이 부분을 인증 의존성으로 교체합니다.
CurrentCustomerId = Annotated[UUID, Header(alias="X-Customer-Id")]
CurrentUserRole = Annotated[str, Header(alias="X-User-Role")]


@inquiry_router.post("", status_code=status.HTTP_201_CREATED)
def create_inquiry(
    inquiry_data: InquiryCreate,
    customer_id: CurrentCustomerId,
) -> ApiResponse:
    """로그인한 회원의 상품 문의를 작성합니다."""

    inquiry = inquiry_service.create_inquiry(customer_id, inquiry_data)
    if inquiry is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="문의 작성에 실패했습니다.",
        )

    return ApiResponse(
        success=True,
        message="문의가 작성되었습니다.",
        data=inquiry,
    )


@inquiry_router.put("/{inquiry_id}/answer")
def answer_inquiry(
    inquiry_id: UUID,
    answer_data: InquiryAnswerUpdate,
    customer_id: CurrentCustomerId,
    user_role: CurrentUserRole,
) -> ApiResponse:
    """답변 권한이 있는 사용자가 문의 답변을 등록하거나 수정합니다."""

    inquiry = inquiry_service.answer_inquiry(
        inquiry_id,
        answer_data,
        customer_id,
        user_role,
    )
    if inquiry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="문의를 찾을 수 없습니다.",
        )

    return ApiResponse(
        success=True,
        message="문의 답변이 저장되었습니다.",
        data=inquiry,
    )


@inquiry_router.put("/{inquiry_id}")
def update_inquiry(
    inquiry_id: UUID,
    inquiry_data: InquiryUpdate,
    customer_id: CurrentCustomerId,
) -> ApiResponse:
    """로그인한 회원이 자신이 작성한 문의를 수정합니다."""

    inquiry = inquiry_service.update_inquiry(
        inquiry_id,
        customer_id,
        inquiry_data,
    )
    if inquiry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="문의를 찾을 수 없습니다.",
        )

    return ApiResponse(
        success=True,
        message="문의가 수정되었습니다.",
        data=inquiry,
    )