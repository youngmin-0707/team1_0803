create table public.inquiries (
  id uuid not null default gen_random_uuid (),
  product_id uuid not null,
  customer_id uuid not null,
  title text not null,
  content text not null,
  answer text null,
  answered_at timestamp without time zone null,
  created_at timestamp without time zone not null default now(),
  updated_at timestamp without time zone null,
  constraint inquiries_pkey primary key (id),
  constraint inquiries_customer_id_fkey foreign KEY (customer_id) references customers (id),
  constraint inquiries_product_id_fkey foreign KEY (product_id) references products (id)
) TABLESPACE pg_default;

create trigger trg_inquiries_updated_at BEFORE
update on inquiries for EACH row
execute FUNCTION set_updated_at ();