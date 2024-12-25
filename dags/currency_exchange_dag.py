from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 12, 25),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'etl_pipeline',
    default_args=default_args,
    description='Currency exchange pipeline',
    schedule_interval=timedelta(days=1),  # Run once per day
) as dag:

    # Task to run the ETL script
    run_etl = BashOperator(
        task_id='run_currency_exchange_etl',
        bash_command='python /opt/airflow/dags/currency_exchange_etl.py',
    )

