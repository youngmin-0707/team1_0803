from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from fastapi import HTTPException

from app.core.supabase_client import get_supabase
from app.schemas.cart_schema import (
    CartCreate,
    CartItemPublic,
    CartOrderItem,
    CartOrderSelection,
    CartQuantityUpdate,
    CartSummary,
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _execute(query: Any, failure_message: str) -> list[dict[str, Any]]:
    try:
        result = query.execute()
    except Exception as error:
        raise HTTPException(status_code=500, detail=failure_message) from error

    return result.data or []


def _get_customer(customer_id: UUID) -> dict[str, Any]:
    supabase = get_supabase()
    rows = _execute(
        supabase.table("customers")
        .select("id")
        .eq("id", str(customer_id))
        .limit(1),
        "회원 정보를 확인하는 중 오류가 발생했습니다.",
    )
    if not rows:
        raise HTTPException(status_code=404, detail="회원을 찾을 수 없습니다.")
    return rows[0]


def _get_product(product_id: UUID) -> dict[str, Any] | None:
    supabase = get_supabase()
    rows = _execute(
        supabase.table("products")
        .select("id,name,price,stock")
        .eq("id", str(product_id))
        .limit(1),
        "상품 정보를 확인하는 중 오류가 발생했습니다.",
    )
    return rows[0] if rows else None


def _require_product(product_id: UUID) -> dict[str, Any]:
    product = _get_product(product_id)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="삭제되었거나 존재하지 않는 상품입니다.",
        )
    return product


def _get_owned_cart_item(
    cart_id: UUID,
    customer_id: UUID,
) -> dict[str, Any]:
    supabase = get_supabase()
    rows = _execute(
        supabase.table("carts")
        .select("*")
        .eq("id", str(cart_id))
        .limit(1),
        "장바구니 항목을 확인하는 중 오류가 발생했습니다.",
    )
    if not rows:
        raise HTTPException(
            status_code=404,
            detail="장바구니 항목을 찾을 수 없습니다.",
        )

    cart_item = rows[0]
    if str(cart_item["customer_id"]) != str(customer_id):
        raise HTTPException(
            status_code=403,
            detail="다른 회원의 장바구니 항목에는 접근할 수 없습니다.",
        )
    return cart_item


def _validate_stock(product: dict[str, Any], quantity: int) -> None:
    stock = int(product.get("stock") or 0)
    if stock == 0:
        raise HTTPException(status_code=409, detail="품절된 상품입니다.")
    if quantity > stock:
        raise HTTPException(
            status_code=409,
            detail=f"상품 재고는 최대 {stock}개입니다.",
        )

    # TODO:
    # products에 판매 상태 컬럼이 추가되면 판매 중지 상품의
    # 장바구니 추가, 수량 변경 및 주문 전달을 이곳에서 차단합니다.


def _to_public_item(
    cart_item: dict[str, Any],
    product: dict[str, Any] | None,
) -> CartItemPublic:
    quantity = int(cart_item["quantity"])
    base_item = {
        "id": cart_item["id"],
        "customer_id": cart_item["customer_id"],
        "product_id": cart_item["product_id"],
        "quantity": quantity,
        "created_at": cart_item["created_at"],
        "updated_at": cart_item["updated_at"],
    }

    if product is None:
        return CartItemPublic(
            **base_item,
            product_name=None,
            price=None,
            stock=None,
            subtotal=0,
            available=False,
            availability_message="삭제되었거나 존재하지 않는 상품입니다.",
        )

    price = int(product["price"])
    stock = int(product.get("stock") or 0)
    available = stock > 0 and quantity <= stock

    if stock == 0:
        message = "품절된 상품입니다."
    elif quantity > stock:
        message = f"현재 재고는 {stock}개입니다."
    else:
        message = None

    return CartItemPublic(
        **base_item,
        product_name=product["name"],
        price=price,
        stock=stock,
        subtotal=price * quantity,
        available=available,
        availability_message=message,
    )


def add_cart_item(
    customer_id: UUID,
    payload: CartCreate,
) -> CartItemPublic:
    _get_customer(customer_id)
    product = _require_product(payload.product_id)

    supabase = get_supabase()
    existing_rows = _execute(
        supabase.table("carts")
        .select("*")
        .eq("customer_id", str(customer_id))
        .eq("product_id", str(payload.product_id))
        .limit(1),
        "장바구니 중복 상품을 확인하는 중 오류가 발생했습니다.",
    )

    if existing_rows:
        existing_item = existing_rows[0]
        new_quantity = int(existing_item["quantity"]) + payload.quantity
        _validate_stock(product, new_quantity)
        saved_rows = _execute(
            supabase.table("carts")
            .update(
                {
                    "quantity": new_quantity,
                    "updated_at": _now_iso(),
                }
            )
            .eq("id", str(existing_item["id"])),
            "장바구니 수량을 증가시키는 중 오류가 발생했습니다.",
        )
    else:
        _validate_stock(product, payload.quantity)
        saved_rows = _execute(
            supabase.table("carts").insert(
                {
                    "customer_id": str(customer_id),
                    "product_id": str(payload.product_id),
                    "quantity": payload.quantity,
                }
            ),
            "장바구니에 상품을 추가하는 중 오류가 발생했습니다.",
        )

    if not saved_rows:
        raise HTTPException(
            status_code=500,
            detail="장바구니 저장 결과를 확인할 수 없습니다.",
        )
    return _to_public_item(saved_rows[0], product)


