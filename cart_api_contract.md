# 작성자: 권오현  
# 작업 구분: port

# 회원·상품·장바구니 통합 계약

## 공통 데이터 형식

- `customers.id`, `products.id`, `carts.id`와 모든 외래키는 UUID를 사용한다.
- `price`, `stock`, `quantity`는 정수를 사용한다.
- API 응답은 `{ "success": bool, "message": str, "data": any }` 형식을 사용한다.
- 프런트엔드는 Supabase를 직접 호출하지 않고 FastAPI를 호출한다.

## 테이블 의존성과 SQL 실행 순서

1. `customers`
2. `categories`
3. `products`
4. `carts`

`products.category_id` 외래키는 카테고리 담당 SQL에서 적용한다.

## Customer API

| 방식 | 경로 | 기능 |
|---|---|---|
| POST | `/customers` | 회원 등록 |
| GET | `/customers` | 회원 목록 조회 |
| GET | `/customers/{customer_id}` | 회원 상세 조회 |
| PATCH | `/customers/{customer_id}` | 회원 수정 |
| DELETE | `/customers/{customer_id}` | 회원 삭제 |

회원 등록 요청:

```json
{
  "name": "권오현",
  "pwd": "password123"
}
```

- 회원 UUID는 DB에서 자동 생성한다.
- 비밀번호는 공통 PBKDF2 함수로 해시하고 API 응답에 포함하지 않는다.
- 실제 로그인 방식은 팀 인증 합의 후 연결한다.

## Product API

| 방식 | 경로 | 기능 |
|---|---|---|
| POST | `/products` | 상품 등록 |
| GET | `/products` | 상품 목록 조회 |
| GET | `/products/{product_id}` | 상품 상세 조회 |
| PATCH | `/products/{product_id}` | 상품 수정 |
| DELETE | `/products/{product_id}` | 상품 삭제 |

상품 등록 요청:

```json
{
  "name": "기본 티셔츠",
  "price": 15000,
  "stock": 100,
  "category_id": null
}
```

- `price`와 `stock`은 0 이상이다.
- `category_id`는 카테고리가 없으면 `null`을 허용한다.
- 판매 상태 컬럼은 팀 ERD 확정 후 추가한다.

## Cart API

장바구니 요청은 임시로 `X-Customer-Id` 헤더에 회원 UUID를 전달한다.

| 방식 | 경로 | 기능 |
|---|---|---|
| POST | `/cart/items` | 상품 추가 |
| GET | `/cart` | 장바구니 조회 |
| PATCH | `/cart/items/{cart_id}` | 수량 변경 |
| DELETE | `/cart/items/{cart_id}` | 개별 삭제 |
| POST | `/cart/items/delete-selected` | 선택 삭제 |
| DELETE | `/cart` | 전체 삭제 |
| POST | `/cart/order-selection` | 주문 전달 데이터 준비 |

장바구니 추가 요청:

```json
{
  "product_id": "상품 UUID",
  "quantity": 2
}
```

## 팀원별 연결 사항

### 회원·인증 담당

- 로그인 성공 후 `customers.id` UUID를 유지한다.
- 장바구니의 테스트 헤더를 실제 인증 의존성으로 교체한다.

### 상품 담당

- 상품 응답에 `id`, `name`, `price`, `stock`을 포함한다.
- 상품 ID는 UUID를 사용한다.

### 카테고리 담당

- `products.category_id`가 `categories.id` UUID를 참조하도록 FK를 적용한다.

### 주문 담당

- 주문 전달 데이터의 `customer_id`, `cart_id`, `product_id`는 UUID이다.
- 주문 성공 후 전달받은 `cart_id` 항목을 삭제한다.

## 미확정 항목

- 실제 로그인과 회원 UUID 연결 방식
- 상품 판매 중지 상태 컬럼
- 상품·회원 삭제 시 FK 정책
- 주문 성공 후 장바구니 삭제 책임과 API 형식
