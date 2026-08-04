# 작성자: 권오현
# 작업 구분: port

from typing import Any
from uuid import UUID

from clients.cart_client import _request


def create_customer(name: str, pwd: str) -> dict[str, Any]:
    return _request_without_customer(
        "POST", "/customers", {"name": name, "pwd": pwd}
    )


def get_customers() -> list[dict[str, Any]]:
    return _request_without_customer("GET", "/customers")


def update_customer(
    customer_id: UUID | str,
    values: dict[str, Any],
) -> dict[str, Any]:
    return _request_without_customer(
        "PATCH", f"/customers/{customer_id}", values
    )


def delete_customer(customer_id: UUID | str) -> dict[str, Any]:
    return _request_without_customer("DELETE", f"/customers/{customer_id}")


def _request_without_customer(
    method: str,
    path: str,
    json: dict[str, Any] | None = None,
) -> Any:
    # Customer API에는 장바구니용 회원 헤더가 필요하지 않습니다.
    return _request(method, path, "00000000-0000-0000-0000-000000000000", json)
