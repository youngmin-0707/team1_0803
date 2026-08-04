# 쇼핑몰 프로젝트 계획서

<details>
<summary><strong>1. 프로젝트 개요</strong></summary>

- Streamlit, FastAPI, Supabase를 이용해 쇼핑몰 서비스를 구현한다.
- 기존 회원가입, 로그인, 상품 기능을 기반으로 카테고리, 상품 리뷰, 상품 문의, 장바구니, 주문 기능을 추가한다.
- 프런트엔드에서 Supabase를 직접 호출하지 않고 FastAPI를 통해 데이터를 처리한다.

</details>

<details>
<summary><strong>2. 팀 ERD</strong></summary>

- ERD Cloud: https://www.erdcloud.com/d/Kmq3jGGpWcrm8LWyi
- ERD 및 Supabase 테이블 관리자: 윤기화
- 테이블명, 컬럼명, 데이터 타입, PK 및 FK 관계는 팀 ERD를 기준으로 한다.
- 테이블 구조 변경이 필요하면 팀장과 먼저 협의한다.
- ERD가 변경되면 Supabase 테이블과 이 문서를 함께 업데이트한다.

### 테이블 및 컬럼

| 테이블 | 컬럼 | 주요 관계 및 용도 |
|---|---|---|
| `customers` | `id uuid`, `pwd text`, `name text`, `updated_at timestamp`, `created_at timestamp` | 회원 정보 |
| `categories` | `id uuid`, `name text`, `updated_at timestamp`, `created_at timestamp` | 상품 카테고리 |
| `products` | `id uuid`, `name text`, `price integer`, `stock integer`, `category_id uuid`, `created_at timestamp`, `updated_at timestamp` | `category_id`로 카테고리 참조 |
| `carts` | `id uuid`, `customer_id uuid`, `product_id uuid`, `quantity integer`, `created_at timestamp`, `updated_at timestamp` | 회원과 상품을 참조하는 장바구니 항목 |
| `orders` | `id uuid`, `customer_id uuid`, `status order_status`, `shipping_address text`, `created_at timestamp`, `updated_at timestamp`, `deleted_at timestamp` | 회원을 참조하는 주문 대표 정보 |
| `order_items` | `id uuid`, `order_id uuid`, `product_id uuid`, `product_name text`, `quantity integer`, `price integer`, `created_at timestamp` | 주문과 상품을 참조하는 주문 상세 항목 |
| `reviews` | `id uuid`, `product_id uuid`, `customer_id uuid`, `rating integer`, `content text`, `created_at timestamp`, `updated_at timestamp` | 회원이 상품에 작성한 리뷰 |
| `inquiries` | `id uuid`, `product_id uuid`, `customer_id uuid`, `title text`, `content text`, `answer text`, `answered_at timestamp`, `created_at timestamp`, `updated_at timestamp` | 회원이 상품에 작성한 문의와 답변 |

### 테이블 관계

- `categories` 1 : N `products`
- `customers` 1 : N `carts`
- `products` 1 : N `carts`
- `customers` 1 : N `orders`
- `orders` 1 : N `order_items`
- `products` 1 : N `order_items`
- `customers` 1 : N `reviews`
- `products` 1 : N `reviews`
- `customers` 1 : N `inquiries`
- `products` 1 : N `inquiries`

### ERD 적용 시 주의사항

- 주요 테이블의 ID와 외래키는 `uuid` 타입을 사용한다.
- 상품 재고는 `products.stock`에 저장한다.
- 주문 상태는 ERD에 정의된 `order_status` 타입을 사용하며 실제 상태 값은 Supabase 생성 스크립트를 기준으로 한다.
- 주문 당시 상품명과 가격은 `order_items.product_name`, `order_items.price`에 별도로 저장한다.
- 주문 삭제 또는 취소 처리 시 `orders.deleted_at` 사용 여부를 주문 담당자와 확정한다.
- 문의 답변 여부는 별도 상태 컬럼이 아니라 `answer`와 `answered_at`을 기준으로 판단한다.

</details>

<details>
<summary><strong>3. 기능 역할 분담</strong></summary>

| 담당자 | 담당 기능 | 난이도 | 주요 구현 내용 |
|---|---|---:|---|
| 윤기화(팀장) | 주문 | 상 | 주문 생성, 주문 상품 저장, 주문 내역 조회, 주문 상태 관리, 주문 취소, 재고 차감 및 복원 |
| 손영민 | 상품 리뷰 | 중 | 리뷰 CRUD, 별점, 평균 별점, 작성자 확인, 중복 리뷰 방지 |
| 김인혜 | 상품 문의 | 중 | 문의 CRUD, 작성자 확인, 문의 답변, 답변 상태 관리 |
| 장상옥 | 카테고리 | 하~중 | 카테고리 CRUD, 상품 연결, 카테고리별 상품 조회, 삭제 제한 |
| 권오현 | 장바구니 | 중상 | 상품 담기, 수량 변경, 상품 삭제, 총금액 계산, 재고 확인, 주문 연동 |

