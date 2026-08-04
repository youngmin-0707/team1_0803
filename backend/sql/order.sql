-- Supabase SQL Editor에서 실행합니다.
-- customers, products 테이블이 먼저 있어야 합니다.
-- order_status 값(pending 외 나머지)은 팀 논의 후 확정 예정이라 CHECK 없이 TEXT로 둡니다.

CREATE TABLE IF NOT EXISTS orders (
    id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL REFERENCES customers (id),
    status TEXT NOT NULL DEFAULT 'pending',
    shipping_address TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    deleted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS order_items (
    id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL REFERENCES orders (id),
    product_id TEXT NOT NULL REFERENCES products (id),
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity >= 1),
    price INTEGER NOT NULL CHECK (price >= 0),
    created_at TIMESTAMP NOT NULL
);
