from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

with DAG(
        'hw_ra-sergeev_11_con',
        default_args={
            'depends_on_past': False,
            'email': ['airflow@example.com'],
            'email_on_failure': False,
            'email_on_retry': False,
            'retries': 1,
            'retry_delay': timedelta(minutes=5),  # timedelta из пакета datetime
        },
        description='task_11',
        schedule_interval=timedelta(days=1),
        start_date=datetime(2023, 9, 17),
        catchup=False,
        tags=['hw_ra-sergeev_11_con']
) as dag:
    def postgre():
        postgres = PostgresHook(postgres_conn_id="startml_feed")
        with postgres.get_conn() as conn:  # вернет тот же connection, что вернул бы psycopg2.connect(...)
            with conn.cursor() as cursor:
                cursor.execut(
                    """
                        SELECT user_id, COUNT(action) AS count
                        FROM feed_action
                        WHERE action = 'like'
                        GROUP BY user_id
                        ORDER BY count DESC
                        LIMIT 1
                    """
                )
                return cursor.fetchone()

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
