provider "google" {
  credentials = file("path/to/your/credentials.json")
  project     = "your-project-id"
  region      = "us-central1"  # Replace with your desired region
}

module "gke" {
  source     = "./gke"
  project_id = var.project_id
}

module "redis" {
  source     = "./redis"
  project_id = var.project_id
}

