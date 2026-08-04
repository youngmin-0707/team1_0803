from datetime import datetime

from fastapi import HTTPException

from app.core.supabase_client import get_supabase
from app.schemas.review_schema import (
    ReviewCreate,
    ReviewDelete,
    ReviewList,
    ReviewPublic,
    ReviewUpdate,
)


# 동일 회원이 동일 상품에 리뷰를 작성했는지 확인
def _review_exists(product_id: str, customer_id: str) -> bool:
    supabase = get_supabase()

    result = (
        supabase.table("reviews")
        .select("id")
        .eq("product_id", product_id)
        .eq("customer_id", customer_id)
        .limit(1)
        .execute()
    )

    return bool(result.data)


# 리뷰 ID로 리뷰 한 건 조회
def _review_get(review_id: str) -> dict | None:
    supabase = get_supabase()

    result = (
        supabase.table("reviews")
        .select("*")
        .eq("id", review_id)
        .execute()
    )

    if not result.data:
        return None

    return result.data[0]


# 리뷰 작성
def review_create(review: ReviewCreate) -> ReviewPublic:
    product_id = str(review.product_id)
    customer_id = str(review.customer_id)

    if _review_exists(product_id, customer_id):
        raise HTTPException(
            status_code=409,
            detail="이미 이 상품에 리뷰를 작성했습니다.",
        )

    supabase = get_supabase()

    result = (
        supabase.table("reviews")
        .insert(
            {
                "product_id": product_id,
                "customer_id": customer_id,
                "rating": review.rating,
                "content": review.content,
            }
        )
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=500,
            detail="리뷰 등록에 실패했습니다.",
        )

    return ReviewPublic.model_validate(result.data[0])


# 상품별 리뷰 목록, 평균 별점, 리뷰 개수 조회
def review_getall(product_id: str) -> ReviewList:
    supabase = get_supabase()

    result = (
        supabase.table("reviews")
        .select("*")
        .eq("product_id", product_id)
        .order("created_at", desc=True)
        .execute()
    )

    reviews = [ReviewPublic.model_validate(item) for item in (result.data or [])]

    review_count = len(reviews)

    if review_count:
        average_rating = round(
            sum(review.rating for review in reviews) / review_count,
            1,
        )
    else:
        average_rating = 0.0

    return ReviewList(
        reviews=reviews,
        average_rating=average_rating,
        review_count=review_count,
    )


# 작성자 본인의 리뷰 수정
def review_update(
    review_id: str,
    review: ReviewUpdate,
) -> ReviewPublic:
    db_review = _review_get(review_id)

    if db_review is None:
        raise HTTPException(
            status_code=404,
            detail="리뷰를 찾을 수 없습니다.",
        )

    if str(db_review["customer_id"]) != str(review.customer_id):
        raise HTTPException(
            status_code=403,
            detail="본인이 작성한 리뷰만 수정할 수 있습니다.",
        )

    supabase = get_supabase()

    result = (
        supabase.table("reviews")
        .update(
            {
                "rating": review.rating,
                "content": review.content,
                "updated_at": datetime.now().isoformat(),
            }
        )
        .eq("id", review_id)
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=500,
            detail="리뷰 수정에 실패했습니다.",
        )

    return ReviewPublic.model_validate(result.data[0])


# 작성자 본인의 리뷰 삭제
def review_delete(
    review_id: str,
    review: ReviewDelete,
) -> ReviewPublic:
    db_review = _review_get(review_id)

    if db_review is None:
        raise HTTPException(
            status_code=404,
            detail="리뷰를 찾을 수 없습니다.",
        )
    if str(db_review["customer_id"]) != str(review.customer_id):
        raise HTTPException(
            status_code=403,
            detail="본인이 작성한 리뷰만 삭제할 수 있습니다.",
        )

    supabase = get_supabase()

    result = (
        supabase.table("reviews")
        .delete()
        .eq("id", review_id)
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=500,
            detail="리뷰 삭제에 실패했습니다.",
        )

    return ReviewPublic.model_validate(result.data[0])
