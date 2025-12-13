import sys
import pandas as pd
from sqlalchemy import create_engine, text

# =========================================================
# Configuration
# =========================================================
PROCESS_DATE = sys.argv[1]  # YYYY-MM-DD from Airflow {{ ds }}
DATA_DIR = "../csv/"        # Local path for testing

TABLE_NAME = "daily_sales_summary"

POSTGRES_CONN_STR = (
    "postgresql+psycopg2://admin:admin123@localhost:5432/postgres"
)

# =========================================================
# 1. Load datasets
# =========================================================
customers = pd.read_csv(DATA_DIR + "customers.csv")
orders = pd.read_csv(DATA_DIR + "orders.csv", parse_dates=["order_time"])
order_items = pd.read_csv(DATA_DIR + "order_items.csv")
products = pd.read_csv(DATA_DIR + "products.csv")

# =========================================================
# 2. Handle late-arriving data (reprocess last 3 days)
# =========================================================
process_date = pd.to_datetime(PROCESS_DATE)
window_start = process_date - pd.Timedelta(days=3)

orders = orders[orders["order_time"].dt.date >= window_start.date()]

# =========================================================
# 3. Deduplicate orders (latest order_time per order_id)
# =========================================================
orders = (
    orders.sort_values("order_time")
    .drop_duplicates(subset=["order_id"], keep="last")
)

# =========================================================
# 4. Enrich with order items
# =========================================================
order_fact = orders.merge(order_items, on="order_id", how="left")

# =========================================================
# 5. Enrich with products
# =========================================================
order_fact = order_fact.merge(products, on="product_id", how="left")

# =========================================================
# 6. Enrich with customers
# =========================================================
order_fact = order_fact.merge(customers, on="customer_id", how="left")

# =========================================================
# 7. Build daily_sales_summary
# =========================================================
order_fact["order_date"] = order_fact["order_time"].dt.date

summary = (
    order_fact
    .groupby(["order_date", "country_y", "category"], dropna=False)
    .agg(
        total_orders=("order_id", "nunique"),
        total_quantity=("quantity", "sum"),
        gross_revenue_usd=("line_total_usd", "sum"),
        avg_order_value_usd=("total_usd", "mean"),
    )
    .reset_index()
)

# Rename country column for clarity
summary = summary.rename(columns={"country_y": "country"})

# =========================================================
# 8. Write output to Postgres (idempotent)
# =========================================================
engine = create_engine(POSTGRES_CONN_STR)

CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    order_date DATE NOT NULL,
    country TEXT,
    category TEXT,
    total_orders INTEGER,
    total_quantity INTEGER,
    gross_revenue_usd NUMERIC,
    avg_order_value_usd NUMERIC
);
"""

processed_dates = summary["order_date"].unique().tolist()

with engine.begin() as conn:
    # Create table if it doesn't exist
    conn.execute(text(CREATE_TABLE_SQL))

    # Delete existing records for processed dates
    conn.execute(
        text(f"""
            DELETE FROM {TABLE_NAME}
            WHERE order_date = ANY(:processed_dates)
        """),
        {"processed_dates": processed_dates}
    )

# Insert fresh data
summary.to_sql(
    TABLE_NAME,
    engine,
    if_exists="append",
    index=False,
    method="multi",
)

print(f"Daily sales summary successfully upserted into '{TABLE_NAME}'")
