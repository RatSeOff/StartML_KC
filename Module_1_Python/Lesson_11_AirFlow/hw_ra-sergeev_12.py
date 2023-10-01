from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator


with DAG(
        'hw_ra-sergeev_12_var',
        default_args={
            'depends_on_past': False,
            'email': ['airflow@example.com'],
            'email_on_failure': False,
            'email_on_retry': False,
            'retries': 1,
            'retry_delay': timedelta(minutes=5),  # timedelta из пакета datetime
        },
        description='task_12',
        schedule_interval=timedelta(days=1),
        start_date=datetime(2023, 9, 17),
        catchup=False,
        tags=['hw_ra-sergeev_12_var']
) as dag:
    def return_string():
        from airflow.models import Variable
        print(Variable.get("is_startml"))
        return Variable.get("is_startml")

    t1 = PythonOperator(
        task_id='string_returner',
        python_callable=return_string
    )

    t1
