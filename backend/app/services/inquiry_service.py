from datetime import datetime
from uuid import UUID
from zoneinfo import ZoneInfo

from fastapi import HTTPException, status

from app.core.supabase_client import get_supabase
from app.schemas.inquiry_schema import (
    Inquiry,
    InquiryAnswerUpdate,
    InquiryCreate,
    InquiryUpdate,
)


ANSWER_ROLES = {"admin", "answerer"}


def _now() -> str:
    """문의 시간 컬럼에 저장할 현재 시간을 반환합니다."""

    return datetime.now(ZoneInfo("Asia/Seoul")).isoformat()


def _get_by_id(supabase, table_name: str, record_id: UUID) -> dict | None:
    """테이블에서 UUID가 일치하는 데이터 한 건을 찾습니다."""

    result = (
        supabase.table(table_name)
        .select("*")
        .eq("id", str(record_id))
        .limit(1)
        .execute()
    )
    if not result.data:
        return None
    return result.data[0]


def _get_inquiry(supabase, inquiry_id: UUID) -> dict | None:
    return _get_by_id(supabase, "inquiries", inquiry_id)


def _check_owner(inquiry: dict, customer_id: UUID) -> None:
    """로그인 사용자와 문의 작성자가 같은지 확인합니다."""

    if str(inquiry["customer_id"]) != str(customer_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="본인이 작성한 문의만 수정하거나 삭제할 수 있습니다.",
        )


def create_inquiry(
    customer_id: UUID,
    inquiry_data: InquiryCreate,
) -> Inquiry:
    """로그인한 회원의 상품 문의를 작성합니다."""

    supabase = get_supabase()

    if _get_by_id(supabase, "customers", customer_id) is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="로그인한 회원 정보를 찾을 수 없습니다.",
        )

    if _get_by_id(supabase, "products", inquiry_data.product_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="상품을 찾을 수 없습니다.",
        )

    result = (
        supabase.table("inquiries")
        .insert(
            {
                "product_id": str(inquiry_data.product_id),
                "customer_id": str(customer_id),
                "title": inquiry_data.title,
                "content": inquiry_data.content,
            }
        )
        .execute()
    )
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="문의 작성에 실패했습니다.",
        )
    return Inquiry.model_validate(result.data[0])


def answer_inquiry(
    inquiry_id: UUID,
    answer_data: InquiryAnswerUpdate,
    customer_id: UUID,
    user_role: str,
) -> Inquiry:
    """답변 권한을 확인한 후 문의 답변을 등록하거나 수정합니다."""

    if user_role not in ANSWER_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="문의 답변 권한이 없습니다.",
        )

    supabase = get_supabase()

    if _get_by_id(supabase, "customers", customer_id) is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="로그인한 회원 정보를 찾을 수 없습니다.",
        )

    if _get_inquiry(supabase, inquiry_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="문의를 찾을 수 없습니다.",
        )

    now = _now()
    result = (
        supabase.table("inquiries")
        .update(
            {
                "answer": answer_data.answer,
                "answered_at": now,
                "updated_at": now,
            }
        )
        .eq("id", str(inquiry_id))
        .execute()
    )
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="문의 답변 저장에 실패했습니다.",
        )
    return Inquiry.model_validate(result.data[0])


def update_inquiry(
    inquiry_id: UUID,
    customer_id: UUID,
    inquiry_data: InquiryUpdate,
) -> Inquiry:
    """작성자 확인 후 문의 제목과 내용을 수정합니다."""

    supabase = get_supabase()
    inquiry = _get_inquiry(supabase, inquiry_id)
    if inquiry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="문의를 찾을 수 없습니다.",
        )

    _check_owner(inquiry, customer_id)

    result = (
        supabase.table("inquiries")
        .update(
            {
                "title": inquiry_data.title,
                "content": inquiry_data.content,
                "updated_at": _now(),
            }
        )
        .eq("id", str(inquiry_id))
        .execute()
    )
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="문의 수정에 실패했습니다.",
        )
    return Inquiry.model_validate(result.data[0])


def delete_inquiry(
    inquiry_id: UUID,
    customer_id: UUID,
) -> Inquiry:
    """작성자 확인 후 문의를 실제로 삭제합니다."""

    supabase = get_supabase()
    inquiry = _get_inquiry(supabase, inquiry_id)
    if inquiry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="문의를 찾을 수 없습니다.",
        )

    _check_owner(inquiry, customer_id)

    result = (
        supabase.table("inquiries")
        .delete()
        .eq("id", str(inquiry_id))
        .execute()
    )
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="문의 삭제에 실패했습니다.",
        )
    return Inquiry.model_validate(result.data[0])
