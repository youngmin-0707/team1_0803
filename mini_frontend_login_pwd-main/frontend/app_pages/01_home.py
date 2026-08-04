import streamlit as st
from core.auth import is_logged_in

st.title("🏠 홈")
if is_logged_in() == True:
    st.info(f"{st.session_state.login_id} 로그인 상태입니다.")
st.info("Layout에 오신 것을 환영합니다.")

col_visitors, col_logs, col_complete = st.columns(3)

with col_visitors:
    st.metric("접속자", "24명")

with col_logs:
    st.metric("로그 수", "128건")

with col_complete:
    st.metric("완료율", "76%")

st.caption("현재 표시된 수치는 화면 구성을 위한 예시 데이터입니다.")
st.write("왼쪽 메뉴에서 보고 싶은 화면을 선택해 보세요.")
