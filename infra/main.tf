provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_bigquery_dataset" "weather_ds" {
  dataset_id    = var.dataset_id
  friendly_name = "Weather Data Production"
  location      = var.region
}

resource "google_bigquery_table" "daily_weather" {
  dataset_id = google_bigquery_dataset.weather_ds.dataset_id
  table_id   = var.table_id
  deletion_protection = false

  schema = <<EOF
[
  {
    "name": "date",
    "type": "DATE",
    "mode": "REQUIRED"
  },
  {
    "name": "avg_temperature_celsius",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "precipitation_mm",
    "type": "FLOAT",
    "mode": "NULLABLE"
  },
  {
    "name": "max_windspeed_kmh",
    "type": "FLOAT",
    "mode": "NULLABLE"
  }
]
EOF
}