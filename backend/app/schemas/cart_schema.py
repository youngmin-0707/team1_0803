from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class CartCreate(BaseModel):
    product_id: UUID
    quantity: int = Field(ge=1, examples=[1])


class CartQuantityUpdate(BaseModel):
    quantity: int = Field(ge=1, examples=[2])


class CartSelectedRequest(BaseModel):
    cart_ids: list[UUID] = Field(min_length=1)

    @field_validator("cart_ids")
    @classmethod
    def remove_duplicate_cart_ids(cls, cart_ids: list[UUID]) -> list[UUID]:
        return list(dict.fromkeys(cart_ids))


class CartItemPublic(BaseModel):
    id: UUID
    customer_id: UUID
    product_id: UUID
    product_name: str | None = None
    price: int | None = None
    stock: int | None = None
    quantity: int
    subtotal: int = 0
    available: bool
    availability_message: str | None = None
    created_at: datetime
    updated_at: datetime


class CartSummary(BaseModel):
    items: list[CartItemPublic]
    total_quantity: int
    total_price: int


class CartOrderItem(BaseModel):
    cart_id: UUID
    product_id: UUID
    product_name: str
    quantity: int
    price: int
    subtotal: int


class CartOrderSelection(BaseModel):
    customer_id: UUID
    items: list[CartOrderItem]
    total_price: int
