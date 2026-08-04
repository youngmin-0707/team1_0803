-- Supabase SQL Editor에서 실행합니다. 팀 ERD의 카테고리 관계를 적용합니다.
CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT categories_name_not_blank CHECK (btrim(name) <> '')
);

-- 대소문자와 앞뒤 공백을 무시하여 이름 중복을 DB에서도 방지합니다.
CREATE UNIQUE INDEX IF NOT EXISTS categories_name_unique
    ON categories (lower(btrim(name)));

ALTER TABLE products
    ADD COLUMN IF NOT EXISTS category_id UUID;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'products_category_id_fkey'
    ) THEN
        ALTER TABLE products
            ADD CONSTRAINT products_category_id_fkey
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT;
    END IF;
END $$;

CREATE INDEX IF NOT EXISTS products_category_id_idx ON products(category_id);
