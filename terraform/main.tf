provider "google" {
  credentials = file("credentials.json")
  project     = "cellular-way-399223"
  region      = "us-central1"
}

# Check if Redis instance exists
data "google_redis_instance" "existing_redis_instance" {
  name = "redis"
}

# Conditionally create Redis instance if it doesn't exist
resource "google_redis_instance" "example" {
  count               = length(data.google_redis_instance.existing_redis_instance) > 0 ? 0 : 1
  name                = "redis"
  tier                = "BASIC"
  memory_size_gb      = 1
  authorized_network  = "projects/cellular-way-399223/global/networks/default"
}

# Check if GKE cluster exists
data "google_container_cluster" "existing_gke_cluster" {
  name     = "gcp-devops-project-clust"
  location = "us-central1"
}

# Conditionally create GKE cluster if it doesn't exist
resource "google_container_cluster" "primary" {
  count               = length(data.google_container_cluster.existing_gke_cluster) > 0 ? 0 : 1
  name                = "gcp-devops-project-clust"
  location            = "us-central1"
  deletion_protection = false
  
  network             = "default"
  subnetwork          = "default"
  enable_autopilot    = true
}
