from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.core.api_response import ApiResponse
from app.schemas.category_schema import CategoryCreate, CategoryUpdate
from app.services.category_service import (
    CategoryAlreadyExistsError,
    CategoryInUseError,
    category_create,
    category_delete,
    category_get,
    category_get_all,
    category_get_products,
    category_update,
)


category_router = APIRouter(prefix="/categories", tags=["Category"])


@category_router.post("", status_code=status.HTTP_201_CREATED)
def create(category: CategoryCreate) -> ApiResponse:
    try:
        created = category_create(category)
    except CategoryAlreadyExistsError as error:
        raise HTTPException(409, "이미 등록된 카테고리 이름입니다.") from error
    return ApiResponse(success=True, message="카테고리가 등록되었습니다.", data=created)


@category_router.get("")
def get_all() -> ApiResponse:
    return ApiResponse(
        success=True,
        message="카테고리 목록을 조회했습니다.",
        data=category_get_all(),
    )


@category_router.get("/{category_id}")
def get(category_id: UUID) -> ApiResponse:
    category = category_get(category_id)
    if category is None:
        raise HTTPException(404, "카테고리를 찾을 수 없습니다.")
    return ApiResponse(success=True, message="카테고리를 조회했습니다.", data=category)


@category_router.put("/{category_id}")
def update(category_id: UUID, category: CategoryUpdate) -> ApiResponse:
    try:
        updated = category_update(category_id, category)
    except CategoryAlreadyExistsError as error:
        raise HTTPException(409, "이미 등록된 카테고리 이름입니다.") from error
    if updated is None:
        raise HTTPException(404, "카테고리를 찾을 수 없습니다.")
    return ApiResponse(success=True, message="카테고리가 수정되었습니다.", data=updated)


@category_router.delete("/{category_id}")
def delete(category_id: UUID) -> ApiResponse:
    try:
        deleted = category_delete(category_id)
    except CategoryInUseError as error:
        raise HTTPException(409, "상품이 연결된 카테고리는 삭제할 수 없습니다.") from error
    if deleted is None:
        raise HTTPException(404, "카테고리를 찾을 수 없습니다.")
    return ApiResponse(success=True, message="카테고리가 삭제되었습니다.", data=deleted)


@category_router.get("/{category_id}/products")
def get_products(category_id: UUID) -> ApiResponse:
    products = category_get_products(category_id)
    if products is None:
        raise HTTPException(404, "카테고리를 찾을 수 없습니다.")
    return ApiResponse(success=True, message="카테고리별 상품을 조회했습니다.", data=products)
