from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.bash import BashOperator

# ------------------------------------------------------------------
# PATH CONFIGURATION
# Set absolute paths relative to the project root directory
# ------------------------------------------------------------------
DAGS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(DAGS_DIR)

# Virtual Environment Python Binary Path
# (If on Linux/macOS/WSL use 'bin/python', if on native Windows use 'Scripts/python.exe')
PYTHON_EXEC = os.path.join(PROJECT_ROOT, "venv", "bin", "python")

# Target Python script paths matching your exact src/ directory tree
INGEST_TOWNS = os.path.join(PROJECT_ROOT, "src", "ct_towns", "ct_towns_ingestion.py")
TRANSFORM_TOWNS = os.path.join(PROJECT_ROOT, "src", "ct_towns", "ct_towns_transformation.py")

INGEST_INCOME = os.path.join(PROJECT_ROOT, "src", "ct_median_income", "ct_median_income_ingestion.py")
TRANSFORM_INCOME = os.path.join(PROJECT_ROOT, "src", "ct_median_income", "ct_median_income_transformation.py")

INGEST_HAZARDOUS = os.path.join(PROJECT_ROOT, "src", "ct_hazardous_waste", "ct_hazardous_waste_ingestion.py")
TRANSFORM_HAZARDOUS = os.path.join(PROJECT_ROOT, "src", "ct_hazardous_waste", "ct_hazardous_waste_transformation.py")


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="ct_data_pipeline",
    default_args=default_args,
    description="Automated ETL pipeline for CT Towns, Median Income, and Hazardous Waste datasets",
    schedule_interval="@daily",  # Adjust schedule: @hourly, @daily, @weekly, or custom cron
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["ct_data", "etl", "postgresql"],
) as dag:

    # ------------------------------------------------------------------
    # INGESTION TASKS
    # ------------------------------------------------------------------
    task_ingest_towns = BashOperator(
        task_id="ingest_ct_towns",
        bash_command=f'"{PYTHON_EXEC}" "{INGEST_TOWNS}"',
    )

    task_ingest_income = BashOperator(
        task_id="ingest_ct_median_income",
        bash_command=f'"{PYTHON_EXEC}" "{INGEST_INCOME}"',
    )

    task_ingest_hazardous = BashOperator(
        task_id="ingest_ct_hazardous_waste",
        bash_command=f'"{PYTHON_EXEC}" "{INGEST_HAZARDOUS}"',
    )

    # ------------------------------------------------------------------
    # TRANSFORMATION TASKS
    # ------------------------------------------------------------------
    task_transform_towns = BashOperator(
        task_id="transform_ct_towns",
        bash_command=f'"{PYTHON_EXEC}" "{TRANSFORM_TOWNS}"',
    )

    task_transform_income = BashOperator(
        task_id="transform_ct_median_income",
        bash_command=f'"{PYTHON_EXEC}" "{TRANSFORM_INCOME}"',
    )

    task_transform_hazardous = BashOperator(
        task_id="transform_ct_hazardous_waste",
        bash_command=f'"{PYTHON_EXEC}" "{TRANSFORM_HAZARDOUS}"',
    )

    # ------------------------------------------------------------------
    # EXECUTION DEPENDENCIES
    # 1. All 3 ingestion scripts run in parallel.
    # 2. Once all ingestions complete, transformations run sequentially
    #    to preserve foreign key dependencies (Towns -> Income & Hazardous).
    # ------------------------------------------------------------------
    [task_ingest_towns, task_ingest_income, task_ingest_hazardous] >> task_transform_towns
    task_transform_towns >> [task_transform_income, task_transform_hazardous]