</details>

<details>
<summary><strong>4. 공통 작업 담당</strong></summary>

| 공통 작업 | 담당자 | 주요 업무 |
|---|---|---|
| ERD 스키마 및 테이블 생성 | 윤기화 | ERD 작성, Supabase 테이블 생성, 테이블 관계와 컬럼 변경 관리 |
| 코드 통합 및 충돌 해결 | 윤기화 | Pull Request 확인, `develop` 병합, 충돌 발생 시 해당 기능 담당자와 해결 |
| 프로젝트 Git 초기 세팅 및 사용 안내 | 손영민 | 저장소 초기 설정, 공통 브랜치와 `.gitignore` 설정, Git 작업 방법 공유 |
| `plan.md`, 디렉터리·코딩 규칙 및 API 명세 취합 | 장상옥 | 계획서 작성, 디렉터리와 코딩 규칙 관리, 기능별 API 명세 취합 |
| 협업 도구 초대 및 통합 테스트 환경 관리 | 권오현 | Notion·ERD Cloud·Supabase 초대, 접근 권한 확인, 공통 실행 환경 점검 |
| 테스트 체크리스트 및 오류 관리 | 김인혜 | 공통 테스트 체크리스트 작성, 테스트 결과 취합, 발견된 오류와 수정 상태 관리 |
| 기능별 테스트 | 각 기능 담당자 | 담당 기능의 정상 입력, 예외 상황 및 권한 테스트 |
| 최종 통합 테스트 | 전체 팀원 | 전체 기능 연결, 페이지 이동 및 데이터 흐름 테스트 |

### 공통 업무 배정 기준

- 주문과 ERD를 담당하는 윤기화는 전체 데이터 관계를 파악하므로 코드 통합과 충돌 해결도 함께 담당한다.
- 손영민은 Git 저장소와 공통 브랜치를 처음 설정하고 팀원에게 Git 사용 방법을 안내한다.
- 실제 Pull Request 확인, `develop` 병합 및 충돌 해결은 윤기화가 담당한다.
- 카테고리는 다른 기능보다 구현 범위가 작으므로 장상옥이 프로젝트 문서, 디렉터리·코딩 규칙 및 API 명세를 함께 관리한다.
- 권오현은 팀원들이 동일한 환경에서 통합 테스트를 실행할 수 있도록 접근 권한과 실행 환경을 관리한다.
- 김인혜는 공통 테스트 항목, 테스트 결과 및 발견된 오류의 수정 여부를 관리한다.
- 각 팀원은 자신이 작성한 API 명세를 장상옥에게 전달하고, 테스트 결과와 오류 내용을 김인혜에게 전달한다.

</details>

<details>
<summary><strong>5. 담당자별 기능 범위</strong></summary>

### 윤기화 — 주문

- 주문 생성
- 주문 상품 저장
- 주문 목록 및 상세 조회
- `order_items.price * order_items.quantity` 합계로 주문 총금액 계산
- 주문 당시 상품명과 가격을 `order_items`에 저장
- 주문 상태 관리
- 주문 취소
- 주문 시 재고 차감
- 주문 취소 시 재고 복원
- 주문 완료 후 해당 장바구니 상품 삭제
- 실제 결제 API와 배송 추적 기능은 이번 범위에서 제외

### 손영민 — 상품 리뷰

- 상품별 리뷰 목록 조회
- 리뷰 작성, 수정 및 삭제
- 1점부터 5점까지 별점 등록
- 상품 평균 별점과 리뷰 개수 표시
- 작성자 본인만 수정 및 삭제 가능
- 동일 회원의 동일 상품 중복 리뷰 방지
- 리뷰 작성일 표시

### 김인혜 — 상품 문의

- 상품별 문의 목록 및 상세 조회
- 문의 작성, 수정 및 삭제
- 작성자 본인만 수정 및 삭제 가능
- 문의 답변 등록 및 수정
- 답변 전, 답변 완료 상태 표시
- 문의 작성일 표시

#### 공통 업무

- 기능별 공통 테스트 체크리스트 작성
- 팀원별 테스트 결과 취합
- 발견된 오류 목록 작성
- 오류 담당자와 수정 예정 상태 기록
- 수정 완료 후 재테스트 여부 확인
- 최종 통합 테스트 결과 정리

### 장상옥 — 카테고리

