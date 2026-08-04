# 작성자: 권오현
# 작업 구분: port

import os
from typing import Any
from uuid import UUID

import httpx

from core.api_client import BackendAPIError


REQUEST_TIMEOUT = 15.0


def _backend_url() -> str:
    return os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")


def _request(
    method: str,
    path: str,
    customer_id: UUID | str,
    json: dict[str, Any] | None = None,
) -> Any:
    try:
        response = httpx.request(
            method,
            f"{_backend_url()}{path}",
            headers={"X-Customer-Id": str(customer_id)},
            json=json,
            timeout=REQUEST_TIMEOUT,
        )
    except httpx.TimeoutException as error:
        raise BackendAPIError("백엔드 응답 시간이 초과되었습니다.") from error
    except httpx.RequestError as error:
        raise BackendAPIError(
            "장바구니 백엔드 서버에 연결할 수 없습니다."
        ) from error

    try:
        payload = response.json()
    except ValueError as error:
        raise BackendAPIError(
            "백엔드가 올바른 JSON을 반환하지 않았습니다."
        ) from error

    if not response.is_success:
        detail = payload.get("detail") if isinstance(payload, dict) else None
        if isinstance(detail, list):
            detail = "입력값을 확인해 주세요."
        raise BackendAPIError(detail or "장바구니 요청 처리에 실패했습니다.")

    if not isinstance(payload, dict) or "data" not in payload:
        raise BackendAPIError("장바구니 API 응답 형식이 올바르지 않습니다.")
    return payload["data"]


def add_cart_item(
    customer_id: UUID | str,
    product_id: UUID | str,
    quantity: int,
) -> dict[str, Any]:
    return _request(
        "POST",
        "/cart/items",
        customer_id,
        json={"product_id": str(product_id), "quantity": quantity},
    )


def get_cart(customer_id: UUID | str) -> dict[str, Any]:
    return _request("GET", "/cart", customer_id)


def update_cart_quantity(
    customer_id: UUID | str,
    cart_id: UUID | str,
    quantity: int,
) -> dict[str, Any]:
    return _request(
        "PATCH",
        f"/cart/items/{cart_id}",
        customer_id,
        json={"quantity": quantity},
    )


def delete_cart_item(
    customer_id: UUID | str,
    cart_id: UUID | str,
) -> dict[str, Any]:
    return _request("DELETE", f"/cart/items/{cart_id}", customer_id)


def delete_selected_cart_items(
    customer_id: UUID | str,
    cart_ids: list[UUID | str],
) -> list[dict[str, Any]]:
    return _request(
        "POST",
        "/cart/items/delete-selected",
        customer_id,
        json={"cart_ids": [str(cart_id) for cart_id in cart_ids]},
    )


def clear_cart(customer_id: UUID | str) -> list[dict[str, Any]]:
    return _request("DELETE", "/cart", customer_id)


def prepare_order_selection(
    customer_id: UUID | str,
    cart_ids: list[UUID | str],
) -> dict[str, Any]:
    return _request(
        "POST",
        "/cart/order-selection",
        customer_id,
        json={"cart_ids": [str(cart_id) for cart_id in cart_ids]},
    )
