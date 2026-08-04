from typing import Any

import httpx

from core.api_client import BACKEND_URL, REQUEST_TIMEOUT, BackendAPIError


def _request_inquiry(
    method: str,
    path: str,
    customer_id: str,
    json: dict[str, Any] | None = None,
    user_role: str | None = None,
) -> dict:
    """로그인 정보 헤더를 포함해 문의 API를 호출합니다."""

    headers = {"X-Customer-Id": customer_id}
    if user_role is not None:
        headers["X-User-Role"] = user_role

    try:
        response = httpx.request(
            method,
            f"{BACKEND_URL}{path}",
            headers=headers,
            json=json,
            timeout=REQUEST_TIMEOUT,
        )
    except httpx.TimeoutException as error:
        raise BackendAPIError("백엔드 응답 시간이 초과되었습니다.") from error
    except httpx.RequestError as error:
        raise BackendAPIError(
            "백엔드 서버에 연결할 수 없습니다. 서버 실행 상태를 확인해 주세요."
        ) from error

    try:
        payload = response.json()
    except ValueError as error:
        raise BackendAPIError("백엔드가 올바른 JSON을 반환하지 않았습니다.") from error

    if response.is_error:
        detail = payload.get("detail", "문의 요청 처리에 실패했습니다.")
        if isinstance(detail, list):
            detail = "입력값을 확인해 주세요."
        raise BackendAPIError(str(detail))

    return payload


def inquiry_create(customer_id: str, inquiry: dict) -> dict:
    return _request_inquiry(
        "POST",
        "/inquiries",
        customer_id,
        json=inquiry,
    )


def inquiry_answer(
    customer_id: str,
    user_role: str,
    inquiry_id: str,
    answer: dict,
) -> dict:
    return _request_inquiry(
        "PUT",
        f"/inquiries/{inquiry_id}/answer",
        customer_id,
        json=answer,
        user_role=user_role,
    )


def inquiry_update(
    customer_id: str,
    inquiry_id: str,
    inquiry: dict,
) -> dict:
    return _request_inquiry(
        "PUT",
        f"/inquiries/{inquiry_id}",
        customer_id,
        json=inquiry,
    )


def inquiry_delete(customer_id: str, inquiry_id: str) -> dict:
    return _request_inquiry(
        "DELETE",
        f"/inquiries/{inquiry_id}",
        customer_id,
    )
