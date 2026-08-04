# 작성자: 권오현
# 작업 구분: port

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from fastapi import HTTPException

from app.core.supabase_client import get_supabase
from app.schemas.product_schema import (
    ProductCreate,
    ProductPublic,
    ProductUpdate,
)


def _execute(query: Any, message: str) -> list[dict[str, Any]]:
    try:
        result = query.execute()
    except Exception as error:
        raise HTTPException(status_code=500, detail=message) from error
    return result.data or []


def create_product(payload: ProductCreate) -> ProductPublic:
    values = payload.model_dump(mode="json")
    values["name"] = payload.name.strip()
    rows = _execute(
        get_supabase().table("products").insert(values),
        "상품을 등록하는 중 오류가 발생했습니다.",
    )
    if not rows:
        raise HTTPException(status_code=500, detail="상품 등록 결과가 없습니다.")
    return ProductPublic.model_validate(rows[0])


def get_products() -> list[ProductPublic]:
    rows = _execute(
        get_supabase().table("products")
        .select("id,name,price,stock,category_id,created_at,updated_at")
        .order("created_at"),
        "상품 목록을 조회하는 중 오류가 발생했습니다.",
    )
    return [ProductPublic.model_validate(row) for row in rows]


def get_product(product_id: UUID) -> ProductPublic:
    rows = _execute(
        get_supabase().table("products")
        .select("id,name,price,stock,category_id,created_at,updated_at")
        .eq("id", str(product_id))
        .limit(1),
        "상품을 조회하는 중 오류가 발생했습니다.",
    )
    if not rows:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")
    return ProductPublic.model_validate(rows[0])


def update_product(
    product_id: UUID,
    payload: ProductUpdate,
) -> ProductPublic:
    get_product(product_id)
    values = payload.model_dump(mode="json", exclude_unset=True)
    if "name" in values and values["name"] is not None:
        values["name"] = values["name"].strip()
    values["updated_at"] = datetime.now(timezone.utc).isoformat()

    rows = _execute(
        get_supabase().table("products")
        .update(values)
        .eq("id", str(product_id)),
        "상품 정보를 수정하는 중 오류가 발생했습니다.",
    )
    if not rows:
        raise HTTPException(status_code=500, detail="상품 수정 결과가 없습니다.")
    return ProductPublic.model_validate(rows[0])


def delete_product(product_id: UUID) -> ProductPublic:
    get_product(product_id)
    rows = _execute(
        get_supabase().table("products")
        .delete()
        .eq("id", str(product_id)),
        "상품을 삭제하는 중 오류가 발생했습니다. 연결된 데이터를 확인해 주세요.",
    )
    if not rows:
        raise HTTPException(status_code=500, detail="상품 삭제 결과가 없습니다.")
    return ProductPublic.model_validate(rows[0])
