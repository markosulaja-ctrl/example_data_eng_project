from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

def run_full_load(file_name):
    """Call full load script"""
    subprocess.run(
        ["python3", "/opt/airflow/scripts/full_load.py", file_name],
        check=True
    )

with DAG(
    'order_items_full_load',
    default_args=default_args,
    description='full load DAG for order_items.csv',
    schedule_interval=None,  # Run manually
    start_date=datetime(2025, 1, 1),
    catchup=False
) as dag:
    
    load_task = PythonOperator(
        task_id='load_order_items_full',
        python_callable=run_full_load,
        op_args=['order_items.csv']
    )
