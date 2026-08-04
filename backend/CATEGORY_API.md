# 카테고리 API 명세

기본 응답은 `{"success": true, "message": "...", "data": ...}` 형식이다.

| Method | Path | 요청 본문 | 설명 |
|---|---|---|---|
| `POST` | `/categories` | `{"name": "의류"}` | 카테고리 등록 |
| `GET` | `/categories` | 없음 | 카테고리 목록 조회 |
| `GET` | `/categories/{category_id}` | 없음 | 카테고리 상세 조회 |
| `PUT` | `/categories/{category_id}` | `{"name": "신발"}` | 카테고리 수정 |
| `DELETE` | `/categories/{category_id}` | 없음 | 카테고리 삭제 |
| `GET` | `/categories/{category_id}/products` | 없음 | 카테고리에 연결된 상품 조회 |

## 오류 응답

- `404`: 해당 카테고리가 존재하지 않음
- `409`: 카테고리 이름 중복 또는 연결 상품이 있어 삭제할 수 없음
- `422`: 빈 이름, 50자 초과 이름 또는 잘못된 UUID

## 상품 연결

상품 등록·수정 요청의 `category_id`에 카테고리 UUID를 전달한다. 카테고리를 지정하지 않을 때는 `null` 또는 필드 생략이 가능하다.

## DB 적용

Supabase SQL Editor에서 `sql/category.sql`을 한 번 실행해 `categories` 테이블과 `products.category_id` 외래키를 생성한다.
