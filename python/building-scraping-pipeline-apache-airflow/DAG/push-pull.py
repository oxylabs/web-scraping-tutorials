from datetime import timedelta

import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': True,
    'retries': 2,
    'retry_delay': timedelta(hours=3),
}
with DAG(
        'push_pull',
        default_args=default_args,
        schedule_interval='@daily',
        description='Push-Pull workflow',
        start_date=pendulum.datetime(2022, 5, 1, tz='UTC'),
        dagrun_timeout=timedelta(minutes=1),
        tags=['scrape', 'database'],
        catchup=False
) as dag:
    task_push = BashOperator(
        task_id='push',
        bash_command='python /opt/airflow/src/pusher.py',
    )

    task_pull = BashOperator(
        task_id='pull',
        bash_command='python /opt/airflow/src/puller.py'
    )

    task_push.set_downstream(task_pull)