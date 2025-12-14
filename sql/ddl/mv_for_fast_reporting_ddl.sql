-- Daily Revenue
CREATE MATERIALIZED VIEW mv_daily_revenue AS
SELECT 
    d.date_value AS date,
    SUM(o.total_usd) AS daily_revenue,
    SUM(o.subtotal_usd) AS daily_subtotal,
    AVG(o.total_usd) AS avg_order_value,
    COUNT(*) AS order_count
FROM fact_orders o
JOIN dim_date d ON o.date_key = d.date_key
GROUP BY d.date_value
WITH DATA;

CREATE INDEX idx_mv_daily_revenue_date ON mv_daily_revenue(date);

-- Product Performance
CREATE MATERIALIZED VIEW mv_product_performance AS
SELECT 
    p.product_id,
    p.name AS product_name,
    p.category,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.line_total_usd) AS revenue,
    SUM(oi.quantity * p.cost_usd) AS total_cost,
    SUM(oi.line_total_usd - (oi.quantity * p.cost_usd)) AS gross_margin
FROM fact_order_items oi
JOIN dim_product p ON oi.product_key = p.product_key
GROUP BY p.product_id, p.name, p.category
WITH DATA;

CREATE INDEX idx_mv_product_performance_revenue ON mv_product_performance(revenue);

-- Customer Metrics
CREATE MATERIALIZED VIEW mv_customer_metrics AS
SELECT 
    c.customer_id,
    c.name,
    c.email,
    c.country,
    COUNT(o.order_key) AS order_count,
    SUM(o.total_usd) AS total_revenue,
    AVG(o.total_usd) AS avg_order_value,
    MIN(o.order_time) AS first_order_date,
    MAX(o.order_time) AS last_order_date
FROM fact_orders o
JOIN dim_customer c ON o.customer_key = c.customer_key
GROUP BY c.customer_id, c.name, c.email, c.country
WITH DATA;

CREATE INDEX idx_mv_customer_metrics_total_rev ON mv_customer_metrics(total_revenue);
