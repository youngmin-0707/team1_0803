# 07_product_management.py

import pandas as pd
import streamlit as st

from clients.product_client import (
    product_create,
    product_delete,
    product_select_all,
    product_update,
)
from clients.category_client import category_select_all
from core.api_client import BackendAPIError


st.title("Product Management")
st.caption("상품을 등록하고 조회·수정·삭제할 수 있습니다.")

try:
    categories = category_select_all().get("data", [])
except BackendAPIError as error:
    categories = []
    st.warning(f"카테고리 목록을 불러오지 못했습니다: {error}")

category_options = [None] + [category["id"] for category in categories]


def category_label(category_id) -> str:
    if category_id is None:
        return "카테고리 없음"
    return next(
        (category["name"] for category in categories if category["id"] == category_id),
        str(category_id),
    )


# 상품 등록
st.subheader("상품 등록")

with st.form("product_create_form", clear_on_submit=True):
    product_name = st.text_input(
        "NAME",
        placeholder="상품명을 입력하세요.",
    )

    product_price = st.number_input(
        "PRICE",
        min_value=1,
        step=1000,
    )

    product_stock = st.number_input(
        "STOCK",
        min_value=0,
        step=1,
    )

    product_category_id = st.selectbox(
        "CATEGORY",
        options=category_options,
        format_func=category_label,
    )

    create_submitted = st.form_submit_button(
        "상품 등록",
        type="primary",
        use_container_width=True,
    )

if create_submitted:
    if not product_name.strip():
        st.warning("상품명을 입력해 주세요.")

    else:
        product = {
            "name": product_name.strip(),
            "price": int(product_price),
            "stock": int(product_stock),
            "category_id": product_category_id,
        }

        try:
            result = product_create(product)

            if result.get("success"):
                created_product = result["data"]

                st.success(result["message"])
                st.info(
                    f"ID: {created_product['id']} / "
                    f"상품명: {created_product['name']} / "
                    f"가격: {created_product['price']}원"
                )
            else:
                st.error(result.get("message", "상품 등록에 실패했습니다."))

        except BackendAPIError as error:
            st.error(str(error))


st.divider()


# 상품 삭제 창
@st.dialog("상품 삭제")
def show_delete_dialog(product: dict) -> None:
    st.warning("정말 삭제하시겠습니까?")
    st.write(f"상품명: {product['name']}")
    st.write(f"가격: {product['price']}원")

    if st.button(
        "삭제하기",
        type="primary",
        use_container_width=True,
    ):
        try:
            with st.spinner("상품을 삭제하고 있습니다."):
                product_delete(product["id"])

            st.success("상품이 삭제되었습니다.")
            st.rerun()

        except BackendAPIError as error:
            st.error(str(error))


# 상품 수정 창
@st.dialog("상품 수정")
def show_update_dialog(product: dict) -> None:
    st.write(f"상품 ID: {product['id']}")

    with st.form(f"product_update_form_{product['id']}"):
        update_name = st.text_input(
            "NAME",
            value=product["name"],
        )

        update_price = st.number_input(


            
            "PRICE",
            min_value=1,
            step=1000,
            value=int(product["price"]),
        )

        update_stock = st.number_input(
            "STOCK",
            min_value=0,
            step=1,
            value=int(product["stock"]),
        )

        current_category_id = product.get("category_id")
        selected_index = (
            category_options.index(current_category_id)
            if current_category_id in category_options else 0
        )
        update_category_id = st.selectbox(
            "CATEGORY",
            options=category_options,
            index=selected_index,
            format_func=category_label,
        )

        update_submitted = st.form_submit_button(
            "수정하기",
            type="primary",
            use_container_width=True,
        )

    if update_submitted:
        if not update_name.strip():
            st.warning("상품명을 입력해 주세요.")

        else:
            update_product = {
                "name": update_name.strip(),
                "price": int(update_price),
                "stock": int(update_stock),
                "category_id": update_category_id,
            }

            try:
                with st.spinner("상품 정보를 수정하고 있습니다."):
                    result = product_update(
                        product["id"],
                        update_product,
                    )

                st.success(result.get("message", "상품 정보가 수정되었습니다."))
                st.rerun()

            except BackendAPIError as error:
                st.error(str(error))


st.divider()


# 상품 조회
st.subheader("상품 전체 목록")
st.caption("등록된 상품을 조회하고 수정하거나 삭제할 수 있습니다.")

try:
    with st.spinner("상품 목록을 불러오고 있습니다."):
        result = product_select_all()

    # 실제 상품 목록만 꺼내기
    products = result.get("data", [])

    if not products:
        st.info("등록된 상품이 없습니다.")

    else:
        for product in products:
            with st.container(border=True):
                information_column, button_column = st.columns([4, 1])

                with information_column:
                    st.write(f"**상품명:** {product['name']}")
                    st.write(f"**가격:** {product['price']:,}원")
                    st.write(f"**재고:** {product['stock']:,}개")
                    st.write(f"**카테고리:** {category_label(product.get('category_id'))}")
                    st.caption(f"ID: {product['id']}")

                with button_column:
                    if st.button(
                        "수정",
                        key=f"update_{product['id']}",
                        use_container_width=True,
                    ):
                        show_update_dialog(product)

                    if st.button(
                        "삭제",
                        key=f"delete_{product['id']}",
                        use_container_width=True,
                    ):
                        show_delete_dialog(product)

except BackendAPIError as error:
    st.error(str(error))
