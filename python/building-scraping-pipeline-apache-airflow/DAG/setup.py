from datetime import timedelta

import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(hours=3),
}
with DAG(
        'setup',
        default_args=default_args,
        schedule_interval='@once',
        description='Setup',
        start_date=pendulum.datetime(2022, 5, 1, tz='UTC'),
        dagrun_timeout=timedelta(minutes=1),
        tags=['scrape', 'database'],
        catchup=False
) as dag:
    setup_task = BashOperator(
        task_id='setup',
        bash_command='python /opt/airflow/src/setup.py',
    )