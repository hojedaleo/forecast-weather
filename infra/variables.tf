variable "project_id" {
  description = "The Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "The region for resources"
  type        = string
  default     = "northamerica-northeast1"
}

variable "dataset_id" {
  description = "The BigQuery Dataset ID"
  type        = string
  default     = "weather_data_prod"
}

variable "table_id" {
  description = "The BigQuery Table ID"
  type        = string
  default     = "toronto_daily_weather"
}