from datetime import datetime
from uuid import UUID

from fastapi.testclient import TestClient

from app.main import app
from app.routers import category_router
from app.schemas.category_schema import CategoryPublic
from app.services.category_service import CategoryAlreadyExistsError, CategoryInUseError


client = TestClient(app)
CATEGORY_ID = UUID("11111111-1111-1111-1111-111111111111")


def make_category(name: str = "의류") -> CategoryPublic:
    timestamp = datetime.fromisoformat("2026-08-04T10:00:00+09:00")
    return CategoryPublic(
        id=CATEGORY_ID,
        name=name,
        created_at=timestamp,
        updated_at=timestamp,
    )


def test_create_category(monkeypatch):
    monkeypatch.setattr(category_router, "category_create", lambda category: make_category(category.name))
    response = client.post("/categories", json={"name": " 의류 "})

    assert response.status_code == 201
    assert response.json()["data"]["name"] == "의류"


def test_create_category_rejects_duplicate(monkeypatch):
    def duplicate(_category):
        raise CategoryAlreadyExistsError

    monkeypatch.setattr(category_router, "category_create", duplicate)
    response = client.post("/categories", json={"name": "의류"})

    assert response.status_code == 409
    assert response.json()["detail"] == "이미 등록된 카테고리 이름입니다."


def test_get_all_categories(monkeypatch):
    monkeypatch.setattr(category_router, "category_get_all", lambda: [make_category()])
    response = client.get("/categories")

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1


def test_get_missing_category(monkeypatch):
    monkeypatch.setattr(category_router, "category_get", lambda category_id: None)
    response = client.get(f"/categories/{CATEGORY_ID}")

    assert response.status_code == 404


def test_update_category(monkeypatch):
    monkeypatch.setattr(
        category_router,
        "category_update",
        lambda category_id, category: make_category(category.name),
    )
    response = client.put(f"/categories/{CATEGORY_ID}", json={"name": "신발"})

    assert response.status_code == 200
    assert response.json()["data"]["name"] == "신발"


def test_delete_category_rejects_category_with_products(monkeypatch):
    def in_use(_category_id):
        raise CategoryInUseError

    monkeypatch.setattr(category_router, "category_delete", in_use)
    response = client.delete(f"/categories/{CATEGORY_ID}")

    assert response.status_code == 409
    assert "삭제할 수 없습니다" in response.json()["detail"]


def test_get_products_by_category(monkeypatch):
    monkeypatch.setattr(
        category_router,
        "category_get_products",
        lambda category_id: [{"id": "product-1", "name": "티셔츠"}],
    )
    response = client.get(f"/categories/{CATEGORY_ID}/products")

    assert response.status_code == 200
    assert response.json()["data"][0]["name"] == "티셔츠"


def test_category_name_cannot_be_blank():
    response = client.post("/categories", json={"name": "   "})
    assert response.status_code == 422
