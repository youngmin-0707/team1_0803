"""장바구니 화면만 독립적으로 실행하는 로컬 Streamlit 앱입니다.

실행 위치: frontend 폴더
실행 명령: streamlit run ft_app_test_port.py --server.port 8502
접속 주소: http://127.0.0.1:8502
"""

import os

import streamlit as st


os.environ.setdefault("BACKEND_URL", "http://127.0.0.1:8001")

st.set_page_config(
    page_title="Cart Test",
    page_icon="🛒",
    layout="wide",
)

cart_page = st.Page(
    "app_pages/cart.py",
    title="장바구니",
    icon="🛒",
    default=True,
)

navigation = st.navigation([cart_page], position="hidden")
navigation.run()
