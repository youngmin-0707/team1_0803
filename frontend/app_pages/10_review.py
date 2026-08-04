import streamlit as st

from clients.review_client import (
    review_create,
    review_delete,
    review_getall,
    review_update,
)
from core.api_client import BackendAPIError


st.title("⭐ 상품 리뷰")
st.write("상품 리뷰와 평균 별점을 확인합니다.")


# 팀 프로젝트에서 저장하는 세션 키에 맞춰 조정
product_id = st.session_state.get("selected_product_id", "")
customer_id = st.session_state.get("login_id", "")


if not customer_id:
    st.warning("로그인 후 리뷰를 이용할 수 있습니다.")
    st.stop()

if not product_id:
    st.warning("리뷰를 확인할 상품을 먼저 선택해 주세요.")
    st.stop()


# 리뷰 목록 조회
try:
    review_result = review_getall(product_id)
    review_data = review_result.get("data", {})

except BackendAPIError as error:
    st.error(str(error))
    st.stop()


reviews = review_data.get("reviews", [])
average_rating = review_data.get("average_rating", 0.0)
review_count = review_data.get("review_count", 0)


# 평균 별점과 리뷰 개수
average_column, count_column = st.columns(2)

with average_column:
    st.metric(
        "평균 별점",
        f"{average_rating:.1f} / 5.0",
    )

with count_column:
    st.metric(
        "리뷰 개수",
        f"{review_count}개",
    )


# 리뷰 작성
st.subheader("리뷰 작성")

with st.form(
    "review_create_form",
    clear_on_submit=True,
):
    create_rating = st.slider(
        "별점",
        min_value=1,
        max_value=5,
        value=5,
    )

    create_content = st.text_area(
        "내용",
        placeholder="상품 후기를 남겨 주세요.",
    )

    create_submitted = st.form_submit_button(
        "리뷰 등록",
        type="primary",
        use_container_width=True,
    )


if create_submitted:
    try:
        result = review_create(
            {
                "product_id": product_id,
                "customer_id": customer_id,
                "rating": create_rating,
                "content": create_content.strip() or None,
            }
        )

        st.success(result["message"])
        st.rerun()

    except BackendAPIError as error:
        st.error(str(error))


# 리뷰 목록
st.subheader("리뷰 목록")

if not reviews:
    st.info("아직 작성된 리뷰가 없습니다.")


for review in reviews:
    review_id = review["id"]
    is_my_review = (
        str(review["customer_id"]) == str(customer_id)
    )

    with st.container(border=True):
        st.write(
            f"{'⭐' * review['rating']} "
            f"({review['rating']}점)"
        )

        st.write(review.get("content") or "작성된 내용이 없습니다.")
        st.caption(f"작성일: {review['created_at']}")

        # 작성자 본인에게만 수정·삭제 메뉴를 표시합니다.
        if not is_my_review:
            continue

        st.caption("내가 작성한 리뷰")

        with st.expander("내 리뷰 수정 또는 삭제"):
            with st.form(f"review_update_form_{review_id}"):
                update_rating = st.slider(
                    "별점 수정",
                    min_value=1,
                    max_value=5,
                    value=int(review["rating"]),
                    key=f"rating_{review_id}",
                )

                update_content = st.text_area(
                    "내용 수정",
                    value=review.get("content") or "",
                    key=f"content_{review_id}",
                )

                update_submitted = st.form_submit_button(
                    "수정",
                    use_container_width=True,
                )

            if update_submitted:
                try:
                    result = review_update(
                        review_id,
                        {
                            "customer_id": customer_id,
                            "rating": update_rating,
                            "content": update_content.strip() or None,
                        },
                    )

                    st.success(result["message"])
                    st.rerun()

                except BackendAPIError as error:
                    st.error(str(error))

            delete_submitted = st.button(
                "삭제",
                key=f"delete_{review_id}",
                use_container_width=True,
            )

            if delete_submitted:
                try:
                    result = review_delete(
                        review_id,
                        customer_id,
                    )

                    st.success(result["message"])
                    st.rerun()

                except BackendAPIError as error:
                    st.error(str(error))