def get_cart(customer_id: UUID) -> CartSummary:
    _get_customer(customer_id)
    supabase = get_supabase()
    cart_rows = _execute(
        supabase.table("carts")
        .select("*")
        .eq("customer_id", str(customer_id))
        .order("created_at"),
        "장바구니를 조회하는 중 오류가 발생했습니다.",
    )

    if not cart_rows:
        return CartSummary(items=[], total_quantity=0, total_price=0)

    product_ids = list({str(row["product_id"]) for row in cart_rows})
    product_rows = _execute(
        supabase.table("products")
        .select("id,name,price,stock")
        .in_("id", product_ids),
        "장바구니 상품을 조회하는 중 오류가 발생했습니다.",
    )
    products = {str(product["id"]): product for product in product_rows}

    items = [
        _to_public_item(row, products.get(str(row["product_id"])))
        for row in cart_rows
    ]
    return CartSummary(
        items=items,
        total_quantity=sum(item.quantity for item in items),
        total_price=sum(item.subtotal for item in items),
    )


def update_cart_quantity(
    customer_id: UUID,
    cart_id: UUID,
    payload: CartQuantityUpdate,
) -> CartItemPublic:
    cart_item = _get_owned_cart_item(cart_id, customer_id)
    product = _require_product(UUID(str(cart_item["product_id"])))
    _validate_stock(product, payload.quantity)

    supabase = get_supabase()
    updated_rows = _execute(
        supabase.table("carts")
        .update(
            {
                "quantity": payload.quantity,
                "updated_at": _now_iso(),
            }
        )
        .eq("id", str(cart_id))
        .eq("customer_id", str(customer_id)),
        "장바구니 수량을 변경하는 중 오류가 발생했습니다.",
    )
    if not updated_rows:
        raise HTTPException(
            status_code=500,
            detail="수량 변경 결과를 확인할 수 없습니다.",
        )
    return _to_public_item(updated_rows[0], product)


def delete_cart_item(customer_id: UUID, cart_id: UUID) -> dict[str, Any]:
    _get_owned_cart_item(cart_id, customer_id)
    supabase = get_supabase()
    deleted_rows = _execute(
        supabase.table("carts")
        .delete()
        .eq("id", str(cart_id))
        .eq("customer_id", str(customer_id)),
        "장바구니 항목을 삭제하는 중 오류가 발생했습니다.",
    )
    if not deleted_rows:
        raise HTTPException(
            status_code=500,
            detail="삭제 결과를 확인할 수 없습니다.",
        )
    return deleted_rows[0]


def _validate_selected_items(
    customer_id: UUID,
    cart_ids: list[UUID],
) -> list[dict[str, Any]]:
    supabase = get_supabase()
    requested_ids = [str(cart_id) for cart_id in cart_ids]
    rows = _execute(
        supabase.table("carts")
        .select("*")
        .in_("id", requested_ids),
        "선택한 장바구니 항목을 확인하는 중 오류가 발생했습니다.",
    )

    found_ids = {str(row["id"]) for row in rows}
    if found_ids != set(requested_ids):
        raise HTTPException(
            status_code=404,
            detail="선택한 장바구니 항목 중 존재하지 않는 항목이 있습니다.",
        )
    if any(str(row["customer_id"]) != str(customer_id) for row in rows):
        raise HTTPException(
            status_code=403,
            detail="다른 회원의 장바구니 항목이 포함되어 있습니다.",
        )
    return rows


def delete_selected_cart_items(
    customer_id: UUID,
    cart_ids: list[UUID],
) -> list[dict[str, Any]]:
    _validate_selected_items(customer_id, cart_ids)
    supabase = get_supabase()
    return _execute(
        supabase.table("carts")
        .delete()
        .in_("id", [str(cart_id) for cart_id in cart_ids])
        .eq("customer_id", str(customer_id)),
        "선택한 장바구니 항목을 삭제하는 중 오류가 발생했습니다.",
    )


def clear_cart(customer_id: UUID) -> list[dict[str, Any]]:
    _get_customer(customer_id)
    supabase = get_supabase()
    return _execute(
        supabase.table("carts")
        .delete()
        .eq("customer_id", str(customer_id)),
        "장바구니 전체를 삭제하는 중 오류가 발생했습니다.",
    )


def prepare_order_selection(
    customer_id: UUID,
    cart_ids: list[UUID],
) -> CartOrderSelection:
    cart_rows = _validate_selected_items(customer_id, cart_ids)
    order_items: list[CartOrderItem] = []

    for cart_item in cart_rows:
        product_id = UUID(str(cart_item["product_id"]))
        product = _require_product(product_id)
        quantity = int(cart_item["quantity"])
        _validate_stock(product, quantity)
        price = int(product["price"])

        order_items.append(
            CartOrderItem(
                cart_id=cart_item["id"],
                product_id=product_id,
                product_name=product["name"],
                quantity=quantity,
                price=price,
                subtotal=price * quantity,
            )
        )

    # TODO:
    # 주문 담당자의 API 명세가 확정되면 이 데이터를 주문 API에 전달하고,
    # 주문 성공 후 선택한 장바구니 항목을 삭제하도록 연결합니다.
    return CartOrderSelection(
        customer_id=customer_id,
        items=order_items,
        total_price=sum(item.subtotal for item in order_items),
    )
