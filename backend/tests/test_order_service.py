import uuid
from datetime import datetime, timezone

import pytest
from fastapi import HTTPException

from app.schemas.order_schema import OrderCreate, OrderItemCreate
from app.services import order_service


class FakeQuery:
    def __init__(self, table: "FakeTable", op: str, payload=None):
        self.table = table
        self.op = op
        self.payload = payload
        self.filters: list[tuple[str, object]] = []

    def eq(self, column, value):
        self.filters.append((column, value))
        return self

    def is_(self, column, value):
        self.filters.append((column, None if value == "null" else value))
        return self

    def order(self, *args, **kwargs):
        return self

    def _matches(self, row):
        return all(row.get(col) == val for col, val in self.filters)

    def execute(self):
        if self.op == "select":
            rows = [row for row in self.table.rows if self._matches(row)]
            return FakeResult(rows)
        if self.op == "insert":
            row = dict(self.payload)
            row.setdefault("id", str(uuid.uuid4()))
            now = datetime.now(timezone.utc).isoformat()
            row.setdefault("created_at", now)
            row.setdefault("updated_at", now)
            if self.table.name == "orders":
                row.setdefault("deleted_at", None)
            self.table.rows.append(row)
            return FakeResult([row])
        if self.op == "update":
            updated = []
            for row in self.table.rows:
                if self._matches(row):
                    row.update(self.payload)
                    updated.append(row)
            return FakeResult(updated)
        raise AssertionError(f"unsupported op {self.op}")


class FakeResult:
    def __init__(self, data):
        self.data = data


class FakeTable:
    def __init__(self, name, rows):
        self.name = name
        self.rows = rows

    def select(self, *_args, **_kwargs):
        return FakeQuery(self, "select")

    def insert(self, payload):
        return FakeQuery(self, "insert", payload)

    def update(self, payload):
        return FakeQuery(self, "update", payload)


class FakeSupabase:
    def __init__(self):
        self.data: dict[str, list[dict]] = {
            "products": [],
            "orders": [],
            "order_items": [],
        }

    def table(self, name):
        return FakeTable(name, self.data[name])


@pytest.fixture
def fake_supabase(monkeypatch):
    supabase = FakeSupabase()
    monkeypatch.setattr(order_service, "get_supabase", lambda: supabase)
    return supabase


def make_product(supabase, stock=5, price=10000, name="바지"):
    product_id = str(uuid.uuid4())
    supabase.data["products"].append(
        {"id": product_id, "name": name, "price": price, "stock": stock}
    )
    return product_id


def test_order_create_decreases_stock(fake_supabase):
    product_id = make_product(fake_supabase, stock=5)

    order = order_service.order_create(
        OrderCreate(
            customer_id=str(uuid.uuid4()),
            shipping_address="서울시 강남구",
            items=[OrderItemCreate(product_id=product_id, quantity=2)],
        )
    )

    assert order.total_amount == 20000
    product = fake_supabase.data["products"][0]
    assert product["stock"] == 3


def test_order_create_rejects_insufficient_stock(fake_supabase):
    product_id = make_product(fake_supabase, stock=1)

    with pytest.raises(HTTPException) as exc_info:
        order_service.order_create(
            OrderCreate(
                customer_id=str(uuid.uuid4()),
                shipping_address="서울시 강남구",
                items=[OrderItemCreate(product_id=product_id, quantity=2)],
            )
        )

    assert exc_info.value.status_code == 400
    assert fake_supabase.data["products"][0]["stock"] == 1


def test_order_cancel_restores_stock(fake_supabase):
    product_id = make_product(fake_supabase, stock=5)

    order = order_service.order_create(
        OrderCreate(
            customer_id=str(uuid.uuid4()),
            shipping_address="서울시 강남구",
            items=[OrderItemCreate(product_id=product_id, quantity=2)],
        )
    )
    assert fake_supabase.data["products"][0]["stock"] == 3

    order_service.order_cancel(order.id)

    assert fake_supabase.data["products"][0]["stock"] == 5
    assert fake_supabase.data["orders"][0]["status"] == "cancelled"


def test_order_cancel_rejects_shipped_order(fake_supabase):
    product_id = make_product(fake_supabase, stock=5)
    order = order_service.order_create(
        OrderCreate(
            customer_id=str(uuid.uuid4()),
            shipping_address="서울시 강남구",
            items=[OrderItemCreate(product_id=product_id, quantity=1)],
        )
    )
    order_service.order_update_status(order.id, "shipped")

    with pytest.raises(HTTPException) as exc_info:
        order_service.order_cancel(order.id)

    assert exc_info.value.status_code == 400
    assert fake_supabase.data["products"][0]["stock"] == 4
