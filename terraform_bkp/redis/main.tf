provider "google" {
  credentials = file("path/to/your/credentials.json")
  project     = var.project_id
  region      = "us-central1"  # Replace with your desired region
}

resource "google_redis_instance" "my_redis" {
  name     = "my-redis-instance"
  tier     = "BASIC"  # Adjust as needed
  location = "us-central1"  # Replace with your desired region
}
