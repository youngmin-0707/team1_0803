# 작성자: 권오현
# 작업 구분: port

from uuid import UUID

from fastapi import APIRouter

from app.core.api_response import ApiResponse
from app.schemas.customer_schema import CustomerCreate, CustomerUpdate
from app.services.customer_service import (
    create_customer,
    delete_customer,
    get_customer,
    get_customers,
    update_customer,
)


customer_router = APIRouter(prefix="/customers", tags=["Customer"])


@customer_router.post("")
def create(payload: CustomerCreate) -> ApiResponse:
    return ApiResponse(
        success=True,
        message="회원을 등록했습니다.",
        data=create_customer(payload),
    )


@customer_router.get("")
def read_all() -> ApiResponse:
    return ApiResponse(
        success=True,
        message="회원 목록을 조회했습니다.",
        data=get_customers(),
    )


@customer_router.get("/{customer_id}")
def read(customer_id: UUID) -> ApiResponse:
    return ApiResponse(
        success=True,
        message="회원을 조회했습니다.",
        data=get_customer(customer_id),
    )


@customer_router.patch("/{customer_id}")
def update(customer_id: UUID, payload: CustomerUpdate) -> ApiResponse:
    return ApiResponse(
        success=True,
        message="회원 정보를 수정했습니다.",
        data=update_customer(customer_id, payload),
    )


@customer_router.delete("/{customer_id}")
def delete(customer_id: UUID) -> ApiResponse:
    return ApiResponse(
        success=True,
        message="회원을 삭제했습니다.",
        data=delete_customer(customer_id),
    )
