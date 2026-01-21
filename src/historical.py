import requests
import pandas as pd
import os
from google.cloud import bigquery
from datetime import datetime

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credential.json"

PROJECT_ID = "weather-toronto-forecast"
DATASET_ID = "weather_data_prod"
TABLE_ID = "toronto_daily_weather"
full_table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

def fetch_historical_data():
    print(" extracting historical data...")
    
    url = "https://archive-api.open-meteo.com/v1/archive"
    
    params = {
        "latitude": 43.65,
        "longitude": -79.38,
        "start_date": "2019-01-01",
        "end_date": "2026-01-20",
        "daily": "temperature_2m_mean,precipitation_sum,windspeed_10m_max",
        "timezone": "America/Toronto"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    daily_data = data['daily']
    
    df = pd.DataFrame({
        "date": daily_data['time'],
        "avg_temperature_celsius": daily_data['temperature_2m_mean'],
        "precipitation_mm": daily_data['precipitation_sum'],
        "max_windspeed_kmh": daily_data['windspeed_10m_max']
    })

    return df

def run_quality_gates(df):
    print(" data quality checks...")
    
    if df.isnull().values.any():
        raise ValueError("Data Quality Error: Null values found in the dataset.")

    if df['avg_temperature_celsius'].max() > 50 or df['avg_temperature_celsius'].min() < -50:
        raise ValueError("Data Quality Error: Unrealistic temperature detected.")

    print(" Data is clean.")
    return df

def load_to_bigquery(df):
    print(f"loading data to {full_table_id}...")
    
    client = bigquery.Client()
    
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE", 
    )

    job = client.load_table_from_dataframe(
        df, full_table_id, job_config=job_config
    )
    
    job.result()
    print(f"  loaded {job.output_rows} rows.")

if __name__ == "__main__":
    raw_df = fetch_historical_data()
    clean_df = run_quality_gates(raw_df)
    load_to_bigquery(clean_df)