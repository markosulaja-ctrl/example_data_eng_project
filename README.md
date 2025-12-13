Trevco Test Project
Project Overview

trevco_test is a data engineering and ETL project built using Apache Airflow, Python, and PostgreSQL. The project ingests e-commerce CSV datasets, performs full loads, incremental loads, and daily sales summary aggregations, and stores processed data in a Postgres database.

This project demonstrates a typical data pipeline architecture, including:

Full loads for initial ingestion

Incremental loads for daily updates

ETL processing for aggregating and summarizing sales data

Postgres as the target relational database

Folder Structure
trevco_test/
├── airflow/
│   └── dags/
│       ├── etl/
│       │   └── daily_sales_sumary_dag.py
│       ├── full_load/
│       │   ├── customers_full_load_dag.py
│       │   ├── events_full_load_dag.py
│       │   ├── order_items_full_load_dag.py
│       │   ├── orders_full_load_dag.py
│       │   ├── products_full_load_dag.py
│       │   ├── reviews_full_load_dag.py
│       │   └── sessions_full_load_dag.py
│       └── incremental_load/
│           ├── customers_incremental_load_dag.py
│           ├── events_incremental_load_dag.py
│           ├── orders_incremental_load_dag.py
│           ├── reviews_incremental_load_dag.py
│           └── sessions_incremental_load_dag.py
├── csv/
│   ├── customers.csv
│   ├── events.csv
│   ├── order_items.csv
│   ├── orders.csv
│   ├── products.csv
│   ├── reviews.csv
│   └── sessions.csv
├── scripts/
│   ├── daily_sales_etl.py
│   ├── full_load.py
│   └── incremental_load.py
└── sql/
    └── ddl/
        └── create_table_ddl

Data Sources

The project ingests CSV files located in the csv/ folder:

File Name	Description
customers.csv	Customer master data
sessions.csv	Session logs for customers
events.csv	Event-level activity logs per session
orders.csv	Orders placed by customers
order_items.csv	Items within each order
products.csv	Product catalog
reviews.csv	Customer product reviews
Database Schema

The database schema is defined in sql/ddl/create_table_ddl and includes the following tables:

customers

sessions (FK: customers)

events (FK: sessions)

products

orders (FK: customers)

order_items (FK: orders, products)

reviews (FK: orders, products)

Airflow DAGs
Full Load DAGs

Located in airflow/dags/full_load/, these DAGs perform initial full ingestion of CSV files into Postgres. Each DAG corresponds to a CSV file and runs manually.

Example DAGs:

customers_full_load_dag.py

orders_full_load_dag.py

products_full_load_dag.py

These DAGs call scripts/full_load.py with the target CSV file as an argument.

Incremental Load DAGs

Located in airflow/dags/incremental_load/, these DAGs perform daily incremental ingestion of new records into Postgres. Each DAG uses a PythonOperator to run scripts/incremental_load.py.

Example DAGs:

customers_incremental_load_dag.py

orders_incremental_load_dag.py

reviews_incremental_load_dag.py

Key Features:

Filters only records from the previous day

Deduplicates by primary key

Appends new records to the Postgres table

ETL DAGs

Located in airflow/dags/etl/:

daily_sales_sumary_dag.py triggers the daily aggregation ETL in scripts/daily_sales_etl.py.

Aggregates order, product, and customer data into daily_sales_summary.

Supports late-arriving data by reprocessing the last 3 days.

Scripts
Full Load Script

scripts/full_load.py:

Reads a CSV file

Loads the entire dataset into Postgres

Replaces the existing table if it exists

Incremental Load Script

scripts/incremental_load.py:

Reads a CSV file

Filters for records from the previous day based on a CDC column

Deduplicates using the primary key

Appends new records to Postgres

Daily Sales ETL

scripts/daily_sales_etl.py:

Joins orders, order_items, products, and customers

Deduplicates and handles late-arriving orders

Aggregates data by order_date, country, and category

Stores results in daily_sales_summary table

Postgres Configuration

Connection string used in scripts:

postgresql+psycopg2://admin:admin123@localhost:5432/postgres


Note: Replace credentials with your production values.

Usage

Setup Airflow and point DAGs to the airflow/dags/ folder.

Run database DDL to create necessary tables:

psql -U admin -d postgres -f sql/ddl/create_table_ddl


Trigger full load DAGs manually for the first ingestion.

Enable incremental load DAGs to run daily.

Trigger daily_sales_summary_etl DAG to build aggregated metrics.

Future Enhancements

Replace local CSV ingestion with AWS S3 or Azure Data Lake sources.

Replace Python scripts with AWS Glue or Fabric notebooks for production ETL.

Add unit tests and data quality checks in Airflow.