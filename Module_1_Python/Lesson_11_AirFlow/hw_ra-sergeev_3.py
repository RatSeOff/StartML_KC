from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from textwrap import dedent

with DAG(
        'hw_ra-sergeev_3',
        default_args={
            'depends_on_past': False,
            'email': ['airflow@example.com'],
            'email_on_failure': False,
            'email_on_retry': False,
            'retries': 1,
            'retry_delay': timedelta(minutes=5),  # timedelta из пакета datetime
        },
        description='second_dag',
        schedule_interval=timedelta(days=1),
        start_date=datetime(2023, 2, 11),
        catchup=False,
        tags=['hw_ra-sergeev_3']
) as dag:
    for i in range(10):
        t1 = BashOperator(
            task_id='bash_'+f'{i}',
            bash_command=f'echo {i}'
        )


    def print_tasknumber(task_number, **kwargs):
        print(f'task number is: {task_number}')
        return f'task number is: {task_number}'

    for i in range(20):
        t2 = PythonOperator(
            task_id='python_'+f'{i}',
            python_callable=print_tasknumber,
            op_kwargs={'task_number': i}
        )
    t1.doc_md = dedent(
        """
        # Абзац
        `code`
        **полужирный**
        _курсив_
        """
    )
    t2.doc_md = dedent(
        """
        # Абзац
        `code`
        **полужирный**
        _курсив_
        """
    )
    t1 >> t2
