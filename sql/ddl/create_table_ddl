-- ===========================
-- customers
-- ===========================
CREATE TABLE customers (
    customer_id       INT PRIMARY KEY,
    name              TEXT NOT NULL,
    email             TEXT,
    country           VARCHAR(2),
    age               INT,
    signup_date       DATE,
    marketing_opt_in  BOOLEAN
);

-- ===========================
-- sessions
-- ===========================
CREATE TABLE sessions (
    session_id   INT PRIMARY KEY,
    customer_id  INT,
    start_time   TIMESTAMPTZ,
    device       TEXT,
    source       TEXT,
    country      VARCHAR(2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- ===========================
-- events
-- ===========================
CREATE TABLE events (
    event_id       INT PRIMARY KEY,
    session_id     INT,
    timestamp      TIMESTAMPTZ,
    event_type     TEXT,
    product_id     NUMERIC,
    qty            NUMERIC,
    cart_size      NUMERIC,
    payment        NUMERIC,
    discount_pct   NUMERIC,
    amount_usd     NUMERIC,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);

-- ===========================
-- products
-- ===========================
CREATE TABLE products (
    product_id   INT PRIMARY KEY,
    category     TEXT,
    name         TEXT,
    price_usd    NUMERIC(12,2),
    cost_usd     NUMERIC(12,2),
    margin_usd   NUMERIC(12,2)
);

-- ===========================
-- orders
-- ===========================
CREATE TABLE orders (
    order_id        INT PRIMARY KEY,
    customer_id     INT,
    order_time      TIMESTAMPTZ,
    payment_method  TEXT,
    discount_pct    NUMERIC,
    subtotal_usd    NUMERIC(12,2),
    total_usd       NUMERIC(12,2),
    country         VARCHAR(2),
    device          TEXT,
    source          TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- ===========================
-- order_items
-- ===========================
CREATE TABLE order_items (
    order_id        INT,
    product_id      INT,
    unit_price_usd  NUMERIC(12,2),
    quantity        NUMERIC,
    line_total_usd  NUMERIC(12,2),
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- ===========================
-- reviews
-- ===========================
CREATE TABLE reviews (
    review_id     INT PRIMARY KEY,
    order_id      INT,
    product_id    INT,
    rating        INT,
    review_text   TEXT,
    review_time   TIMESTAMPTZ,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
