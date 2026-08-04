from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header

from app.core.api_response import ApiResponse
from app.schemas.cart_schema import (
    CartCreate,
    CartQuantityUpdate,
    CartSelectedRequest,
)
from app.services.cart_service import (
    add_cart_item,
    clear_cart,
    delete_cart_item,
    delete_selected_cart_items,
    get_cart,
    prepare_order_selection,
    update_cart_quantity,
)


cart_router = APIRouter(prefix="/cart", tags=["Cart"])


def get_test_customer_id(
    customer_id: Annotated[UUID, Header(alias="X-Customer-Id")],
) -> UUID:
    """독립 테스트 요청에서 회원 UUID를 읽습니다.

    TODO:
    팀 인증 방식이 확정되면 이 테스트 헤더를 로그인 세션 또는
    인증 토큰에서 얻은 회원 UUID로 교체합니다.
    """
    return customer_id


CurrentCustomerId = Annotated[UUID, Depends(get_test_customer_id)]


@cart_router.post("/items")
def create_cart_item(
    payload: CartCreate,
    customer_id: CurrentCustomerId,
) -> ApiResponse:
    item = add_cart_item(customer_id, payload)
    return ApiResponse(
        success=True,
        message="장바구니에 상품을 추가했습니다.",
        data=item,
    )


@cart_router.get("")
def read_cart(
    customer_id: CurrentCustomerId,
) -> ApiResponse:
    summary = get_cart(customer_id)
    return ApiResponse(
        success=True,
        message="장바구니를 조회했습니다.",
        data=summary,
    )


@cart_router.patch("/items/{cart_id}")
def change_cart_quantity(
    cart_id: UUID,
    payload: CartQuantityUpdate,
    customer_id: CurrentCustomerId,
) -> ApiResponse:
    item = update_cart_quantity(
        customer_id,
        cart_id,
        payload,
    )
    return ApiResponse(
        success=True,
        message="장바구니 수량을 변경했습니다.",
        data=item,
    )


@cart_router.delete("/items/{cart_id}")
def remove_cart_item(
    cart_id: UUID,
    customer_id: CurrentCustomerId,
) -> ApiResponse:
    item = delete_cart_item(customer_id, cart_id)
    return ApiResponse(
        success=True,
        message="장바구니 상품을 삭제했습니다.",
        data=item,
    )


@cart_router.post("/items/delete-selected")
def remove_selected_cart_items(
    payload: CartSelectedRequest,
    customer_id: CurrentCustomerId,
) -> ApiResponse:
    items = delete_selected_cart_items(
        customer_id,
        payload.cart_ids,
    )
    return ApiResponse(
        success=True,
        message="선택한 장바구니 상품을 삭제했습니다.",
        data=items,
    )


@cart_router.delete("")
def remove_all_cart_items(
    customer_id: CurrentCustomerId,
) -> ApiResponse:
    items = clear_cart(customer_id)
    return ApiResponse(
        success=True,
        message="장바구니를 비웠습니다.",
        data=items,
    )


@cart_router.post("/order-selection")
def create_order_selection(
    payload: CartSelectedRequest,
    customer_id: CurrentCustomerId,
) -> ApiResponse:
    selection = prepare_order_selection(
        customer_id,
        payload.cart_ids,
    )
    return ApiResponse(
        success=True,
        message="주문으로 전달할 장바구니 정보를 준비했습니다.",
        data=selection,
    )
