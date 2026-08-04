from core.api_client import request

def login_process(id:str, pwd:str):
    """ 로그인 진행 ID와 PWD 입력하면 사용자 정보 리턴 """
    return request("POST", f"/auth/signin", json={"id":id, "pwd":pwd})

def logout_process(id:str):
    return request("GET", f"/auth/signout/{id}")

def register_process(auth:dict):
    return request("POST", f"/auth/create", json=auth)

def update_process(auth:dict):
    return request("PUT", f"/auth/update", json=auth)

def mypage_process(id:str):
    """ 회원 마이페이지 - ID를 입력하면 회원 정보(id, name)를 반환합니다. """
    return request("GET", f"/auth/mypage/{id}")

def update_password_process(
    user_id: str,
    current_pwd: str,
    new_pwd: str,
):
    return request(
        "PUT",
        f"/auth/password/{user_id}",
        json={
            "current_pwd": current_pwd,
            "new_pwd": new_pwd,
        },
    )