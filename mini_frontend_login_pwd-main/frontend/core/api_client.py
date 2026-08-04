"""모든 메뉴 API에서 공통으로 사용하는 HTTP 요청 기능."""

import os
from typing import Any

import httpx


BACKEND_URL = "http://127.0.0.1:8000"
# BACKEND_URL = "https://mini-frontend-02-mock-m4wy.onrender.com"
REQUEST_TIMEOUT = 15.0


class BackendAPIError(Exception):
    """백엔드 연결 또는 API 응답 처리 중 발생한 오류입니다."""


def request(method: str, path: str, json: dict[str, Any] | None = None):
    try:
        response = httpx.request(
            method,
            f"{BACKEND_URL}{path}",
            json=json,
            timeout=REQUEST_TIMEOUT,
        )
    except httpx.TimeoutException as error:
        raise BackendAPIError("백엔드 응답 시간이 초과되었습니다.") from error
    except httpx.RequestError as error:
        raise BackendAPIError(
            "백엔드 서버에 연결할 수 없습니다. 서버 실행 상태를 확인해 주세요."
        ) from error

    if response.status_code == 401:
        raise BackendAPIError(
            "로그인 아이디 또는 패스워드 문제."
        )

    if response.status_code == 409:
        raise BackendAPIError(
            "이미 사용중인 ID입니다."
        )

    if response.status_code == 404:
        raise BackendAPIError(
            "존재하지 않습니다."
        )


    try:
        payload = response.json()
    except ValueError as error:
        raise BackendAPIError("백엔드가 올바른 JSON을 반환하지 않았습니다.") from error

    return payload