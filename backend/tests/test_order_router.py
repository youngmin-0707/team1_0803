from datetime import datetime

from fastapi.testclient import TestClient

from app.main import app
from app.routers import order_router
from app.schemas.order_schema import OrderDetailPublic, OrderItemPublic, OrderPublic

client = TestClient(app)


def make_order_item(order_id: str = "order-1") -> OrderItemPublic:
    return OrderItemPublic(
        id="item-1",
        order_id=order_id,
        product_id="product-1",
        product_name="바지",
        quantity=2,
        price=10000,
        created_at=datetime.fromisoformat("2026-08-04T10:30:00+09:00"),
    )


def make_order_detail(order_id: str = "order-1") -> OrderDetailPublic:
    item = make_order_item(order_id)
    return OrderDetailPublic(
        id=order_id,
        customer_id="customer-1",
        status="pending",
        shipping_address="서울시 강남구",
        created_at=datetime.fromisoformat("2026-08-04T10:30:00+09:00"),
        updated_at=datetime.fromisoformat("2026-08-04T10:30:00+09:00"),
        items=[item],
        total_amount=20000,
    )


def make_order(order_id: str = "order-1") -> OrderPublic:
    return OrderPublic(
        id=order_id,
        customer_id="customer-1",
        status="pending",
        shipping_address="서울시 강남구",
        created_at=datetime.fromisoformat("2026-08-04T10:30:00+09:00"),
        updated_at=datetime.fromisoformat("2026-08-04T10:30:00+09:00"),
    )


def test_create_order_returns_created_order(monkeypatch):
    monkeypatch.setattr(order_router, "order_create", lambda order: make_order_detail())

    response = client.post(
        "/order/create",
        json={
            "customer_id": "customer-1",
            "shipping_address": "서울시 강남구",
            "items": [{"product_id": "product-1", "quantity": 2}],
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["id"] == "order-1"
    assert response.json()["data"]["total_amount"] == 20000


def test_get_order_returns_404_when_missing(monkeypatch):
    monkeypatch.setattr(order_router, "order_get", lambda order_id: None)

    response = client.get("/order/get/missing-order")

    assert response.status_code == 404
    assert response.json()["detail"] == "주문 ID missing-order를 찾을 수 없습니다."


def test_get_order_returns_order_detail(monkeypatch):
    monkeypatch.setattr(order_router, "order_get", lambda order_id: make_order_detail(order_id))

    response = client.get("/order/get/order-1")

    assert response.status_code == 200
    assert response.json()["data"]["items"][0]["product_id"] == "product-1"


def test_get_all_orders_returns_order_list(monkeypatch):
    monkeypatch.setattr(
        order_router,
        "order_get_all",
        lambda customer_id: [make_order("order-1"), make_order("order-2")],
    )

    response = client.get("/order/list/customer-1")

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert len(response.json()["data"]) == 2
