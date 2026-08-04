-- Supabase SQL Editor에서 실행합니다.
-- customers, products 테이블이 uuid 기준으로 먼저 있어야 합니다.

-- order_status 값은 ERD 확정 값 기준입니다. 이미 Supabase에 생성돼 있다면 이 블록은 건너뜁니다.
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'order_status') THEN
        CREATE TYPE order_status AS ENUM (
            'pending',
            'paid',
            'shipped',
            'delivered',
            'cancelled',
            'refunded',
            'returned',
            'payment_failed'
        );
    END IF;
END $$;

CREATE TABLE IF NOT EXISTS orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL REFERENCES customers (id),
    status order_status NOT NULL DEFAULT 'pending',
    shipping_address TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
    deleted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders (id),
    product_id UUID NOT NULL REFERENCES products (id),
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity >= 1),
    price INTEGER NOT NULL CHECK (price >= 0),
    created_at TIMESTAMP NOT NULL DEFAULT now()
);
