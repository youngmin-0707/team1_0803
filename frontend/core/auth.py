"""공통 로그인 상태와 인증 동작을 관리합니다."""

import streamlit as st
from core.api_client import BackendAPIError
from clients.auth_client import login_process, logout_process

def init_state(
    stored_loginout: str = "logout",
    stored_login_id: str = "",
    stored_login_name: str = "",
) -> None:
    st.session_state.setdefault("loginout", stored_loginout)
    st.session_state.setdefault("login_id", stored_login_id)
    st.session_state.setdefault("login_name", stored_login_name)

# Login with Fronend
# def login(login_id:str, login_pwd:str) -> None:

#     if login_id == "id01" and login_pwd == "pwd01":
#         st.session_state.loginout = "login"
#         st.session_state.login_id = login_id
#         st.session_state.login_name = "이말숙"
#         st.rerun()
#     else:
#         st.error("로그인 아이디 또는 패스워드 틀림")

# def logout() -> None:
#     st.session_state.loginout = "logout"
#     st.session_state.login_id = ""
#     st.session_state.login_pwd = ""
#     st.session_state.login_name = ""

# Login with Backend
def login(login_id:str, login_pwd:str) -> None:
    try:
        result = login_process(login_id, login_pwd)
        if result is not None:
            st.session_state.loginout = "login"
            st.session_state.login_id = login_id
            st.session_state.login_name = result["name"]
            st.rerun()
    except BackendAPIError as error: 
        st.error(str(error))


def logout() -> None:
    result = logout_process(st.session_state.login_id)
    if result is not None:
        st.session_state.loginout = "logout"
        st.session_state.login_id = ""
        st.session_state.login_pwd = ""
        st.session_state.login_name = ""


def is_logged_in() -> bool:
    return st.session_state.loginout == "login"
