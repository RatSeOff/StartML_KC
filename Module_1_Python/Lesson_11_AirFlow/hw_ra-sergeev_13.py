from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator,  BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.models import Variable

def get_decision():
    if Variable.get("is_startml") == "True":
        return "startml_desc"
    else:
        return "not_startml_desc"


def get_info_startml():
    print("StartML is a starter course for ambitious people")


def get_info_not_startml():
    print("Not a startML course, sorry")

with DAG(
        'hw_ra-sergeev_13_fin',
        default_args={
            'depends_on_past': False,
            'email': ['airflow@example.com'],
            'email_on_failure': False,
            'email_on_retry': False,
            'retries': 1,
            'retry_delay': timedelta(minutes=5),  # timedelta из пакета datetime
        },
        description='task_13',
        schedule_interval=timedelta(days=1),
        start_date=datetime(2023, 9, 17),
        catchup=False,
        tags=['hw_ra-sergeev_13_fin']
) as dag:
    t1 = DummyOperator(
        task_id='dummy_start'
    )
    t2 = BranchPythonOperator(
        task_id='get_decision',
        python_callable=get_decision
    )
    t3 = PythonOperator(
        task_id='startml_desc',
        python_callable=get_info_startml
    )
    t4 = PythonOperator(
        task_id='not_startml_desc',
        python_callable=get_info_not_startml
    )
    t5 = DummyOperator(
        task_id='dummy_finish'
    )

    t1 >> t2 >> [t3, t4] >> t5
