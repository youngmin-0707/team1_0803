import streamlit as st

from core.auth import is_logged_in, login, logout


if not is_logged_in():
    st.title("LOGIN")

    with st.form("login_form", clear_on_submit=True):
        login_id = st.text_input("ID 입력", value="id01")
        login_pwd = st.text_input("PWD 입력", type="password", value="pwd01")
        submitted = st.form_submit_button("LOGIN")

    if submitted:
        login(login_id, login_pwd)

else:
    st.success("로그인되었습니다.")
    st.button("LOGOUT", on_click=logout)
