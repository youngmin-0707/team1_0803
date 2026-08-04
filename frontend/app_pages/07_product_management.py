# 07_product_management.py

import pandas as pd
import streamlit as st

from clients.product_client import (
    product_create,
    product_delete,
    product_select_all,
    product_update,
)
from core.api_client import BackendAPIError


st.title("Product Management")
st.caption("상품을 등록하고 조회·수정·삭제할 수 있습니다.")


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