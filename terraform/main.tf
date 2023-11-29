provider "google" {
  credentials = file("credentials.json")
  project     = "cellular-way-399223"
  region      = "us-central1"
}

resource "google_redis_instance" "example" {
  name                = "redis"
  tier                = "BASIC"  
  memory_size_gb      = 1             
  authorized_network  = "projects/cellular-way-399223/global/networks/default"  
}


resource "google_container_cluster" "primary" {
  name                = "gcp-devops-project-clust"
  location            = "us-central1"
  deletion_protection = false
  
  network             = "default"
  subnetwork          = "default"
  enable_autopilot    = true
}
