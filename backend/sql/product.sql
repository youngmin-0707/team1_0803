-- 팀 ERD 기준 products 테이블입니다. Supabase SQL Editor에서 실행합니다.
CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    price INTEGER NOT NULL CHECK (price >= 0),
    stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    category_id UUID,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
    CONSTRAINT products_name_not_blank CHECK (btrim(name) <> '')
);

-- 기존 테이블에 누락된 ERD 컬럼을 보완합니다.
ALTER TABLE products
    ADD COLUMN IF NOT EXISTS stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    ADD COLUMN IF NOT EXISTS category_id UUID,
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP NOT NULL DEFAULT now();

-- category_id 외래키는 categories 생성 후 category.sql에서 적용합니다.
-- 기존 id가 TEXT인 환경은 carts/order_items/reviews/inquiries 외래키와 함께
-- UUID로 마이그레이션해야 하므로 운영 데이터 백업 후 별도 적용합니다.

INSERT INTO products (id, name, price, stock, created_at, updated_at) VALUES
    ('10000000-0000-0000-0000-000000000001', '기본 티셔츠', 15000, 100, '2026-07-22 09:00:00+09', '2026-07-22 09:00:00+09'),
    ('10000000-0000-0000-0000-000000000002', '청바지', 45000, 50, '2026-07-22 09:05:00+09', '2026-07-22 09:05:00+09'),
    ('10000000-0000-0000-0000-000000000003', '후드 집업', 59000, 40, '2026-07-22 09:10:00+09', '2026-07-22 09:10:00+09')
ON CONFLICT (id) DO NOTHING;
