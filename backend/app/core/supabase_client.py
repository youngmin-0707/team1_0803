"""Supabase 연결을 만드는 공통 helper입니다."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import Client, create_client


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"


def get_required_env(name: str) -> str:
    """필수 환경 변수를 읽고, 비어 있거나 예시 값이면 오류를 냅니다."""

    value = os.getenv(name, "").strip()

    if not value:
        raise RuntimeError(f"{name} 값이 없습니다. .env 파일을 확인하세요.")

    if value.startswith(("your-", "https://your-")):
        raise RuntimeError(f"{name} 값이 예시 값입니다. Supabase Dashboard에서 실제 값을 복사해 넣어 주세요.")

    return value


def get_supabase() -> Client:
    """Supabase client를 생성합니다."""

    load_dotenv(ENV_PATH)

    url = get_required_env("SUPABASE_URL")
    service_role_key = get_required_env("SUPABASE_SERVICE_ROLE_KEY")

    return create_client(url, service_role_key)
