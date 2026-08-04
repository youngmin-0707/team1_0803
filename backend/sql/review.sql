CREATE TABLE IF NOT EXISTS reviews (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL,
    customer_id UUID NOT NULL,
    rating INTEGER NOT NULL,
    content TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),

    CONSTRAINT PK_REVIEWS
        PRIMARY KEY (id),

    CONSTRAINT CK_REVIEWS_RATING
        CHECK (rating BETWEEN 1 AND 5),

    CONSTRAINT UQ_REVIEWS_PRODUCT_CUSTOMER
        UNIQUE (product_id, customer_id),

    CONSTRAINT FK_REVIEWS_PRODUCT
        FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE CASCADE,

    CONSTRAINT FK_REVIEWS_CUSTOMER
        FOREIGN KEY (customer_id)
        REFERENCES customers(id)
        ON DELETE CASCADE
);
