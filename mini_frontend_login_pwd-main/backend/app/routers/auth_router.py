# auth_router.py

from fastapi import APIRouter
from app.schemas.auth_scheme import (
    AuthCreate,
    AuthPublic,
    AuthLogin,
    PasswordUpdate,
    AuthUpdate,
)
from app.services.auth_service import (
    sign_up_process,
    sign_in_process,
    sign_out_process,
    my_page_process,
    update_password_process,
    update_process
)

auth_router = APIRouter(tags=["Auth"])

@auth_router.post("/auth/create")
def create(auth:AuthCreate) -> AuthPublic:
    """신규 입력"""
    return sign_up_process(auth)

@auth_router.put("/auth/update")
def update(auth:AuthUpdate) -> AuthPublic:
    """회원정보수정"""
    return update_process(auth)

@auth_router.post("/auth/signin")
def signin(auth:AuthLogin) -> AuthPublic:
    """로그인"""
    return sign_in_process(auth)

@auth_router.get("/auth/signout/{input_id}")
def signout(input_id:str) -> AuthPublic:
    return sign_out_process(input_id)

@auth_router.get("/auth/mypage/{input_id}")
def mypage(input_id:str) -> AuthPublic:
    """회원 마이페이지 - ID를 입력하면 회원 정보(id, name)를 반환합니다."""
    return my_page_process(input_id)

@auth_router.put("/auth/password/{input_id}")
def update_password(
    input_id: str,
    password_data: PasswordUpdate,
):
    """회원 비밀번호 변경"""
    return update_password_process(input_id, password_data)