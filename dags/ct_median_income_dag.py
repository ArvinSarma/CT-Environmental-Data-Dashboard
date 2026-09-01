from datetime import datetime, timedelta
from airflow.decorators import dag, task

# Adjust these imports to match your actual file names in the ct_data module
from ct_data.ct_median_income import ct_median_income_ingestion
from ct_data.ct_median_income import ct_median_income_transformation

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
    dag_id='ct_median_income_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for extracting CT median household income data',
    schedule='@daily',  # Runs once every day at midnight
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['example', 'etl', 'median_income'],
)
def median_income_etl_pipeline():

    # 1. Extract Task
    @task()
    def extract():
        """Extracting median income data from ArcGIS feature server."""
        filepath = "/opt/airflow/shared_data/ct_data"
        filename = ct_median_income_ingestion.extract_data(filepath) 
        print(f"Extracted data to: {filename}")
        return filename  # Automatically passed to the next task via XCom

    # 2. Transform Task
    @task()
    def transform(filename):
        """Processing/transforming and loading data into PostgreSQL."""
        ct_median_income_transformation.load_median_income(filename)
        print("Transformed and loaded median income data successfully.")

    # Define the task dependencies by passing data downstream
    file_name = extract()
    transform(file_name)

# Call the pipeline function to register the DAG with Airflow
median_income_etl_pipeline()