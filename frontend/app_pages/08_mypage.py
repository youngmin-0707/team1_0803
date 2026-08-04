# 08_mypage.py

import streamlit as st

from clients.auth_client import (
    mypage_process, 
    update_password_process,
    update_process,
)
from core.api_client import BackendAPIError
from core.auth import is_logged_in

# mypage 회원조회 작성
"""회원 마이페이지 - ID를 입력하면 회원 정보(id, name)를 반환합니다."""

st.title("회원 마이페이지")
if not is_logged_in():
    st.warning("로그인이 필요합니다.")
    st.stop()

try:

    with st.spinner("Loading..."):
        get_mypage = mypage_process(st.session_state.login_id)

        with st.form("update_form", clear_on_submit=True):
            update_id = st.text_input(
                "ID",
                value = get_mypage["id"],
                disabled = True,
                placeholder="사용할 ID를 입력하세요",
            )
            update_pwd = st.text_input(
                "PWD",
                type="password",
                placeholder="비밀번호를 입력하세요",
            )
            update_pwd_com = st.text_input(
                "PWD 확인",
                type="password",
                placeholder="비밀번호를 다시 입력하세요",
            )
            update_name = st.text_input(
                "이름",
                value = get_mypage["name"],
                placeholder="이름을 입력하세요",
            )
            update_submitted = st.form_submit_button(
                "정보수정",
                type="primary",
                use_container_width=True,
            )

    if update_submitted:
        if not update_pwd or not update_pwd_com or not update_name:
            st.warning("PWD, 이름을 모두 입력해 주세요.")
        else:
            if update_pwd != update_pwd_com:
                st.warning("PWD와 PWD 확인이 일치하지 않습니다.")
            else:
                payload = {
                    "id": update_id, 
                    "pwd": update_pwd, 
                    "name": update_name,
                }
                try:
                    with st.spinner("회원정보 수정 진행 중..."):
                        result = update_process(payload)
                    if result is not None:
                        st.success("회원정보 수정이 완료되었습니다.")
                        st.rerun()
                except BackendAPIError as error:
                    st.error(str(error))

    st.write("id : ", get_mypage["id"])
    st.write("name : ", get_mypage["name"])

    
except BackendAPIError as error:
    st.error(str(error))
    st.stop()



# 비밀번호 변경 폼을 표시할지 기억하는 값
st.session_state.setdefault(
    "show_password_form",
    False,
)


if st.button("비밀번호 수정"):
    st.session_state.show_password_form = (
        not st.session_state.show_password_form
    )


if st.session_state.show_password_form:

    with st.form(
        "password_update_form",
        clear_on_submit=True,
    ):
        current_pwd = st.text_input(
            "현재 비밀번호",
            type="password",
            placeholder="현재 비밀번호를 입력하세요.",
        )

        new_pwd = st.text_input(
            "새 비밀번호",
            type="password",
            placeholder="새 비밀번호를 입력하세요.",
        )

        new_pwd_confirm = st.text_input(
            "새 비밀번호 확인",
            type="password",
            placeholder="새 비밀번호를 다시 입력하세요.",
        )

        submitted = st.form_submit_button(
            "변경하기"
        )


    if submitted:

        if not current_pwd:
            st.warning("현재 비밀번호를 입력하세요.")

        elif not new_pwd:
            st.warning("새 비밀번호를 입력하세요.")

        elif len(new_pwd) < 4:
            st.warning(
                "새 비밀번호는 4글자 이상이어야 합니다."
            )

        elif new_pwd != new_pwd_confirm:
            st.warning(
                "새 비밀번호가 서로 일치하지 않습니다."
            )

        elif current_pwd == new_pwd:
            st.warning(
                "새 비밀번호는 현재 비밀번호와 달라야 합니다."
            )

        else:
            try:
                result = update_password_process(
                    st.session_state.login_id,
                    current_pwd,
                    new_pwd,
                )

                st.success(result["message"])

                # 변경 성공 후 입력 폼 닫기
                st.session_state.show_password_form = False

            except BackendAPIError as error:
                st.error(str(error))