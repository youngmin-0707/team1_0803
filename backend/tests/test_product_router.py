from datetime import datetime
from uuid import UUID

from fastapi.testclient import TestClient

from app.main import app
from app.routers import product_router
from app.schemas.product_schema import ProductPublic


client = TestClient(app)


PRODUCT_ID_1 = UUID("10000000-0000-0000-0000-000000000001")
PRODUCT_ID_2 = UUID("10000000-0000-0000-0000-000000000002")


def make_product(product_id: UUID = PRODUCT_ID_1) -> ProductPublic:
    timestamp = datetime.fromisoformat("2026-07-22T10:30:00+09:00")
    return ProductPublic(
        id=product_id,
        name="바지",
        price=10000,
        stock=10,
        created_at=timestamp,
        updated_at=timestamp,
    )


def test_create_product_returns_created_product(monkeypatch):
    monkeypatch.setattr(product_router, "product_create", lambda product: make_product())

    response = client.post(
        "/product/create",
        json={"name": "바지", "price": 10000, "stock": 10},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["id"] == str(PRODUCT_ID_1)


def test_get_product_returns_404_when_missing(monkeypatch):
    monkeypatch.setattr(product_router, "product_get", lambda product_id: None)

    response = client.get("/product/get/not-a-uuid")

    assert response.status_code == 422


def test_get_all_products_returns_product_list(monkeypatch):
    monkeypatch.setattr(
        product_router,
        "product_get_all",
        lambda: [make_product(PRODUCT_ID_1), make_product(PRODUCT_ID_2)],
    )

    response = client.get("/product/getall")

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert len(response.json()["data"]) == 2


def test_update_product_uses_path_product_id(monkeypatch):
    received = {}

    def fake_update(product_id, product):
        received["product_id"] = product_id
        received["name"] = product.name
        received["price"] = product.price
        received["stock"] = product.stock
        return make_product(product_id)

    monkeypatch.setattr(product_router, "product_update", fake_update)

    response = client.put(
        f"/product/{PRODUCT_ID_1}",
        json={"name": "청바지", "price": 20000, "stock": 20},
    )

    assert response.status_code == 200
    assert response.json()["data"]["id"] == str(PRODUCT_ID_1)
    assert received == {
        "product_id": PRODUCT_ID_1,
        "name": "청바지",
        "price": 20000,
        "stock": 20,
    }


def test_delete_product_returns_deleted_product(monkeypatch):
    monkeypatch.setattr(product_router, "product_delete", lambda product_id: make_product(product_id))

    response = client.delete(f"/product/delete/{PRODUCT_ID_1}")

    assert response.status_code == 200
    assert response.json()["data"]["id"] == str(PRODUCT_ID_1)
