from uuid import UUID

from fastapi import APIRouter

from app.core.api_response import ApiResponse
from app.schemas.review_schema import (
    ReviewCreate,
    ReviewDelete,
    ReviewUpdate,
)
from app.services.review_service import (
    review_create,
    review_delete,
    review_getall,
    review_update,
)

review_router = APIRouter(tags=["Review"])


@review_router.post("/review/create")
def create(review: ReviewCreate) -> ApiResponse:
    created_review = review_create(review)

    return ApiResponse(
        success=True,
        message="리뷰가 등록되었습니다.",
        data=created_review,
    )

@review_router.get("/review/product/{product_id}")
def get_all(product_id: UUID) -> ApiResponse:
    review_list = review_getall(str(product_id))

    return ApiResponse(
        success=True,
        message="리뷰 목록을 조회했습니다.",
        data=review_list,
    )

@review_router.put("/review/{review_id}")
def update(review_id: UUID, review: ReviewUpdate) -> ApiResponse:
    updated_review = review_update(str(review_id), review)

    return ApiResponse(
        success=True,
        message="리뷰가 수정되었습니다.",
        data=updated_review,
    )

@review_router.delete("/review/{review_id}")
def delete(review_id: UUID, review: ReviewDelete) -> ApiResponse:
    deleted_review = review_delete(str(review_id), review)

    return ApiResponse(
        success=True,
        message="리뷰가 삭제되었습니다.",
        data=deleted_review,
    )
