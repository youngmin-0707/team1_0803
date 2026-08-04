# product_service.py
from app.schemas.product_schema import (
    ProductCreate, 
    ProductPublic, 
    ProductUpdate,
)
from app.core.supabase_client import get_supabase
from zoneinfo import ZoneInfo
from datetime import datetime
from uuid import UUID, uuid4

# 1. 입력
def product_create(product: ProductCreate) -> ProductPublic | None:
    supabase = get_supabase()
    now = datetime.now(ZoneInfo("Asia/Seoul"))

    result = (
        supabase.table("products")
         .insert(
            {
                "id": str(uuid4()),
                "name": product.name,
                "price": product.price,
                "stock": product.stock,
                "category_id": str(product.category_id) if product.category_id else None,
                "created_at": now.isoformat(),   # timestamptz
                "updated_at": now.isoformat(),
            }
        )
        .execute()
    )
    if not result.data:
        return None
    return ProductPublic.model_validate(result.data[0])

# 2. 전체조회
def product_get_all() -> list[ProductPublic]:
    supabase = get_supabase()
    result = (
        supabase.table("products")
        .select("*")
        .execute()
    )
    return [ProductPublic.model_validate(item) for item in result.data]

# 3. 한개조회
def product_get(product_id: UUID) -> ProductPublic | None:
    supabase = get_supabase()

    result = (
        supabase.table("products")
        .select("*")
        .eq("id", str(product_id))
        .execute()
    )
    if not result.data:
        return None
    return ProductPublic.model_validate(result.data[0])


# 4. 삭제
def product_delete(product_id: UUID) -> ProductPublic | None:
    supabase = get_supabase()
    result = (
        supabase.table("products")
        .delete()
        .eq("id", str(product_id))
        .execute()
    )
    if not result.data:
        return None
    return ProductPublic.model_validate(result.data[0])


# 5. 수정
def product_update(
    product_id: UUID,
    product: ProductUpdate,
) -> ProductPublic | None:
    supabase = get_supabase()

    result = (
        supabase.table("products")
        .update(
                {
                    "name": product.name,
                    "price": product.price,
                    "stock": product.stock,
                    "category_id": str(product.category_id) if product.category_id else None,
                    "updated_at": datetime.now(ZoneInfo("Asia/Seoul")).isoformat(),
                }
            )
            .eq("id", str(product_id))
            .execute()
    )
    if not result.data:
        return None
    return ProductPublic.model_validate(result.data[0])
