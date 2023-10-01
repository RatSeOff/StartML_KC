from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG(
        'hw_ra-sergeev_10_xcom',
        default_args={
            'depends_on_past': False,
            'email': ['airflow@example.com'],
            'email_on_failure': False,
            'email_on_retry': False,
            'retries': 1,
            'retry_delay': timedelta(minutes=5),  # timedelta из пакета datetime
        },
        description='task_10',
        schedule_interval=timedelta(days=1),
        start_date=datetime(2023, 2, 11),
        catchup=False,
        tags=['hw_ra-sergeev_10_xcom']
) as dag:

    def return_string():
        return "Airflow tracks everything"

    t1 = PythonOperator(
        task_id='string_returner',
        python_callable=return_string
    )

    def xcom_pull(ti):
        result = ti.xcom_pull(
            key='return_value',
            task_ids='string_returner'
        )
        print(result)
        return result

    t2 = PythonOperator(
        task_id='xcom_pull',
        python_callable=xcom_pull
    )
    t1 >> t2
