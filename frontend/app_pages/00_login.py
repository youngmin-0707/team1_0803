import streamlit as st

from core.auth import is_logged_in, login, logout


if not is_logged_in():
    st.title("LOGIN")

    with st.form("login_form", clear_on_submit=True):
        login_id = st.text_input(
            "회원 ID(UUID) 입력",
            placeholder="회원가입 후 발급된 UUID를 입력하세요.",
        )
        login_pwd = st.text_input("PWD 입력", type="password")
        submitted = st.form_submit_button("LOGIN")

    if submitted:
        login(login_id, login_pwd)

else:
    st.success("로그인되었습니다.")
    st.button("LOGOUT", on_click=logout)
