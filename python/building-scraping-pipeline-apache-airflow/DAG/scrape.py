from datetime import timedelta

import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import ShortCircuitOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': True,
    'retries': 2,
    'retry_delay': timedelta(hours=3),
}
with DAG(
        'scrape',
        default_args=default_args,
        schedule_interval='* * * * *',
        description='Scrape the website',
        start_date=pendulum.datetime(2022, 5, 1, tz='UTC'),
        dagrun_timeout=timedelta(minutes=1),
        tags=['scrape', 'oxylabs', 'push', 'pull'],
        catchup=False
) as dag:
    trigger_always = ShortCircuitOperator(
        task_id='always',
        python_callable=lambda prev_start_date_success: prev_start_date_success is not None,
        provide_context=True,
        dag=dag
    )

    trigger_once = ShortCircuitOperator(
        task_id='once',
        python_callable=lambda prev_start_date_success: prev_start_date_success is None,
        provide_context=True,
        dag=dag
    )

    setup_task = BashOperator(
        task_id='setup',
        bash_command='python /opt/airflow/src/setup.py',
    )

    trigger_once.set_downstream(setup_task)
def is_midnight(logical_date):
        return logical_date.hour == 0 and logical_date.minute == 0

    trigger_once_per_day = ShortCircuitOperator(
        task_id='once_per_day',
        python_callable=is_midnight,
        provide_context=True,
        dag=dag
    )

    task_push = BashOperator(
        task_id='push',
        bash_command='python /opt/airflow/src/pusher.py',
    )
    trigger_once_per_day.set_downstream(task_push)

    task_pull = BashOperator(
        task_id='pull',
        bash_command='python /opt/airflow/src/puller.py'
    )

    trigger_always.set_downstream(task_pull)
    trigger_always.set_downstream(trigger_once_per_day)
