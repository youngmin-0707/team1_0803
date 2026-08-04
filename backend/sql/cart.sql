-- 작성자: 권오현
-- 작업 구분: port

-- Supabase SQL Editor에서 실행합니다.
-- 테이블과 컬럼은 팀 ERD의 carts 정의를 기준으로 합니다.
-- 실제 실행 전 customers.id와 products.id가 UUID인지 확인해야 합니다.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS carts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL,
    product_id UUID NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity >= 1),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_carts_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(id),

    CONSTRAINT fk_carts_product
        FOREIGN KEY (product_id)
        REFERENCES products(id),

    CONSTRAINT uq_carts_customer_product
        UNIQUE (customer_id, product_id)
);

CREATE INDEX IF NOT EXISTS idx_carts_customer_id
    ON carts(customer_id);

CREATE INDEX IF NOT EXISTS idx_carts_product_id
    ON carts(product_id);

-- TODO:
-- 상품 삭제 시 carts를 유지할지, 함께 삭제할지는 팀의 FK 정책이
-- 확정된 후 ON DELETE 옵션으로 반영합니다.
