import streamlit as st
from uuid import uuid4
from clients.auth_client import register_process
from core.api_client import BackendAPIError

def init_state():
    if "register_ok" not in st.session_state:
        st.session_state.register_ok = False
    if "register_name" not in st.session_state:
        st.session_state.register_name = ""
    if "register_id" not in st.session_state:
        st.session_state.register_id = ""

init_state()

#-------------------------------------------------------

st.title("📝 회원가입")


if st.session_state.register_ok == False:

    st.write("회원 정보를 입력해 주세요.")

    with st.form("signup_form", clear_on_submit=True):
        signup_pwd = st.text_input(
            "PWD",
            type="password",
            placeholder="사용할 비밀번호를 입력하세요",
        )
        signup_name = st.text_input(
            "이름",
            placeholder="이름을 입력하세요",
        )
        signup_submitted = st.form_submit_button(
            "회원가입",
            type="primary",
            use_container_width=True,
        )

    if signup_submitted:
        if not signup_pwd or not signup_name:
            st.warning("PWD와 이름을 모두 입력해 주세요.")
        else:
            signup_id = str(uuid4())
            payload = {
                "id": signup_id, 
                "pwd": signup_pwd, 
                "name": signup_name,
            }
            try:
                result = register_process(payload)
                if result is not None:
                    st.session_state.register_ok = True
                    st.session_state.register_name = result["name"]
                    st.session_state.register_id = result["id"]
                    st.rerun()
            except BackendAPIError as error:
                st.error(str(error))
                
else:
    st.success(f" {st.session_state.register_name}님, 회원가입 정보가 입력되었습니다.")
    st.info(f"로그인에 사용할 회원 ID: {st.session_state.register_id}")
    st.warning("회원 ID를 안전한 곳에 복사해 두세요.")
