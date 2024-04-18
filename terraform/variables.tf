variable "credentials" {
  description = "Credentials"

}


variable "project" {
  description = "Project"
}

variable "region" {
  description = "Region"
}

variable "location" {
  description = "Project Location"
}

variable "bq_dataset_name" {
  description = "BigQuery Dataset Name"

}

variable "gcs_bucket_name" {
  description = "Storage Bucket Name"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

variable "events_schema" {

default="/app/events_schema.json"

}