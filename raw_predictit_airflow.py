import requests
import boto3
import airflow
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
import datetime
import json

# Set start date
start_date = airflow.utils.dates.days_ago(2)  # 2 days ago

# Default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=5),
}

# Python function to scrape the JSON and upload directly to S3
def json_scraper(url, bucket, file_name):
    print('Starting JSON scraper')

    try:
        # Make the request with a timeout
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        
        # Get the JSON data
        json_data = response.json()

        # Convert JSON to string for direct S3 upload
        json_string = json.dumps(json_data, ensure_ascii=False, indent=4)

        # Upload the JSON string to S3 without saving locally
        s3 = boto3.client('s3')
        s3.put_object(Bucket=bucket, Key=f"predictit/{file_name}", Body=json_string)

        print('Upload to S3 complete')

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
    except boto3.exceptions.Boto3Error as e:
        print(f"Error during S3 upload: {e}")

# Define the DAG
with DAG(
    "raw_predictit_airflow",
    default_args=default_args,
    description="A DAG to scrape PredictIt data and upload to S3",
    schedule_interval=datetime.timedelta(days=1),
    start_date=start_date,
    catchup=False,
    tags=["sdg"],
) as dag:

    # Task to run the Python function
    extract_predictit = PythonOperator(
        task_id='extract_predictit',
        python_callable=json_scraper,
        op_kwargs={
            'url': 'https://www.predictit.org/api/marketdata/all/',
            'file_name': 'predictit_markets.json',
            'bucket': "gmr-s3-bucket"  # Updated bucket name
        },
    )

    # Dummy task for readiness check
    ready = DummyOperator(task_id='ready')

    # Task dependency
    extract_predictit >> ready
