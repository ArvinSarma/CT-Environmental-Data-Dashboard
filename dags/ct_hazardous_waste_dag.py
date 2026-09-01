from datetime import datetime, timedelta
from airflow.decorators import dag, task

# Adjust these imports to match your actual file names in the ct_data module
from ct_data.ct_hazardous_waste import ct_hazardous_waste_ingestion
from ct_data.ct_hazardous_waste import ct_hazardous_waste_transformation

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
    dag_id='ct_hazardous_waste_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for extracting CT hazardous waste data',
    schedule='@daily',  # Runs once every day at midnight
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['example', 'etl', 'hazardous_waste'],
)
def hazardous_waste_etl_pipeline():

    # 1. Extract Task
    @task()
    def extract():
        """Extracting hazardous waste data from source."""
        filepath = "/opt/airflow/shared_data/ct_data"
        # Calls extract_data() from source 3
        filename = ct_hazardous_waste_ingestion.extract_data(filepath)
        print(f"Extracted data to: {filename}")
        return filename  # Automatically passed to the next task via XCom

    # 2. Transform Task
    @task()
    def transform(filename):
        """Processing/transforming and loading data into database for CT hazardous waste."""
        # Calls load_hazardous_data() from source 4
        data_cnt = ct_hazardous_waste_transformation.load_hazardous_data(filename)
        print(f"Transformed data (records inserted): {data_cnt}")
        return data_cnt

    # Define the task dependencies by passing data downstream
    file_name = extract()
    data_cnt = transform(file_name)

# Call the pipeline function to register the DAG with Airflow
hazardous_waste_etl_pipeline()