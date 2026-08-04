from fastapi import FastAPI
from app.routers.product_router import product_router
from app.routers.auth_router import auth_router
from app.routers.category_router import category_router
from app.routers.order_router import order_router
from app.routers.review_router import review_router

# Swagger 문서(/docs)
tags_metadata = [
    {
        "name": "Auth",
        "description": "Sign up, in, out",
    },
    {
        "name": "Product",
        "description": "Supabase에 저장된 상품을 생성·조회·수정·삭제합니다.",
    },
    {
        "name": "Category",
        "description": "카테고리와 카테고리별 상품을 관리합니다.",
    },
    {
        "name": "Order",
        "description": "주문을 생성하고 주문 내역을 조회합니다.",
    },
    {
        "name": "Review",
        "description": "상품 리뷰를 작성·조회·수정·삭제합니다.",
    },
]

app = FastAPI(title="Main App", openapi_tags=tags_metadata)

app.include_router(product_router)
app.include_router(auth_router)
app.include_router(category_router)
app.include_router(order_router)
app.include_router(review_router)
