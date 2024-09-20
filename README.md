# PredictIt Data Scraper and Airflow DAG

This project is an ETL pipeline implemented using Apache Airflow that scrapes data from the PredictIt market and uploads the JSON data directly to an S3 bucket. The project is designed to demonstrate the following:

- **Data Engineering Skills**: Working with ETL pipelines, handling APIs, and working with AWS services (S3).
- **Apache Airflow**: Configuring and managing DAGs for scheduling, task dependencies, and error handling.

## Features

- **Daily Scraper**: Automatically pulls data from the PredictIt API every 24 hours.
- **AWS Integration**: Uploads the scraped data to Amazon S3.
- **Error Handling**: Handles request errors and AWS S3 errors gracefully with proper logging.
- **Modular Design**: Separation of data fetching and uploading tasks for easier maintainability.

## Setup Instructions

1. **Clone the repository**: `git clone https://github.com/gilbertmichaelredman/predictit_demo.git`
2. **Configure AWS Credentials**: Ensure you have access to an AWS account and configure your credentials using the AWS CLI.
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Run Airflow DAG**:
   - Start Airflow scheduler and web server.
   - Load the DAG from the Airflow UI.
   - Trigger the DAG manually or wait for the scheduled daily run.
