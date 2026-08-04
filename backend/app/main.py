from fastapi import FastAPI

from app.routers.order_router import order_router

tags_metadata = [
    {
        "name": "Order",
        "description": "주문 생성, 주문 상품 저장, 주문 목록 및 상세 조회를 처리합니다.",
    },
]

app = FastAPI(title="Main App")

app.include_router(order_router)
