-- ============================================
-- DIMENSIONS
-- ============================================

-- 1. Date Dimension
CREATE TABLE dim_date (
    date_key      INT PRIMARY KEY,      -- YYYYMMDD
    date_value    DATE NOT NULL,
    year          INT,
    quarter       INT,
    month         INT,
    day           INT,
    day_of_week   INT,
    is_weekend    BOOLEAN
);

-- 2. Customer Dimension
CREATE TABLE dim_customer (
    customer_key      SERIAL PRIMARY KEY,
    customer_id       INT UNIQUE,
    name              TEXT,
    email             TEXT,
    country           VARCHAR(2),
    signup_date       DATE,
    marketing_opt_in  BOOLEAN,
    age               INT
);

-- 3. Product Dimension
CREATE TABLE dim_product (
    product_key   SERIAL PRIMARY KEY,
    product_id    INT UNIQUE,
    name          TEXT,
    category      TEXT,
    price_usd     NUMERIC(12,2),
    cost_usd      NUMERIC(12,2),
    margin_usd    NUMERIC(12,2)
);

-- 4. Country Dimension (Optional but useful)
CREATE TABLE dim_country (
    country_key   SERIAL PRIMARY KEY,
    country_code  VARCHAR(2) UNIQUE,
    country_name  TEXT,
    region        TEXT
);

-- 5. Session Dimension (Optional)
CREATE TABLE dim_session (
    session_key   SERIAL PRIMARY KEY,
    session_id    INT UNIQUE,
    customer_id   INT,
    start_time    TIMESTAMPTZ,
    device        TEXT,
    source        TEXT,
    country       VARCHAR(2)
);

-- ============================================
-- FACT TABLES
-- ============================================

-- 6. Fact Orders
CREATE TABLE fact_orders (
    order_key        SERIAL PRIMARY KEY,
    order_id         INT UNIQUE,
    customer_key     INT REFERENCES dim_customer(customer_key),
    date_key         INT REFERENCES dim_date(date_key),
    country_key      INT REFERENCES dim_country(country_key),
    order_time       TIMESTAMPTZ,
    payment_method   TEXT,
    discount_pct     NUMERIC,
    subtotal_usd     NUMERIC(12,2),
    total_usd        NUMERIC(12,2),
    device           TEXT,
    source           TEXT
);

-- 7. Fact Order Items
CREATE TABLE fact_order_items (
    order_item_key    SERIAL PRIMARY KEY,
    order_key         INT REFERENCES fact_orders(order_key),
    product_key       INT REFERENCES dim_product(product_key),
    date_key          INT REFERENCES dim_date(date_key),
    unit_price_usd    NUMERIC(12,2),
    quantity          NUMERIC,
    line_total_usd    NUMERIC(12,2)
);

-- 8. Fact Events (optional)
CREATE TABLE fact_events (
    event_key      SERIAL PRIMARY KEY,
    session_key    INT REFERENCES dim_session(session_key),
    product_key    INT REFERENCES dim_product(product_key),
    date_key       INT REFERENCES dim_date(date_key),
    event_type     TEXT,
    qty            NUMERIC,
    cart_size      NUMERIC,
    payment        NUMERIC,
    discount_pct   NUMERIC,
    amount_usd     NUMERIC
);
