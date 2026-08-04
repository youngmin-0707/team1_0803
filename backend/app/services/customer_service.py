# 작성자: 권오현
# 작업 구분: port

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from fastapi import HTTPException

from app.core.password import hash_password
from app.core.supabase_client import get_supabase
from app.schemas.customer_schema import (
    CustomerCreate,
    CustomerPublic,
    CustomerUpdate,
)


def _execute(query: Any, message: str) -> list[dict[str, Any]]:
    try:
        result = query.execute()
    except Exception as error:
        raise HTTPException(status_code=500, detail=message) from error
    return result.data or []


def create_customer(payload: CustomerCreate) -> CustomerPublic:
    rows = _execute(
        get_supabase().table("customers").insert(
            {
                "name": payload.name.strip(),
                "pwd": hash_password(payload.pwd),
            }
        ),
        "회원을 등록하는 중 오류가 발생했습니다.",
    )
    if not rows:
        raise HTTPException(status_code=500, detail="회원 등록 결과가 없습니다.")
    return CustomerPublic.model_validate(rows[0])


def get_customers() -> list[CustomerPublic]:
    rows = _execute(
        get_supabase().table("customers")
        .select("id,name,created_at,updated_at")
        .order("created_at"),
        "회원 목록을 조회하는 중 오류가 발생했습니다.",
    )
    return [CustomerPublic.model_validate(row) for row in rows]


def get_customer(customer_id: UUID) -> CustomerPublic:
    rows = _execute(
        get_supabase().table("customers")
        .select("id,name,created_at,updated_at")
        .eq("id", str(customer_id))
        .limit(1),
        "회원을 조회하는 중 오류가 발생했습니다.",
    )
    if not rows:
        raise HTTPException(status_code=404, detail="회원을 찾을 수 없습니다.")
    return CustomerPublic.model_validate(rows[0])


def update_customer(
    customer_id: UUID,
    payload: CustomerUpdate,
) -> CustomerPublic:
    get_customer(customer_id)
    values: dict[str, Any] = {"updated_at": datetime.now(timezone.utc).isoformat()}
    if payload.name is not None:
        values["name"] = payload.name.strip()
    if payload.pwd is not None:
        values["pwd"] = hash_password(payload.pwd)

    rows = _execute(
        get_supabase().table("customers")
        .update(values)
        .eq("id", str(customer_id)),
        "회원 정보를 수정하는 중 오류가 발생했습니다.",
    )
    if not rows:
        raise HTTPException(status_code=500, detail="회원 수정 결과가 없습니다.")
    return CustomerPublic.model_validate(rows[0])


def delete_customer(customer_id: UUID) -> CustomerPublic:
    get_customer(customer_id)
    rows = _execute(
        get_supabase().table("customers")
        .delete()
        .eq("id", str(customer_id)),
        "회원을 삭제하는 중 오류가 발생했습니다. 연결된 데이터가 있는지 확인해 주세요.",
    )
    if not rows:
        raise HTTPException(status_code=500, detail="회원 삭제 결과가 없습니다.")
    return CustomerPublic.model_validate(rows[0])
