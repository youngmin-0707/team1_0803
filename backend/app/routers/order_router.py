# order_router.py

from fastapi import APIRouter, HTTPException

from app.core.api_response import ApiResponse
from app.schemas.order_schema import OrderCreate, OrderStatusUpdate
from app.services.order_service import (
    order_cancel,
    order_create,
    order_delete,
    order_get,
    order_get_all,
    order_update_status,
)

order_router = APIRouter(tags=["Order"])

# 200: 정상
# 400: 잘못된 요청
# 404: 데이터 없음
# 500: 서버 또는 DB 처리 실패


# 1. 주문 생성
@order_router.post("/order/create")
def create(order: OrderCreate) -> ApiResponse:
    created_order = order_create(order)
    response = ApiResponse(
        success=True,
        message="주문이 생성되었습니다.",
        data=created_order,
    )
    return response


# 2. 회원 주문 목록 조회
@order_router.get("/order/list/{customer_id}")
def get_all(customer_id: str) -> ApiResponse:
    orders = order_get_all(customer_id)
    response = ApiResponse(
        success=True,
        message="주문 목록 조회에 성공했습니다.",
        data=orders,
    )
    return response


# 3. 주문 상세 조회
@order_router.get("/order/get/{order_id}")
def get(order_id: str) -> ApiResponse:
    order = order_get(order_id)
    if order is None:
        raise HTTPException(
            status_code=404,
            detail=f"주문 ID {order_id}를 찾을 수 없습니다.",
        )
    response = ApiResponse(
        success=True,
        message="주문 조회에 성공했습니다.",
        data=order,
    )
    return response


# 4. 주문 상태 변경
@order_router.patch("/order/{order_id}/status")
def update_status(order_id: str, status_update: OrderStatusUpdate) -> ApiResponse:
    order = order_update_status(order_id, status_update.status)
    response = ApiResponse(
        success=True,
        message="주문 상태가 변경되었습니다.",
        data=order,
    )
    return response


# 5. 주문 취소
@order_router.post("/order/{order_id}/cancel")
def cancel(order_id: str) -> ApiResponse:
    order = order_cancel(order_id)
    response = ApiResponse(
        success=True,
        message="주문이 취소되었습니다.",
        data=order,
    )
    return response


# 6. 주문 삭제 (소프트 삭제)
@order_router.delete("/order/{order_id}")
def delete(order_id: str) -> ApiResponse:
    order = order_delete(order_id)
    response = ApiResponse(
        success=True,
        message="주문이 삭제되었습니다.",
        data=order,
    )
    return response
