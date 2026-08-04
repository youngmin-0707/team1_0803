# 13_order.py

import streamlit as st

from clients.order_client import order_cancel, order_create, order_get, order_list
from clients.product_client import product_select_all
from core.api_client import BackendAPIError
from core.auth import is_logged_in

CANCELLABLE_STATUSES = {"pending", "paid"}

st.title("주문")

if not is_logged_in():
    st.warning("로그인이 필요합니다.")
    st.stop()

customer_id = st.session_state.login_id

create_tab, history_tab = st.tabs(["주문하기", "주문 내역"])

with create_tab:
    st.subheader("상품 선택 후 주문")
    try:
        products = product_select_all().get("data", [])
    except BackendAPIError as error:
        st.error(str(error))
        products = []

    if not products:
        st.info("주문할 수 있는 상품이 없습니다.")
    else:
        shipping_address = st.text_input("배송 주소")
        st.write("상품별 수량 (0이면 주문에서 제외)")

        quantities: dict[str, int] = {}
        for product in products:
            quantities[product["id"]] = st.number_input(
                f"{product['name']} (재고 {product['stock']}개, {product['price']:,}원)",
                min_value=0,
                max_value=product["stock"],
                value=0,
                step=1,
                key=f"order_qty_{product['id']}",
            )

        if st.button("주문하기", type="primary"):
            items = [
                {"product_id": product_id, "quantity": quantity}
                for product_id, quantity in quantities.items()
                if quantity > 0
            ]
            if not shipping_address.strip():
                st.warning("배송 주소를 입력해 주세요.")
            elif not items:
                st.warning("한 개 이상의 상품 수량을 입력해 주세요.")
            else:
                try:
                    result = order_create(
                        {
                            "customer_id": customer_id,
                            "shipping_address": shipping_address.strip(),
                            "items": items,
                        }
                    )
                    st.success(result["message"])
                    st.rerun()
                except BackendAPIError as error:
                    st.error(str(error))

with history_tab:
    st.subheader("내 주문 내역")
    try:
        orders = order_list(customer_id).get("data", [])
    except BackendAPIError as error:
        st.error(str(error))
        orders = []

    if not orders:
        st.info("주문 내역이 없습니다.")
    else:
        for order in orders:
            with st.container(border=True):
                st.write(f"주문 ID: {order['id']}")
                st.write(f"상태: {order['status']}")
                st.write(f"배송 주소: {order['shipping_address']}")
                st.write(f"주문일: {order['created_at']}")

                detail_column, cancel_column = st.columns(2)
                with detail_column:
                    if st.button("상세보기", key=f"order_detail_{order['id']}"):
                        detail_key = f"show_detail_{order['id']}"
                        st.session_state[detail_key] = not st.session_state.get(
                            detail_key, False
                        )
                with cancel_column:
                    if order["status"] in CANCELLABLE_STATUSES:
                        if st.button("주문 취소", key=f"order_cancel_{order['id']}"):
                            try:
                                order_cancel(order["id"])
                                st.success("주문이 취소되었습니다.")
                                st.rerun()
                            except BackendAPIError as error:
                                st.error(str(error))

                if st.session_state.get(f"show_detail_{order['id']}", False):
                    try:
                        detail = order_get(order["id"])["data"]
                        st.dataframe(
                            detail["items"],
                            use_container_width=True,
                            hide_index=True,
                        )
                        st.write(f"총 금액: {detail['total_amount']:,}원")
                    except BackendAPIError as error:
                        st.error(str(error))
