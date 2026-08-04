from uuid import UUID

import streamlit as st

from clients.cart_client import (
    add_cart_item,
    clear_cart,
    delete_cart_item,
    delete_selected_cart_items,
    get_cart,
    prepare_order_selection,
    update_cart_quantity,
)
from core.api_client import BackendAPIError


def _init_cart_state() -> None:
    st.session_state.setdefault("cart_customer_id", "")
    st.session_state.setdefault("cart_summary", None)
    st.session_state.setdefault("cart_success_message", "")
    st.session_state.setdefault("prepared_order", None)


def _parse_uuid(value: str, field_name: str) -> UUID | None:
    try:
        return UUID(value.strip())
    except (ValueError, AttributeError):
        st.warning(f"{field_name}에 올바른 UUID를 입력해 주세요.")
        return None


def _load_cart(show_error: bool = True) -> bool:
    customer_id = st.session_state.cart_customer_id
    if not customer_id:
        if show_error:
            st.info("먼저 테스트 회원 UUID를 설정해 주세요.")
        return False

    try:
        st.session_state.cart_summary = get_cart(customer_id)
        return True
    except BackendAPIError as error:
        if show_error:
            st.error(str(error))
        return False


def _finish_action(message: str) -> None:
    st.session_state.cart_success_message = message
    st.session_state.prepared_order = None
    _load_cart(show_error=False)
    st.rerun()


