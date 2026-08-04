# 작성자: 권오현
# 작업 구분: port

import streamlit as st

from clients.customer_client import (
    create_customer,
    delete_customer,
    get_customers,
    update_customer,
)
from core.api_client import BackendAPIError


def _load_customers() -> None:
    st.session_state.customer_rows = get_customers()


def render_customer_page() -> None:
    st.title("회원 관리")
    st.caption("최신 ERD의 UUID 회원 데이터를 생성하고 관리합니다.")
    st.session_state.setdefault("customer_rows", [])

    with st.form("customer_create_form", clear_on_submit=True):
        name = st.text_input("회원 이름")
        pwd = st.text_input("비밀번호", type="password")
        create_submitted = st.form_submit_button(
            "회원 등록", type="primary", use_container_width=True
        )

    if create_submitted:
        try:
            created = create_customer(name.strip(), pwd)
            st.success(f"회원을 등록했습니다. UUID: {created['id']}")
            _load_customers()
        except BackendAPIError as error:
            st.error(str(error))

    if st.button("회원 목록 새로고침", use_container_width=True):
        try:
            _load_customers()
        except BackendAPIError as error:
            st.error(str(error))

    customers = st.session_state.customer_rows
    if not customers:
        st.info("등록된 회원이 없습니다.")
        return

    st.dataframe(customers, use_container_width=True, hide_index=True)
    selected_id = st.selectbox(
        "수정 또는 삭제할 회원",
        options=[customer["id"] for customer in customers],
        format_func=lambda customer_id: next(
            f"{customer['name']} · {customer['id']}"
            for customer in customers
            if customer["id"] == customer_id
        ),
    )
    selected = next(customer for customer in customers if customer["id"] == selected_id)

    update_tab, delete_tab = st.tabs(["회원 수정", "회원 삭제"])
    with update_tab:
        with st.form("customer_update_form"):
            new_name = st.text_input("수정할 이름", value=selected["name"])
            new_pwd = st.text_input(
                "새 비밀번호", type="password", help="변경하지 않으려면 비워 두세요."
            )
            update_submitted = st.form_submit_button(
                "회원 수정", type="primary", use_container_width=True
            )
        if update_submitted:
            values = {"name": new_name.strip()}
            if new_pwd:
                values["pwd"] = new_pwd
            try:
                update_customer(selected_id, values)
                _load_customers()
                st.success("회원 정보를 수정했습니다.")
                st.rerun()
            except BackendAPIError as error:
                st.error(str(error))

    with delete_tab:
        confirmed = st.checkbox(
            "연결된 장바구니·주문이 있으면 삭제가 제한될 수 있습니다.",
            key=f"customer_delete_confirm_{selected_id}",
        )
        if st.button(
            "회원 삭제",
            disabled=not confirmed,
            use_container_width=True,
            key=f"customer_delete_{selected_id}",
        ):
            try:
                delete_customer(selected_id)
                _load_customers()
                st.success("회원을 삭제했습니다.")
                st.rerun()
            except BackendAPIError as error:
                st.error(str(error))


render_customer_page()
