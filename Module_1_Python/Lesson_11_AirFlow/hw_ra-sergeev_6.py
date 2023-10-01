from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from textwrap import dedent

with DAG(
        'hw_ra-sergeev_6',
        default_args={
            'depends_on_past': False,
            'email': ['airflow@example.com'],
            'email_on_failure': False,
            'email_on_retry': False,
            'retries': 1,
            'retry_delay': timedelta(minutes=5),  # timedelta из пакета datetime
        },
        description='task_6',
        schedule_interval=timedelta(days=1),
        start_date=datetime(2023, 2, 11),
        catchup=False,
        tags=['hw_ra-sergeev_6']
) as dag:
    for i in range(10):
        t1 = BashOperator(
            env={'NUMBER': i},
            task_id='bash_'+f'{i}',
            bash_command=f'echo $NUMBER'
        )
    t1
