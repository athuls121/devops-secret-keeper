provider "google" {
  credentials = file("credentials.json")
  project     = "cellular-way-399223"
  region      = "us-central1"
}

# Check if Redis instance exists
data "google_redis_instance" "existing_redis_instance" {
  name = "redis"
}

resource "google_redis_instance" "example" {
  count           = try(length(data.google_redis_instance.existing_redis_instance), 0)
  name            = "redis-instance-name"  # Provide a name
  memory_size_gb  = 1                      # Provide memory size
  # ... other required configuration
}

# Check if GKE cluster exists
data "google_container_cluster" "existing_gke_cluster" {
  name     = "gcp-devops-project-clust"
  location = "us-central1"
}

resource "google_container_cluster" "primary" {
  count     = try(length(data.google_container_cluster.existing_gke_cluster), 0)
  name      = "gke-cluster-name"  # Provide a name
  # ... other required configuration
}
