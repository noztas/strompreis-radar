from airflow.sdk import dag
from airflow.providers.standard.operators.bash import BashOperator
from pendulum import datetime
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator

PROJECT = "/usr/local/airflow/project"   # where the container sees my code (from the mount file)


@dag(
    schedule=None,                        # no schedule yet: only runs when I click Trigger
    start_date=datetime(2026, 11, 1),
    catchup=False,                        # don't run for past days automatically
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
