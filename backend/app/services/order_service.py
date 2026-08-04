# order_service.py

from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import HTTPException

from app.core.supabase_client import get_supabase
from app.schemas.order_schema import (
    OrderCreate,
    OrderDetailPublic,
    OrderItemPublic,
    OrderPublic,
)


def _generate_id(seq: int = 0) -> str:
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    return f"{now.strftime('%Y%m%d%H%M%S%f')}{seq:02d}"


def _get_product(supabase, product_id: str) -> dict | None:
    result = (
        supabase.table("products")
        .select("*")
        .eq("id", product_id)
        .execute()
    )
    if not result.data:
        return None
    return result.data[0]


# 1. 주문 생성 (상품 목록 -> 주문 + 주문 상품 저장)
def order_create(order: OrderCreate) -> OrderDetailPublic:
    supabase = get_supabase()
    now = datetime.now(ZoneInfo("Asia/Seoul"))

    products_by_id: dict[str, dict] = {}
    for item in order.items:
        product = _get_product(supabase, item.product_id)
        if product is None:
            raise HTTPException(
                status_code=404,
                detail=f"상품 ID {item.product_id}를 찾을 수 없습니다.",
            )
        products_by_id[item.product_id] = product

    order_id = _generate_id()
    order_result = (
        supabase.table("orders")
        .insert(
            {
                "id": order_id,
                "customer_id": order.customer_id,
                "status": "pending",
                "shipping_address": order.shipping_address,
                "created_at": now.isoformat(),
                "updated_at": now.isoformat(),
            }
        )
        .execute()
    )
    if not order_result.data:
        raise HTTPException(status_code=500, detail="주문 생성에 실패했습니다.")

    order_items: list[OrderItemPublic] = []
    for seq, item in enumerate(order.items, start=1):
        product = products_by_id[item.product_id]
        item_result = (
            supabase.table("order_items")
            .insert(
                {
                    "id": _generate_id(seq),
                    "order_id": order_id,
                    "product_id": item.product_id,
                    "product_name": product["name"],
                    "quantity": item.quantity,
                    "price": product["price"],
                    "created_at": now.isoformat(),
                }
            )
            .execute()
        )
        if not item_result.data:
            raise HTTPException(status_code=500, detail="주문 상품 저장에 실패했습니다.")
        order_items.append(OrderItemPublic.model_validate(item_result.data[0]))

    order_data = order_result.data[0]
    total_amount = sum(oi.price * oi.quantity for oi in order_items)
    return OrderDetailPublic.model_validate(
        {**order_data, "items": order_items, "total_amount": total_amount}
    )


# 2. 회원 주문 목록 조회
def order_get_all(customer_id: str) -> list[OrderPublic]:
    supabase = get_supabase()
    result = (
        supabase.table("orders")
        .select("*")
        .eq("customer_id", customer_id)
        .is_("deleted_at", "null")
        .order("created_at", desc=True)
        .execute()
    )
    return [OrderPublic.model_validate(item) for item in result.data]


# 3. 주문 상세 조회 (주문 상품 포함)
def order_get(order_id: str) -> OrderDetailPublic | None:
    supabase = get_supabase()

    order_result = (
        supabase.table("orders")
        .select("*")
        .eq("id", order_id)
        .is_("deleted_at", "null")
        .execute()
    )
    if not order_result.data:
        return None

    items_result = (
        supabase.table("order_items")
        .select("*")
        .eq("order_id", order_id)
        .execute()
    )
    items = [OrderItemPublic.model_validate(item) for item in items_result.data]
    total_amount = sum(item.price * item.quantity for item in items)

    order_data = order_result.data[0]
    return OrderDetailPublic.model_validate(
        {**order_data, "items": items, "total_amount": total_amount}
    )
