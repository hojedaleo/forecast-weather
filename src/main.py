import functions_framework
import requests
from google.cloud import bigquery
from datetime import datetime, timedelta
import os

PROJECT_ID = os.environ.get("GCP_PROJECT")
DATASET_ID = "weather_data_prod"
TABLE_ID = "toronto_daily_weather"
FULL_TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

@functions_framework.http
def daily_ingest(request):
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y-%m-%d')

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 43.65,
        "longitude": -79.38,
        "start_date": yesterday_str,
        "end_date": yesterday_str,
        "daily": "temperature_2m_mean,precipitation_sum,windspeed_10m_max",
        "timezone": "America/Toronto"
    }

    # Extract Data
    response = requests.get(url, params=params)
    data = response.json()
    
    # Load to BigQuery
    client = bigquery.Client()
    
    row_to_insert = [{
        "date": yesterday_str,
        "avg_temperature_celsius": data['daily']['temperature_2m_mean'][0],
        "precipitation_mm": data['daily']['precipitation_sum'][0],
        "max_windspeed_kmh": data['daily']['windspeed_10m_max'][0]
    }]

    errors = client.insert_rows_json(FULL_TABLE_ID, row_to_insert)
    
    if errors == []:
        return f"Success: Loaded data for {yesterday_str}", 200
    else:
        return f"Error: {errors}", 500