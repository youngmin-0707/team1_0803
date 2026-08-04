-- Supabase SQL Editor에서 실행합니다.
-- 테이블이 이미 존재한다면 CREATE TABLE 구문은 생략하고 INSERT 구문만 실행하세요.

CREATE TABLE IF NOT EXISTS customers (
    id TEXT PRIMARY KEY,
    pwd TEXT NOT NULL,
    name TEXT NOT NULL
);
