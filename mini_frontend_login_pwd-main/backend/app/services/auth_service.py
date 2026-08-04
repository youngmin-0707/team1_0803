from app.core.supabase_client import get_supabase
from fastapi import HTTPException
from app.schemas.auth_scheme import (
    AuthCreate, AuthLogin, AuthPublic, PasswordUpdate, AuthUpdate
)
from app.core.password import hash_password, verify_password


def sign_up_process(auth: AuthCreate):
    """ 회원 가입 """
    supabase = get_supabase()
    db_customer = _customer_get(auth.id)
    if db_customer is not None:
        raise HTTPException(
            status_code=409,
            detail="이미 사용 중인 아이디입니다."
        )
    result = (
        supabase.table("customers")
         .insert(
            {
                "id": auth.id,
                "pwd": hash_password(auth.pwd),
                "name": auth.name,
            }
        )
        .execute()
    )
    if not result.data:
        raise HTTPException(
                status_code = 500,
                detail = "DB 장애"
            )
    return AuthPublic.model_validate(result.data[0])

def update_process(auth: AuthUpdate):
    """ 회원정보 수정 """
    supabase = get_supabase()
    if not _customer_get(auth.id):
        raise HTTPException(
            status_code = 404,
            detail="이미 사용 중인 아이디입니다."
        )
    result = (
        supabase.table("customers")
         .update(
            {
                "pwd": hash_password(auth.pwd),
                "name": auth.name,
            }
        )
        .eq("id", auth.id)
        .execute()
    )
    if not result.data:
        raise HTTPException(
                status_code = 500,
                detail = "DB 장애"
            )
    return AuthPublic.model_validate(result.data[0])

def sign_in_process(auth: AuthLogin):
    """ 회원 로그인 """
    db_customer = _customer_get(auth.id)
    if db_customer is None:
        raise HTTPException(
            status_code=401,
            detail="사용자를 찾을 수 없습니다."
        )
    if verify_password(auth.pwd, db_customer["pwd"]):
        payload = {
            "id": db_customer["id"],
            "name": db_customer["name"],
        }
        return AuthPublic.model_validate(payload)
    else:
        raise HTTPException(
            status_code = 401,
            detail = "아이디 또는 패스워드가 올바르지 않습니다."
        )

def sign_out_process(input_id:str):
    """ 회원 로그 아웃 """

    return AuthPublic(
        id = input_id,
    )

def update_password_process(
    input_id: str,
    password_data: PasswordUpdate,
):
    """기존 비밀번호를 확인한 후 새 비밀번호로 변경합니다."""

    supabase = get_supabase()
    db_customer = _customer_get(input_id)

    if db_customer is None:
        raise HTTPException(
            status_code=404,
            detail="사용자를 찾을 수 없습니다.",
        )

    if not verify_password(
        password_data.current_pwd,
        db_customer["pwd"],
    ):
        raise HTTPException(
            status_code=401,
            detail="현재 비밀번호가 올바르지 않습니다.",
        )

    if password_data.current_pwd == password_data.new_pwd:
        raise HTTPException(
            status_code=400,
            detail="새 비밀번호는 현재 비밀번호와 달라야 합니다.",
        )

    result = (
        supabase.table("customers")
        .update(
            {
                "pwd": hash_password(password_data.new_pwd),
            }
        )
        .eq("id", input_id)
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=500,
            detail="비밀번호를 변경하지 못했습니다.",
        )

    return {
        "message": "비밀번호가 변경되었습니다.",
    }

def my_page_process(input_id:str):
    """ 회원 마이페이지 """

    db_customer = _customer_get(input_id)
    if db_customer is None:
        raise HTTPException(
            status_code=401,
            detail="사용자를 찾을 수 없습니다."
        )
    return AuthPublic.model_validate(db_customer)

def _customer_get(customer_id: str) -> dict | None:
    supabase = get_supabase()

    result = (
        supabase.table("customers")
        .select("*")
        .eq("id", customer_id)
        .execute()
    )
    if not result.data:
        return None
    return result.data[0]