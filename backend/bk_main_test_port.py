"""장바구니 API만 독립적으로 실행하기 위한 로컬 테스트 앱입니다.

실행 위치: backend 폴더
실행 명령: uvicorn bk_main_test_port:app --reload --port 8001
API 문서: http://127.0.0.1:8001/docs
"""

from fastapi import FastAPI

from app.routers.cart_router import cart_router


app = FastAPI(
    title="Cart Test API",
    description="기존 main.py와 분리된 장바구니 기능 확인용 API입니다.",
)
app.include_router(cart_router)
