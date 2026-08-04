from datetime import datetime
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

from app.core.supabase_client import get_supabase
from app.schemas.category_schema import CategoryCreate, CategoryPublic, CategoryUpdate


class CategoryAlreadyExistsError(Exception):
    pass


class CategoryInUseError(Exception):
    pass


def _now() -> str:
    return datetime.now(ZoneInfo("Asia/Seoul")).isoformat()


def _find_by_name(name: str, exclude_id: UUID | None = None) -> dict | None:
    query = get_supabase().table("categories").select("*").ilike("name", name)
    if exclude_id is not None:
        query = query.neq("id", str(exclude_id))
    result = query.limit(1).execute()
    return result.data[0] if result.data else None


def category_create(category: CategoryCreate) -> CategoryPublic:
    if _find_by_name(category.name):
        raise CategoryAlreadyExistsError

    now = _now()
    result = (
        get_supabase()
        .table("categories")
        .insert({
            "id": str(uuid4()),
            "name": category.name,
            "created_at": now,
            "updated_at": now,
        })
        .execute()
    )
    if not result.data:
        raise RuntimeError("카테고리를 등록하지 못했습니다.")
    return CategoryPublic.model_validate(result.data[0])


def category_get_all() -> list[CategoryPublic]:
    result = (
        get_supabase().table("categories").select("*").order("name").execute()
    )
    return [CategoryPublic.model_validate(item) for item in result.data]


def category_get(category_id: UUID) -> CategoryPublic | None:
    result = (
        get_supabase().table("categories").select("*")
        .eq("id", str(category_id)).limit(1).execute()
    )
    if not result.data:
        return None
    return CategoryPublic.model_validate(result.data[0])


def category_update(category_id: UUID, category: CategoryUpdate) -> CategoryPublic | None:
    if _find_by_name(category.name, exclude_id=category_id):
        raise CategoryAlreadyExistsError

    result = (
        get_supabase().table("categories")
        .update({"name": category.name, "updated_at": _now()})
        .eq("id", str(category_id)).execute()
    )
    if not result.data:
        return None
    return CategoryPublic.model_validate(result.data[0])


def category_delete(category_id: UUID) -> CategoryPublic | None:
    products = (
        get_supabase().table("products").select("id")
        .eq("category_id", str(category_id)).limit(1).execute()
    )
    if products.data:
        raise CategoryInUseError

    result = (
        get_supabase().table("categories").delete()
        .eq("id", str(category_id)).execute()
    )
    if not result.data:
        return None
    return CategoryPublic.model_validate(result.data[0])


def category_get_products(category_id: UUID) -> list[dict] | None:
    if category_get(category_id) is None:
        return None
    result = (
        get_supabase().table("products").select("*")
        .eq("category_id", str(category_id)).order("created_at", desc=True).execute()
    )
    return result.data