- 카테고리 등록, 목록 조회, 상세 조회, 수정 및 삭제
- 카테고리 이름 중복 방지
- 상품과 카테고리 연결
- 카테고리별 상품 목록 조회
- 상품이 연결된 카테고리의 삭제 제한
- 관리자용 카테고리 관리 화면
- 사용자용 카테고리 선택 및 상품 조회 화면

#### 공통 업무

- `plan.md` 작성 및 업데이트
- 프로젝트 디렉터리 구조 관리
- 파일명, 함수명 및 코딩 규칙 관리
- 팀원별 API 명세 양식 공유
- 각 담당자가 작성한 API 명세 취합
- ERD 또는 개발 규칙 변경 내용을 문서에 반영

### 권오현 — 장바구니

- 장바구니에 상품 추가
- 로그인 회원의 장바구니 조회
- 동일 상품을 다시 담으면 기존 수량 증가
- 장바구니 상품 수량 변경
- 개별, 선택 및 전체 상품 삭제
- 상품별 금액과 장바구니 총금액 계산
- 수량이 1보다 작아지는 것 방지
- 상품 재고를 초과하는 수량 제한
- 판매 중지 또는 삭제된 상품 처리
- 선택한 상품 정보를 주문 기능에 전달

#### 공통 업무

- Notion, ERD Cloud 및 Supabase 팀원 초대
- 협업 도구 접근 권한 확인
- 공통 환경 변수 설정 방법 공유
- 백엔드와 프런트엔드 실행 방법 확인
- 통합 테스트용 계정과 테스트 데이터 준비 지원
- 전체 팀원의 통합 테스트 환경 접속 여부 확인

</details>

<details>
<summary><strong>6. 프로젝트 디렉터리 구성</strong></summary>

아래 구조는 현재 프로젝트 구성을 유지하면서 담당 기능을 추가하는 기준안이다.

```text
team1_0803/
├─ plan.md
├─ backend/
│  ├─ .env
│  ├─ requirements.txt
│  ├─ README.md
│  ├─ sql/
│  │  ├─ customer.sql
│  │  ├─ product.sql
│  │  ├─ category.sql
│  │  ├─ review.sql
│  │  ├─ inquiry.sql
│  │  ├─ cart.sql
│  │  ├─ order.sql
│  │  └─ order_item.sql
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ core/
│  │  │  ├─ api_response.py
│  │  │  ├─ password.py
│  │  │  └─ supabase_client.py
│  │  ├─ routers/
│  │  │  ├─ auth_router.py
│  │  │  ├─ product_router.py
│  │  │  ├─ category_router.py
│  │  │  ├─ review_router.py
│  │  │  ├─ inquiry_router.py
│  │  │  ├─ cart_router.py
│  │  │  └─ order_router.py
│  │  ├─ schemas/
│  │  │  ├─ auth_schema.py
│  │  │  ├─ product_schema.py
│  │  │  ├─ category_schema.py
│  │  │  ├─ review_schema.py
│  │  │  ├─ inquiry_schema.py
│  │  │  ├─ cart_schema.py
│  │  │  └─ order_schema.py
│  │  └─ services/
│  │     ├─ auth_service.py
│  │     ├─ product_service.py
│  │     ├─ category_service.py
│  │     ├─ review_service.py
│  │     ├─ inquiry_service.py
│  │     ├─ cart_service.py
│  │     └─ order_service.py
│  └─ tests/
│     ├─ test_auth_router.py
│     ├─ test_product_router.py
│     ├─ test_category_router.py
│     ├─ test_review_router.py
│     ├─ test_inquiry_router.py
│     ├─ test_cart_router.py
│     └─ test_order_router.py
└─ frontend/
   ├─ app.py
   ├─ requirements.txt
   ├─ README.md
   ├─ core/
   │  ├─ __init__.py
   │  ├─ api_client.py
   │  └─ auth.py
   ├─ clients/
   │  ├─ auth_client.py
   │  ├─ product_client.py
   │  ├─ category_client.py
   │  ├─ review_client.py
   │  ├─ inquiry_client.py
   │  ├─ cart_client.py
   │  └─ order_client.py
   └─ app_pages/
      ├─ 00_login.py
      ├─ 01_home.py
      ├─ 02_signup.py
      ├─ 03_weather.py
      ├─ 04_health.py
      ├─ 07_product_management.py
      ├─ 08_mypage.py
      ├─ 09_category.py
      ├─ 10_review.py
      ├─ 11_inquiry.py
      ├─ 12_cart.py
      └─ 13_order.py
```

### 디렉터리 적용 규칙

