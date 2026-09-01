from datetime import datetime, timedelta
from airflow.decorators import dag, task
from ct_data.ct_towns import ct_towns_ingestion
from ct_data.ct_towns import ct_towns_transformation

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Instantiate the DAG using the @dag decorator
@dag(
    dag_id='ct_towns_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for extracting CT towns data',
    schedule='@daily',  # Runs once every day at midnight
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['example', 'etl'],
)
def etl_pipeline():

    # 1. Extract Task
    @task()
    def extract():
        """extracting data from a source for all CT towns."""
        filepath="/opt/airflow/shared_data/ct_data"
        filename= ct_towns_ingestion.extract_data(filepath)
        print(f"Extracted data to : {filename}")
        return filename  # Automatically passed to the next task via XCom

    # 2. Transform Task
    @task()
    def transform(filename):
        """processing/transforming and loading data intop database for CT towns."""
        data_cnt = ct_towns_transformation.load_towns(filename)
        print(f"Transformed data (doubled values): {data_cnt}")
        return data_cnt

    # Define the task dependencies by passing data downstream
    file_name=extract()
    data_cnt=transform(file_name)

# Call the pipeline function to register the DAG with Airflow
etl_pipeline()