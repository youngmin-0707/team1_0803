import streamlit as st

from clients.category_client import (
    category_create,
    category_delete,
    category_products,
    category_select_all,
    category_update,
)
from core.api_client import BackendAPIError


st.title("카테고리")
management_tab, shopping_tab = st.tabs(["카테고리 관리", "카테고리별 상품"])


def load_categories() -> list[dict]:
    return category_select_all().get("data", [])


with management_tab:
    st.subheader("카테고리 등록")
    with st.form("category_create_form", clear_on_submit=True):
        new_name = st.text_input("카테고리 이름")
        create_submitted = st.form_submit_button("등록", type="primary")

    if create_submitted:
        if not new_name.strip():
            st.warning("카테고리 이름을 입력해 주세요.")
        else:
            try:
                result = category_create(new_name.strip())
                st.success(result["message"])
                st.rerun()
            except BackendAPIError as error:
                st.error(str(error))

    try:
        categories = load_categories()
        if not categories:
            st.info("등록된 카테고리가 없습니다.")
        for category in categories:
            with st.container(border=True):
                name_column, update_column, delete_column = st.columns([3, 1, 1])
                with name_column:
                    edited_name = st.text_input(
                        "이름", value=category["name"],
                        key=f"category_name_{category['id']}",
                    )
                with update_column:
                    if st.button("수정", key=f"category_update_{category['id']}"):
                        if not edited_name.strip():
                            st.warning("카테고리 이름을 입력해 주세요.")
                        else:
                            try:
                                category_update(category["id"], edited_name.strip())
                                st.success("카테고리가 수정되었습니다.")
                                st.rerun()
                            except BackendAPIError as error:
                                st.error(str(error))
                with delete_column:
                    if st.button("삭제", key=f"category_delete_{category['id']}"):
                        try:
                            category_delete(category["id"])
                            st.success("카테고리가 삭제되었습니다.")
                            st.rerun()
                        except BackendAPIError as error:
                            st.error(str(error))
    except BackendAPIError as error:
        st.error(str(error))

with shopping_tab:
    st.subheader("카테고리별 상품 조회")
    try:
        shop_categories = load_categories()
        if not shop_categories:
            st.info("선택할 카테고리가 없습니다.")
        else:
            selected_id = st.selectbox(
                "카테고리 선택",
                options=[category["id"] for category in shop_categories],
                format_func=lambda value: next(
                    category["name"] for category in shop_categories
                    if category["id"] == value
                ),
            )
            products = category_products(selected_id).get("data", [])
            if not products:
                st.info("이 카테고리에 등록된 상품이 없습니다.")
            else:
                st.dataframe(products, use_container_width=True, hide_index=True)
    except BackendAPIError as error:
        st.error(str(error))