- 위 구조는 계획안이며 빈 파일을 한꺼번에 생성하지 않는다.
- 각 담당자는 기능 개발을 시작할 때 자신의 파일만 생성한다.
- 기존 파일 이름은 다른 팀원과 협의 없이 변경하지 않는다.
- 문의 관련 파일명은 `inquiry`로 통일한다. ERD의 최종 테이블명이 다르면 팀 협의 후 함께 변경한다.
- 스키마 파일명은 `scheme`이 아닌 `schema`로 통일한다.
- 페이지 번호는 통합 시 중복되지 않도록 장상옥이 관리한다.
- `backend/app/main.py`와 `frontend/app.py`의 최종 통합은 윤기화가 담당한다.

</details>

<details>
<summary><strong>7. 공통 파일명 및 코드 규칙</strong></summary>

| 구분 | 파일명 형식 | 예시 |
|---|---|---|
| Router | `{기능}_router.py` | `category_router.py` |
| Schema | `{기능}_schema.py` | `category_schema.py` |
| Service | `{기능}_service.py` | `category_service.py` |
| Frontend Client | `{기능}_client.py` | `category_client.py` |
| Router 테스트 | `test_{기능}_router.py` | `test_category_router.py` |

- 함수명과 변수명은 `snake_case`를 사용한다.
- 클래스명은 `PascalCase`를 사용한다.
- 들여쓰기는 공백 4칸을 사용한다.
- 비즈니스 로직은 Router가 아닌 Service에 작성한다.
- 프런트엔드에서는 Supabase를 직접 호출하지 않는다.
- 프런트엔드는 Client 함수를 통해 FastAPI를 호출한다.
- API 키와 비밀번호는 코드에 직접 작성하지 않는다.
- Supabase 연결은 공통 `get_supabase()` 함수를 사용한다.
- 각 담당자는 자신이 구현한 API 명세와 테스트 결과를 작성한다.

</details>

<details>
<summary><strong>8. Git 작업 규칙</strong></summary>

### 브랜치

- `main`: 최종 완료 및 배포용 코드
- `develop`: 기능 통합 및 테스트용 코드
- `feature/order`: 주문
- `feature/review`: 상품 리뷰
- `feature/inquiry`: 상품 문의
- `feature/category`: 카테고리
- `feature/cart`: 장바구니

### 작업 순서

1. 작업 시작 전 `develop` 브랜치의 최신 코드를 받는다.
2. 담당 기능 브랜치에서 작업한다.
3. 하나의 기능 단위로 커밋한다.
4. 작업 완료 후 Pull Request를 생성한다.
5. 윤기화가 Pull Request와 실행 여부를 확인한다.
6. 문제가 없으면 `develop` 브랜치에 병합한다.
7. 충돌이 발생하면 윤기화와 해당 기능 담당자가 함께 해결한다.
8. 전체 테스트 완료 후 `main` 브랜치에 병합한다.

### 커밋 메시지

- `feat`: 새로운 기능 추가
- `fix`: 오류 수정
- `docs`: 문서 수정
- `refactor`: 코드 구조 개선
- `test`: 테스트 추가 및 수정
- `style`: 코드 형식 수정

예시:

```text
feat: 카테고리 등록 기능 구현
fix: 주문 총금액 계산 오류 수정
docs: 상품 문의 API 명세 추가
test: 장바구니 수량 변경 테스트 추가
```

</details>

<details>
<summary><strong>9. 기능 개발 순서</strong></summary>

1. 윤기화가 ERD와 Supabase 테이블을 확정하고 공유한다.
2. 각 담당자가 자신의 테이블명, 컬럼, PK 및 FK를 확인한다.
3. 각 기능의 Schema, Service, Router를 구현한다.
4. 각 기능의 Frontend Client와 Streamlit 화면을 구현한다.
5. 담당자가 정상 입력, 예외 상황 및 권한을 테스트한다.
6. Pull Request를 생성하고 윤기화가 `develop`에 통합한다.
7. 전체 팀원이 최종 통합 테스트를 진행하고 김인혜가 결과와 오류 수정 여부를 정리한다.

</details>

<details>
<summary><strong>10. 기능 완료 조건</strong></summary>

- [ ] ERD와 동일한 테이블명 및 컬럼명을 사용했다.
- [ ] Backend Schema, Service, Router를 구현했다.
- [ ] Frontend Client와 Streamlit 화면을 구현했다.
- [ ] Supabase와 정상적으로 연결된다.
- [ ] 담당 기능의 등록, 조회, 수정 및 삭제가 정상 작동한다.
- [ ] 잘못된 입력과 존재하지 않는 데이터의 오류를 처리한다.
- [ ] 본인 데이터에 대한 수정 및 삭제 권한을 확인한다.
- [ ] API 명세와 테스트 결과를 작성했다.
- [ ] `develop` 브랜치에서 다른 기능과 함께 정상 실행된다.

</details>
