from airflow.sdk import dag
from airflow.providers.standard.operators.bash import BashOperator
from pendulum import datetime
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from datetime import timedelta

PROJECT = "/usr/local/airflow/project"   # where the container sees my code (from the mount file)


@dag(
    schedule="0 14 * * *",                               # every day at 14:00
    start_date=datetime(2026, 11, 1, tz="Europe/Berlin"),  # German time
    catchup=False,
    default_args={
        "retries": 3,                                    # try again up to 3 times
        "retry_delay": timedelta(minutes=5),             # wait 5 min between tries
    },
    tags=["strompreis"],
)
def strompreis_daily():
    download = BashOperator(
        task_id="download",
        bash_command=f"cd {PROJECT} && python ingestion/smard_download.py",
    )
    upload = BashOperator(
        task_id="upload",
        bash_command=f"cd {PROJECT} && python ingestion/upload_to_volume.py",
    )
    auto_loader = DatabricksRunNowOperator(
        task_id="auto_loader",
        job_id=921991820198534,
    )
    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=(
            f"cd {PROJECT}/dbt/strompreis_radar && "
            "/usr/local/airflow/dbt_venv/bin/dbt build --profiles-dir ."
        ),
    )

    download >> upload >> auto_loader >> dbt_build



strompreis_daily()
