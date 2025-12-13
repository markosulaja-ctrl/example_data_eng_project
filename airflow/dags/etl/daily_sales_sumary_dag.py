# =========================
# File: dags/daily_sales_summary_dag.py
# =========================
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta


DEFAULT_ARGS = {
"owner": "data-eng",
"depends_on_past": False,
"retries": 1,
"retry_delay": timedelta(minutes=5),
}


with DAG(
dag_id="daily_sales_summary_etl",
default_args=DEFAULT_ARGS,
description="Trigger local Python ETL to build daily_sales_summary",
schedule_interval="@daily",
start_date=datetime(2024, 1, 1),
catchup=False,
tags=["sales", "etl"],
) as dag:


    run_etl = BashOperator(
        task_id="run_daily_sales_etl",
        bash_command="python /opt/airflow/dags/etl/daily_sales_etl.py {{ ds }}",
    )


run_etl