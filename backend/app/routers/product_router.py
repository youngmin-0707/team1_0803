# 작성자: 권오현
# 작업 구분: port

from uuid import UUID

from fastapi import APIRouter

from app.core.api_response import ApiResponse
from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.services.product_service import (
    create_product,
    delete_product,
    get_product,
    get_products,
    update_product,
)


product_router = APIRouter(prefix="/products", tags=["Product"])


@product_router.post("")
def create(payload: ProductCreate) -> ApiResponse:
    return ApiResponse(
        success=True,
        message="상품을 등록했습니다.",
        data=create_product(payload),
    )


@product_router.get("")
def read_all() -> ApiResponse:
    return ApiResponse(
        success=True,
        message="상품 목록을 조회했습니다.",
        data=get_products(),
    )


@product_router.get("/{product_id}")
def read(product_id: UUID) -> ApiResponse:
    return ApiResponse(
        success=True,
        message="상품을 조회했습니다.",
        data=get_product(product_id),
    )


@product_router.patch("/{product_id}")
def update(product_id: UUID, payload: ProductUpdate) -> ApiResponse:
    return ApiResponse(
        success=True,
        message="상품 정보를 수정했습니다.",
        data=update_product(product_id, payload),
    )


@product_router.delete("/{product_id}")
def delete(product_id: UUID) -> ApiResponse:
    return ApiResponse(
        success=True,
        message="상품을 삭제했습니다.",
        data=delete_product(product_id),
    )
