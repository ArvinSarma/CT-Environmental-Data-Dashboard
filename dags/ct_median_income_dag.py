from datetime import datetime, timedelta
from airflow.decorators import dag, task

# Assuming your modules are inside the ct_data package under ct_median_income
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
    description='ETL pipeline for extracting CT median income data',
    schedule='@daily',  # Runs once every day at midnightHere are the two Airflow DAGs built using the exact pattern from your `ct_towns_dag.py` example. 

I've set up the imports based on a standard module structure, assuming you've split your ingestion and transformation scripts into separate files just like in your towns pipeline. You may need to tweak the exact import paths (`from ct_data.XYZ import ...`) to match your project's folder structure.

### `ct_median_income_dag.py`

This DAG wires up the POST request script that downloads the ArcGIS replica[cite: 1] to the pandas transformation script that loads the data into `ct_towns_median_income`[cite: 2]. 

*Note: Your `load_median_income` function doesn't currently return a row count[cite: 2], so the DAG task just executes it without returning a variable.*

```python
from datetime import datetime, timedelta
from airflow.decorators import dag, task

# Adjust these imports to match your actual file names in the ct_data module
from ct_data.ct_median_income import median_income_ingestion
from ct_data.ct_median_income import median_income_transformation

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
        # Calls extract_data() from source 1
        filename = median_income_ingestion.extract_data(filepath) 
        print(f"Extracted data to: {filename}")
        return filename  # Automatically passed to the next task via XCom

    # 2. Transform Task
    @task()
    def transform(filename):
        """Processing/transforming and loading data into PostgreSQL."""
        # Calls load_median_income() from source 2
        median_income_transformation.load_median_income(filename)
        print("Transformed and loaded median income data successfully.")

    # Define the task dependencies by passing data downstream
    file_name = extract()
    transform(file_name)

# Call the pipeline function to register the DAG with Airflow
median_income_etl_pipeline()