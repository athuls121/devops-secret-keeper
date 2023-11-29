variable "project_id" {
  description = "The ID of the Google Cloud project"
  default     = "cellular-way-399223"
}

variable "credentials_file" {
  description = "Path to your GCP credentials file"
  default     = "credentials.json"
}

variable "region" {
  description = "The GCP region"
  default     = "us-central1"
}

