import os

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from scripts import raw_parser, dw_transform, bigquery_upload


default_args = {
    "owner": "himewel",
    "start_date": "2000-01-01",
    "depends_on_past": False,
    "retries": 5,
}

with DAG(
    dag_id="weather_data_pipeline",
    schedule_interval="@yearly",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
) as dag:
    project_path = f"{os.getenv('AIRFLOW_HOME')}/dags"
    scripts_path = f"{project_path}/scripts"
    data_path = f"{project_path}/data"

    url_source = "https://portal.inmet.gov.br/uploads/dadoshistoricos/"
    bash_args = "{data_path} {url_source} {reference_year}"
    bash_args = bash_args.format(
        scripts_path=scripts_path,
        data_path=data_path,
        url_source=url_source,
        reference_year="{{ execution_date.year }}",
    )

    extract_task = BashOperator(
        task_id="extract_files",
        bash_command=f"bash {scripts_path}/extraction_script.bash {bash_args}",
    )

    raw_parser_task = PythonOperator(
        task_id="raw_parser",
        python_callable=raw_parser,
        op_kwargs={'data_path': data_path},
    )

    dw_transform_task = PythonOperator(
        task_id="dw_transform",
        python_callable=dw_transform,
        op_kwargs={'data_path': data_path},
    )

    bq_upload_task = PythonOperator(
        task_id="upload",
        python_callable=bigquery_upload,
        op_kwargs={'data_path': data_path},
    )

    extract_task >> raw_parser_task >> dw_transform_task
    dw_transform_task >> bq_upload_task
