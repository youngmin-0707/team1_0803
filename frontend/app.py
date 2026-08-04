"""초보자를 위한 가장 간단한 Streamlit 멀티페이지 앱입니다."""

import streamlit as st
from streamlit_session_browser_storage import SessionStorage

from core.auth import init_state, is_logged_in, logout


st.set_page_config(
    page_title="Layout",
    page_icon="🌱",
    layout="wide",
)

# ========================================================================

storage = SessionStorage(key="login_session_storage")

stored_loginout = storage.getItem("loginout") or "logout"
stored_login_id = storage.getItem("login_id") or ""
stored_login_name = storage.getItem("login_name") or ""


if "loginout" not in st.session_state:
    init_state(stored_loginout, stored_login_id, stored_login_name)

if st.session_state.loginout != stored_loginout:
    storage.setItem(
        "loginout",
        st.session_state.loginout,
        key=f"save{st.session_state.loginout}",
    )
if st.session_state.loginout == "logout":
    # 브라우저 Session Storage의 로그인 정보 삭제
    storage.deleteAll(key="login_session_storage")
else:
    storage.setItem(
        "login_id",
        st.session_state.login_id,
        key="save_login_id",
    )
    storage.setItem(
        "login_name",
        st.session_state.login_name,
        key="save_login_name",
    )


# ========================================================================

home_page = st.Page("app_pages/01_home.py", title="홈", icon="🏠", default=True)
login_page = st.Page("app_pages/00_login.py", title="로그인", icon="🔐")
signup_page = st.Page("app_pages/02_signup.py", title="회원가입", icon="📝")
weather_page = st.Page("app_pages/03_weather.py", title="날씨조회", icon="🌥️")
health_page = st.Page("app_pages/04_health.py", title="서버체크", icon="❤️‍🩹")
# product_create_page = st.Page("app_pages/05_product_create.py", title="제품입력", icon="📥")
# product_select_page = st.Page("app_pages/06_product_select.py", title="제품조회", icon="🔍")
product_management_page = st.Page("app_pages/07_product_management.py", title="Product Management", icon="📥")
mypage_page = st.Page("app_pages/08_mypage.py", title="My Page", icon="📥")



if st.session_state.loginout == "login":
    pages = [
        home_page,
        mypage_page,
        product_management_page,
        # product_create_page,
        # product_select_page,
    ]
else:
    pages = [home_page, login_page, signup_page, health_page, weather_page,]


navigation = st.navigation(pages, position="hidden")

with st.sidebar:
    st.page_link(home_page)

    if st.session_state.loginout == "login":
        st.page_link(mypage_page)
        st.page_link(product_management_page)
        st.button("LOGOUT", on_click=logout, use_container_width=True)
        # st.page_link(product_create_page)
        # st.page_link(product_select_page)
    else:
        st.page_link(login_page)
        st.page_link(signup_page)
        st.page_link(health_page)
        st.page_link(weather_page)

navigation.run()