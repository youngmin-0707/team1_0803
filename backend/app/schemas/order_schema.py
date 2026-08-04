# order_schema.py

from datetime import datetime

from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    product_id: str
    quantity: int = Field(ge=1, examples=[2])


class OrderCreate(BaseModel):
    customer_id: str
    shipping_address: str = Field(min_length=1, examples=["서울시 강남구 테헤란로 1"])
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderItemPublic(BaseModel):
    id: str
    order_id: str
    product_id: str
    product_name: str
    quantity: int
    price: int
    created_at: datetime


class OrderPublic(BaseModel):
    id: str
    customer_id: str
    status: str
    shipping_address: str
    created_at: datetime
    updated_at: datetime


class OrderDetailPublic(OrderPublic):
    items: list[OrderItemPublic]
    total_amount: int


class OrderStatusUpdate(BaseModel):
    status: str = Field(min_length=1, examples=["paid"])
