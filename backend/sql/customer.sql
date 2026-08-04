-- 팀 ERD 기준 customers 테이블입니다. Supabase SQL Editor에서 실행합니다.
CREATE TABLE IF NOT EXISTS customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pwd TEXT NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
    CONSTRAINT customers_name_not_blank CHECK (btrim(name) <> '')
);

-- 기존 테이블에 누락된 시간 컬럼을 보완합니다.
ALTER TABLE customers
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NOT NULL DEFAULT now(),
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP NOT NULL DEFAULT now();

-- 기존 id가 TEXT인 환경은 carts/orders/reviews/inquiries 외래키와 함께
-- UUID로 마이그레이션해야 하므로 운영 데이터 백업 후 별도 적용합니다.
