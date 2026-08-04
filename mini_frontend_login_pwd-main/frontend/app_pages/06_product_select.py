# 06_product_select.py

import httpx
import streamlit as st


API_BASE_URL = "https://zero2-mini-project-8r38.onrender.com"
REQUEST_TIMEOUT = 15.0


def get_products() -> list[dict]:
    """백엔드에서 전체 제품 목록을 가져옵니다."""
    response = httpx.get(
        f"{API_BASE_URL}/product/getall",
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def refresh_products() -> None:
    """최신 제품 목록을 session_state에 저장합니다."""
    st.session_state.products = get_products()


def product_select() -> None:
    st.title("Product 조회")
    st.caption("등록된 제품을 조회하고 수정하거나 삭제할 수 있습니다.")

    # session_state 초기값 설정
    if "products" not in st.session_state:
        st.session_state.products = []

    if "products_loaded" not in st.session_state:
        st.session_state.products_loaded = False

    if "success_message" not in st.session_state:
        st.session_state.success_message = ""

    # 수정·삭제 후 성공 메시지 표시
    if st.session_state.success_message:
        st.success(st.session_state.success_message)
        st.session_state.success_message = ""

    # 제품 전체 조회
    select_button = st.button(
        "제품조회",
        type="primary",
        use_container_width=True,
    )

    if select_button:
        try:
            with st.spinner("제품 목록을 불러오고 있습니다."):
                refresh_products()

            st.session_state.products_loaded = True

        except httpx.TimeoutException:
            st.error(
                "서버 응답 시간이 초과되었습니다. "
                "잠시 후 다시 시도해 주세요."
            )

        except httpx.HTTPStatusError as error:
            st.warning(
                "제품 조회에 실패했습니다. "
                f"상태 코드: {error.response.status_code}"
            )

        except httpx.RequestError:
            st.error("백엔드 서버에 연결할 수 없습니다.")

        except ValueError:
            st.error("서버에서 올바른 제품 데이터를 받지 못했습니다.")

    # 조회된 제품이 있을 때
    if st.session_state.products:
        st.dataframe(
            st.session_state.products,
            use_container_width=True,
            hide_index=True,
        )

        st.divider()
        st.subheader("제품 수정 및 삭제")

        # 수정하거나 삭제할 제품 선택
        selected_product_id = st.selectbox(
            "제품을 선택하세요.",
            options=[
                product["id"]
                for product in st.session_state.products
            ],
            format_func=lambda product_id: next(
                (
                    f"{product['id']} - {product['name']}"
                    for product in st.session_state.products
                    if product["id"] == product_id
                ),
                str(product_id),
            ),
        )

        # 선택한 제품의 전체 정보 찾기
        selected_product = next(
            product
            for product in st.session_state.products
            if product["id"] == selected_product_id
        )

        update_tab, delete_tab = st.tabs(["제품 수정", "제품 삭제"])

        # 제품 수정
        with update_tab:
            with st.form(
                f"product_update_form_{selected_product_id}"
            ):
                update_name = st.text_input(
                    "수정할 상품명",
                    value=selected_product["name"],
                )

                update_price = st.number_input(
                    "수정할 가격",
                    min_value=0,
                    step=1000,
                    value=int(selected_product["price"]),
                )

                update_submitted = st.form_submit_button(
                    "제품 수정",
                    type="primary",
                    use_container_width=True,
                )

            if update_submitted:
                if not update_name.strip():
                    st.warning("수정할 상품명을 입력해 주세요.")

                else:
                    update_payload = {
                        "name": update_name.strip(),
                        "price": int(update_price),
                    }

                    try:
                        with st.spinner(
                            "제품 정보를 수정하고 있습니다."
                        ):
                            response = httpx.put(
                                (
                                    f"{API_BASE_URL}/product/update/"
                                    f"{selected_product_id}"
                                ),
                                json=update_payload,
                                timeout=REQUEST_TIMEOUT,
                            )
                            response.raise_for_status()

                            refresh_products()

                        st.session_state.success_message = (
                            "제품 수정이 완료되었습니다."
                        )
                        st.rerun()

                    except httpx.TimeoutException:
                        st.error(
                            "서버 응답 시간이 초과되었습니다. "
                            "잠시 후 다시 시도해 주세요."
                        )

                    except httpx.HTTPStatusError as error:
                        st.warning(
                            "제품 수정에 실패했습니다. "
                            f"상태 코드: {error.response.status_code}"
                        )

                    except httpx.RequestError:
                        st.error("백엔드 서버에 연결할 수 없습니다.")

                    except ValueError:
                        st.error(
                            "서버에서 올바른 제품 데이터를 받지 못했습니다."
                        )

        # 제품 삭제
        with delete_tab:
            st.warning(
                f"선택한 제품: "
                f"{selected_product['id']} - "
                f"{selected_product['name']}"
            )

            delete_confirmed = st.checkbox(
                "삭제할 제품을 확인했습니다.",
                key=f"delete_confirm_{selected_product_id}",
            )

            delete_button = st.button(
                "제품 삭제",
                type="primary",
                use_container_width=True,
                disabled=not delete_confirmed,
                key=f"delete_button_{selected_product_id}",
            )

            if delete_button:
                try:
                    with st.spinner("제품을 삭제하고 있습니다."):
                        response = httpx.delete(
                            (
                                f"{API_BASE_URL}/product/delete/"
                                f"{selected_product_id}"
                            ),
                            timeout=REQUEST_TIMEOUT,
                        )
                        response.raise_for_status()

                        refresh_products()

                    st.session_state.success_message = (
                        "제품 삭제가 완료되었습니다."
                    )
                    st.rerun()

                except httpx.TimeoutException:
                    st.error(
                        "서버 응답 시간이 초과되었습니다. "
                        "잠시 후 다시 시도해 주세요."
                    )

                except httpx.HTTPStatusError as error:
                    st.warning(
                        "제품 삭제에 실패했습니다. "
                        f"상태 코드: {error.response.status_code}"
                    )

                except httpx.RequestError:
                    st.error("백엔드 서버에 연결할 수 없습니다.")

                except ValueError:
                    st.error(
                        "서버에서 올바른 제품 데이터를 받지 못했습니다."
                    )

    # 조회했지만 제품이 없을 때
    elif st.session_state.products_loaded:
        st.info("등록된 제품이 없습니다.")


product_select()