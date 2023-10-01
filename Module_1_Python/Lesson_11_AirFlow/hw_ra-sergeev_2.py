"""
Create BashOperator - pwd & PythonOperator - print ds
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

with DAG(
        'hw_ra-sergeev_2',
        default_args={
            'depends_on_past': False,
            'email': ['airflow@example.com'],
            'email_on_failure': False,
            'email_on_retry': False,
            'retries': 1,
            'retry_delay': timedelta(minutes=5),
        },
        description='my_first_dag',
        schedule_interval=timedelta(days=1),
        start_date=datetime(2023, 2, 11),
        catchup=False,
        tags=['hw_ra-sergeev_2']
) as dag:
    t1 = BashOperator(
        task_id='get_directory',
        bash_command='pwd'
    )


    def print_ds(ds, **kwargs):
        print(kwargs)
        print(ds)
        return f'Logic time is {ds}'


    t2 = PythonOperator(
        task_id='print_ds',
        python_callable=print_ds
    )
    t1 >> t2
