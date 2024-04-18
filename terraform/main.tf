terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}

resource "google_storage_bucket" "data-lake-bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true


  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}


resource "google_bigquery_table" "table" {
 project             = var.project
 dataset_id          = var.bq_dataset_name
 table_id            = "events"
 deletion_protection = false
 depends_on = [
    google_bigquery_dataset.dataset,
  ]

 schema = file(var.events_schema)

 time_partitioning {
   type  = "DAY"
   field = "EventDate"
 }


 clustering = ["Year","Event"]

}