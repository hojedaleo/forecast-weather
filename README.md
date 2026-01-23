Milestone 1: Infrastructure & Security
- Provisioned all GCP resources using Terraform for reproducibility.
- Defined BigQuery Datasets and Tables with strict schemas.

Milestone 2: ETL & Data Ingestion
- Ingestion strategy
- Historical Backfill (historical.py):
- Ingested 6 years of data (2019–2025).
- Data Quality: Implemented null checks and outlier detection.
- Used WRITE_TRUNCATE to ensure re-runs do not create duplicates.
- Daily Automation
- Incremental append strategy.
- Scheduled to run daily at 08:00 AM EST.

Milestone 3: Analytics & Forecasting
- Medallion Architecture: structured data into Bronze (Raw), Silver (Cleaned), and Gold (Aggregated) layers using BigQuery Views.
- Machine Learning: Trained an ARIMA_PLUS model directly in BigQuery using SQL to forecast temperature trends for the next 15 days.
- Dashboard: Built a live Looker Studio dashboard connected to the Gold layer.

dashboard: https://lookerstudio.google.com/s/tRP2RIU2aGo
