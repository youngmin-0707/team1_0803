import httpx
import streamlit as st


API_BASE_URL = "https://zero2-mini-project-8r38.onrender.com"


def product_create() -> None:
    st.title("Product 입력")
    st.caption("등록할 상품 정보를 입력해 주세요.")

    with st.form("product_form", clear_on_submit=True):
        product_id = st.number_input("ID", min_value=1, step=1)
        product_name = st.text_input(
            "NAME",
            placeholder="품명을 입력하세요.",
        )
        product_price = st.number_input(
            "PRICE",
            min_value=0,
            step=1000,
        )

        submitted = st.form_submit_button("전송")

    if submitted:
        if not product_name.strip():
            st.warning("상품명을 입력해 주세요.")
        else:
            product_name = product_name.strip()

            payload = {
                "id": int(product_id),
                "name": product_name,
                "price": int(product_price),
            }

            try:
                with st.spinner("상품 정보를 전송하고 있습니다."):
                    response = httpx.post(
                        f"{API_BASE_URL}/product/create",
                        json=payload,
                        timeout=15.0,
                    )

                if response.status_code == 200:
                    result = response.json()

                    st.success("상품 입력이 완료되었습니다.")
                    st.info(
                        f"ID: {result['id']} / "
                        f"상품명: {result['name']} / "
                        f"가격: {result['price']}원"
                    )
                else:
                    st.warning(
                        f"상품 입력에 실패했습니다. "
                        f"상태 코드: {response.status_code}"
                    )

            except httpx.TimeoutException:
                st.error(
                    "서버 응답 시간이 초과되었습니다. "
                    "잠시 후 다시 시도해 주세요."
                )

            except httpx.RequestError:
                st.error("백엔드 서버에 연결할 수 없습니다.")


product_create()