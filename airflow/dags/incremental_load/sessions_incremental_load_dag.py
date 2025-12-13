from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

def run_incremental_load(file_name):
    """
       Call the incremental load script.
       In the test case, this is a simple Python script; in production, it would be an AWS Glue job.
    """
    subprocess.run(
        ["python3", "/opt/airflow/scripts/incremental_load.py", file_name],
        check=True
    )

with DAG(
    'sessions_incremental_load',
    default_args=default_args,
    description='Incremental load DAG for sessions.csv',
    schedule_interval='@daily',  # daily load
    start_date=datetime(2025, 1, 1),
    catchup=False
) as dag:
    
    incremental_task = PythonOperator(
        task_id='load_sessions_incremental',
        python_callable=run_incremental_load,
        # Incremental load arguments: source csv, cdc_column, primary key
        op_args=['sessions.csv', 'review_time', 'review_id']
    )
