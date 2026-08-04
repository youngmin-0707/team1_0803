import streamlit as st

from clients.inquiry_client import (
    inquiry_answer,
    inquiry_create,
    inquiry_delete,
    inquiry_update,
)
from core.api_client import BackendAPIError
from core.auth import is_logged_in


st.title("상품 문의")
st.caption("상품 문의를 작성하고, 작성한 문의를 수정하거나 삭제할 수 있습니다.")

if not is_logged_in():
    st.warning("로그인이 필요합니다.")
    st.stop()

customer_id = st.session_state.login_id
user_role = st.session_state.get("user_role", "customer")

st.info(f"작성자: {st.session_state.login_name} ({customer_id})")

create_tab, update_tab, delete_tab, answer_tab = st.tabs(
    ["문의 작성", "문의 수정", "문의 삭제", "문의 답변"]
)


with create_tab:
    with st.form("inquiry_create_form", clear_on_submit=True):
        product_id = st.text_input(
            "상품 ID",
            placeholder="문의할 상품의 UUID를 입력하세요.",
        )
        title = st.text_input(
            "문의 제목",
            placeholder="문의 제목을 입력하세요.",
        )
        content = st.text_area(
            "문의 내용",
            placeholder="문의 내용을 입력하세요.",
        )
        create_submitted = st.form_submit_button(
            "문의 작성",
            type="primary",
            use_container_width=True,
        )

    if create_submitted:
        if not product_id.strip() or not title.strip() or not content.strip():
            st.warning("상품 ID, 문의 제목, 문의 내용을 모두 입력해 주세요.")
        else:
            try:
                result = inquiry_create(
                    customer_id,
                    {
                        "product_id": product_id.strip(),
                        "title": title.strip(),
                        "content": content.strip(),
                    },
                )
                st.success(result.get("message", "문의가 작성되었습니다."))
                if result.get("data"):
                    st.json(result["data"])
            except BackendAPIError as error:
                st.error(str(error))


with update_tab:
    with st.form("inquiry_update_form"):
        update_inquiry_id = st.text_input(
            "문의 ID",
            placeholder="수정할 문의의 UUID를 입력하세요.",
        )
        update_title = st.text_input("수정할 제목")
        update_content = st.text_area("수정할 내용")
        update_submitted = st.form_submit_button(
            "문의 수정",
            type="primary",
            use_container_width=True,
        )

    if update_submitted:
        if (
            not update_inquiry_id.strip()
            or not update_title.strip()
            or not update_content.strip()
        ):
            st.warning("문의 ID, 수정할 제목, 수정할 내용을 모두 입력해 주세요.")
        else:
            try:
                result = inquiry_update(
                    customer_id,
                    update_inquiry_id.strip(),
                    {
                        "title": update_title.strip(),
                        "content": update_content.strip(),
                    },
                )
                st.success(result.get("message", "문의가 수정되었습니다."))
                if result.get("data"):
                    st.json(result["data"])
            except BackendAPIError as error:
                st.error(str(error))


with delete_tab:
    with st.form("inquiry_delete_form"):
        delete_inquiry_id = st.text_input(
            "문의 ID",
            placeholder="삭제할 문의의 UUID를 입력하세요.",
        )
        delete_confirmed = st.checkbox("문의 삭제를 확인했습니다.")
        delete_submitted = st.form_submit_button(
            "문의 삭제",
            type="primary",
            use_container_width=True,
        )

    if delete_submitted:
        if not delete_inquiry_id.strip():
            st.warning("삭제할 문의 ID를 입력해 주세요.")
        elif not delete_confirmed:
            st.warning("삭제 확인 항목을 선택해 주세요.")
        else:
            try:
                result = inquiry_delete(customer_id, delete_inquiry_id.strip())
                st.success(result.get("message", "문의가 삭제되었습니다."))
            except BackendAPIError as error:
                st.error(str(error))


with answer_tab:
    if user_role not in {"admin", "answerer"}:
        st.info("문의 답변은 관리자 또는 답변 권한이 있는 사용자만 작성할 수 있습니다.")
    else:
        with st.form("inquiry_answer_form"):
            answer_inquiry_id = st.text_input(
                "문의 ID",
                placeholder="답변할 문의의 UUID를 입력하세요.",
            )
            answer_content = st.text_area(
                "답변 내용",
                placeholder="답변 내용을 입력하세요.",
            )
            answer_submitted = st.form_submit_button(
                "답변 저장",
                type="primary",
                use_container_width=True,
            )

        if answer_submitted:
            if not answer_inquiry_id.strip() or not answer_content.strip():
                st.warning("문의 ID와 답변 내용을 모두 입력해 주세요.")
            else:
                try:
                    result = inquiry_answer(
                        customer_id,
                        user_role,
                        answer_inquiry_id.strip(),
                        {"answer": answer_content.strip()},
                    )
                    st.success(
                        result.get("message", "문의 답변이 저장되었습니다.")
                    )
                    if result.get("data"):
                        st.json(result["data"])
                except BackendAPIError as error:
                    st.error(str(error))
