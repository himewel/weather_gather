terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.5.0"
    }
  }
  required_version = ">= 0.14.3"
}

provider "google" {
  credentials = file(var.CREDENTIALS_FILEPATH)
  project     = var.PROJECT_ID
}
