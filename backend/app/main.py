from fastapi import FastAPI
from app.routers.chat_router import chat_router
from app.routers.product_router import product_router
from app.routers.auth_router import auth_router
import app.core.chat_config

# Swagger 문서(/docs)
tags_metadata = [
    {
        "name": "Auth",
        "description": "Sign up, in, out",
    },
    {
        "name": "Chat",
        "description": "Gemini 모델을 사용해 사용자 메시지에 답변합니다.",
    },
    {
        "name": "Product",
        "description": "Supabase에 저장된 상품을 생성·조회·수정·삭제합니다.",
    },
]

app = FastAPI(title="Main App")

app.include_router(chat_router)
app.include_router(product_router)
app.include_router(auth_router)

