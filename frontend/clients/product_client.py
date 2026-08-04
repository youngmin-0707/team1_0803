# 작성자: 권오현
# 작업 구분: port

from typing import Any
from uuid import UUID

from clients.cart_client import _request


def create_product(values: dict[str, Any]) -> dict[str, Any]:
    return _request_without_customer("POST", "/products", values)


def get_products() -> list[dict[str, Any]]:
    return _request_without_customer("GET", "/products")


def update_product(
    product_id: UUID | str,
    values: dict[str, Any],
) -> dict[str, Any]:
    return _request_without_customer("PATCH", f"/products/{product_id}", values)


def delete_product(product_id: UUID | str) -> dict[str, Any]:
    return _request_without_customer("DELETE", f"/products/{product_id}")


def _request_without_customer(
    method: str,
    path: str,
    json: dict[str, Any] | None = None,
) -> Any:
    # Product API에는 장바구니용 회원 헤더가 필요하지 않습니다.
    return _request(method, path, "00000000-0000-0000-0000-000000000000", json)
