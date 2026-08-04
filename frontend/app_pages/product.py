# 작성자: 권오현
# 작업 구분: port

from uuid import UUID

import streamlit as st

from clients.product_client import (
    create_product,
    delete_product,
    get_products,
    update_product,
)
from core.api_client import BackendAPIError


def _category_value(value: str) -> str | None:
    if not value.strip():
        return None
    try:
        return str(UUID(value.strip()))
    except ValueError:
        st.warning("카테고리 UUID 형식을 확인해 주세요.")
        return "INVALID"


def _load_products() -> None:
    st.session_state.product_rows = get_products()


def render_product_page() -> None:
    st.title("상품 관리")
    st.caption("최신 ERD의 UUID·가격·재고 형식으로 상품을 관리합니다.")
    st.session_state.setdefault("product_rows", [])

    with st.form("product_create_form", clear_on_submit=True):
        name = st.text_input("상품명")
        price = st.number_input("가격", min_value=0, value=0, step=1000)
        stock = st.number_input("재고", min_value=0, value=0, step=1)
        category_input = st.text_input("카테고리 UUID", help="없으면 비워 두세요.")
        create_submitted = st.form_submit_button(
            "상품 등록", type="primary", use_container_width=True
        )

    if create_submitted:
        category_id = _category_value(category_input)
        if category_id != "INVALID":
            try:
                created = create_product(
                    {
                        "name": name.strip(),
                        "price": int(price),
                        "stock": int(stock),
                        "category_id": category_id,
                    }
                )
                st.success(f"상품을 등록했습니다. UUID: {created['id']}")
                _load_products()
            except BackendAPIError as error:
                st.error(str(error))

    if st.button("상품 목록 새로고침", use_container_width=True):
        try:
            _load_products()
        except BackendAPIError as error:
            st.error(str(error))

    products = st.session_state.product_rows
    if not products:
        st.info("등록된 상품이 없습니다.")
        return

    st.dataframe(products, use_container_width=True, hide_index=True)
    selected_id = st.selectbox(
        "수정 또는 삭제할 상품",
        options=[product["id"] for product in products],
        format_func=lambda product_id: next(
            f"{product['name']} · {product['id']}"
            for product in products
            if product["id"] == product_id
        ),
    )
    selected = next(product for product in products if product["id"] == selected_id)

    update_tab, delete_tab = st.tabs(["상품 수정", "상품 삭제"])
    with update_tab:
        with st.form("product_update_form"):
            new_name = st.text_input("상품명", value=selected["name"])
            new_price = st.number_input(
                "가격", min_value=0, value=int(selected["price"]), step=1000
            )
            new_stock = st.number_input(
                "재고", min_value=0, value=int(selected["stock"]), step=1
            )
            new_category = st.text_input(
                "카테고리 UUID", value=selected.get("category_id") or ""
            )
            update_submitted = st.form_submit_button(
                "상품 수정", type="primary", use_container_width=True
            )
        if update_submitted:
            category_id = _category_value(new_category)
            if category_id != "INVALID":
                try:
                    update_product(
                        selected_id,
                        {
                            "name": new_name.strip(),
                            "price": int(new_price),
                            "stock": int(new_stock),
                            "category_id": category_id,
                        },
                    )
                    _load_products()
                    st.success("상품 정보를 수정했습니다.")
                    st.rerun()
                except BackendAPIError as error:
                    st.error(str(error))

    with delete_tab:
        confirmed = st.checkbox(
            "연결된 장바구니·주문이 있으면 삭제가 제한될 수 있습니다.",
            key=f"product_delete_confirm_{selected_id}",
        )
        if st.button(
            "상품 삭제",
            disabled=not confirmed,
            use_container_width=True,
            key=f"product_delete_{selected_id}",
        ):
            try:
                delete_product(selected_id)
                _load_products()
                st.success("상품을 삭제했습니다.")
                st.rerun()
            except BackendAPIError as error:
                st.error(str(error))


render_product_page()