def _render_customer_section() -> None:
    st.subheader("테스트 회원")
    st.caption(
        "팀 로그인 연동 전까지 Supabase customers에 존재하는 회원 UUID를 사용합니다."
    )

    with st.form("cart_customer_form"):
        customer_input = st.text_input(
            "회원 UUID",
            value=st.session_state.cart_customer_id,
            placeholder="550e8400-e29b-41d4-a716-446655440000",
        )
        submitted = st.form_submit_button(
            "회원 설정 및 장바구니 조회",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        customer_id = _parse_uuid(customer_input, "회원 UUID")
        if customer_id is not None:
            st.session_state.cart_customer_id = str(customer_id)
            st.session_state.prepared_order = None
            if _load_cart():
                st.rerun()


def _render_add_form() -> None:
    st.subheader("상품 담기")
    with st.form("cart_add_form", clear_on_submit=True):
        product_input = st.text_input(
            "상품 UUID",
            placeholder="Supabase products에 존재하는 상품 UUID",
        )
        quantity = st.number_input(
            "수량",
            min_value=1,
            value=1,
            step=1,
        )
        submitted = st.form_submit_button(
            "장바구니 담기",
            type="primary",
            use_container_width=True,
            disabled=not bool(st.session_state.cart_customer_id),
        )

    if submitted:
        product_id = _parse_uuid(product_input, "상품 UUID")
        if product_id is None:
            return
        try:
            add_cart_item(
                st.session_state.cart_customer_id,
                product_id,
                int(quantity),
            )
            _finish_action("장바구니에 상품을 추가했습니다.")
        except BackendAPIError as error:
            st.error(str(error))


def _render_cart_item(item: dict) -> bool:
    cart_id = item["id"]
    available = bool(item.get("available"))
    product_name = item.get("product_name") or "삭제된 상품"
    price = item.get("price")
    stock = item.get("stock")
    quantity = int(item["quantity"])

    with st.container(border=True):
        selected = st.checkbox(
            f"{product_name} 선택",
            key=f"select_cart_{cart_id}",
            disabled=not available,
        )
        st.markdown(f"### {product_name}")

        info_columns = st.columns(4)
        info_columns[0].metric(
            "가격",
            f"{int(price):,}원" if price is not None else "확인 불가",
        )
        info_columns[1].metric(
            "재고",
            f"{int(stock):,}개" if stock is not None else "확인 불가",
        )
        info_columns[2].metric("현재 수량", f"{quantity:,}개")
        info_columns[3].metric(
            "상품 합계",
            f"{int(item.get('subtotal') or 0):,}원",
        )

        if item.get("availability_message"):
            st.warning(item["availability_message"])

        quantity_column, update_column, delete_column = st.columns([2, 1, 1])
        new_quantity = quantity_column.number_input(
            "변경할 수량",
            min_value=1,
            value=quantity,
            step=1,
            key=f"quantity_{cart_id}",
            disabled=not available,
        )

        if update_column.button(
            "수량 변경",
            key=f"update_{cart_id}",
            use_container_width=True,
            disabled=not available,
        ):
            try:
                update_cart_quantity(
                    st.session_state.cart_customer_id,
                    cart_id,
                    int(new_quantity),
                )
                _finish_action("상품 수량을 변경했습니다.")
            except BackendAPIError as error:
                st.error(str(error))

        if delete_column.button(
            "개별 삭제",
            key=f"delete_{cart_id}",
            use_container_width=True,
        ):
            try:
                delete_cart_item(st.session_state.cart_customer_id, cart_id)
                _finish_action("장바구니 상품을 삭제했습니다.")
            except BackendAPIError as error:
                st.error(str(error))

    return selected


def _render_cart_list() -> None:
    summary = st.session_state.cart_summary
    if summary is None:
        return

    items = summary.get("items", [])
    st.divider()
    title_column, refresh_column = st.columns([4, 1])
    title_column.subheader("장바구니 목록")
    if refresh_column.button("새로고침", use_container_width=True):
        if _load_cart():
            st.rerun()

    if not items:
        st.info("장바구니가 비어 있습니다.")
        return

    selected_ids: list[str] = []
    selected_price = 0
    for item in items:
        if _render_cart_item(item):
            selected_ids.append(item["id"])
            selected_price += int(item.get("subtotal") or 0)

    st.divider()
    total_columns = st.columns(3)
    total_columns[0].metric(
        "전체 수량",
        f"{int(summary.get('total_quantity') or 0):,}개",
    )
    total_columns[1].metric("선택 금액", f"{selected_price:,}원")
    total_columns[2].metric(
        "전체 금액",
        f"{int(summary.get('total_price') or 0):,}원",
    )

    selected_delete_column, order_column = st.columns(2)
    if selected_delete_column.button(
        "선택 상품 삭제",
        use_container_width=True,
        disabled=not selected_ids,
    ):
        try:
            delete_selected_cart_items(
                st.session_state.cart_customer_id,
                selected_ids,
            )
            _finish_action("선택한 장바구니 상품을 삭제했습니다.")
        except BackendAPIError as error:
            st.error(str(error))

    if order_column.button(
        "선택 상품 주문 정보 준비",
        type="primary",
        use_container_width=True,
        disabled=not selected_ids,
    ):
        try:
            st.session_state.prepared_order = prepare_order_selection(
                st.session_state.cart_customer_id,
                selected_ids,
            )
        except BackendAPIError as error:
            st.error(str(error))

    st.subheader("장바구니 전체 삭제")
    delete_confirmed = st.checkbox(
        "장바구니의 모든 상품을 삭제하는 것에 동의합니다.",
        key="clear_cart_confirmed",
    )
    if st.button(
        "전체 삭제",
        use_container_width=True,
        disabled=not delete_confirmed,
    ):
        try:
            clear_cart(st.session_state.cart_customer_id)
            _finish_action("장바구니를 비웠습니다.")
        except BackendAPIError as error:
            st.error(str(error))


def render_cart_page() -> None:
    _init_cart_state()
    st.title("장바구니")
    st.caption("상품 수량과 재고를 확인하고 주문할 상품을 선택합니다.")

    if st.session_state.cart_success_message:
        st.success(st.session_state.cart_success_message)
        st.session_state.cart_success_message = ""

    _render_customer_section()
    _render_add_form()
    _render_cart_list()

    if st.session_state.prepared_order is not None:
        st.subheader("주문 전달 예정 데이터")
        st.info("실제 주문 생성과 장바구니 삭제는 아직 수행하지 않습니다.")
        st.json(st.session_state.prepared_order)


render_cart_page()
