provider "google" {
  credentials = file("credentials.json")
  project     = "cellular-way-399223"
  region      = "us-central1"
}

# Redis DB
resource "google_redis_instance" "example" {
  name                = "redis"
  tier                = "BASIC"  
  memory_size_gb      = 1             
  authorized_network  = "projects/cellular-way-399223/global/networks/default"  
}

# GKE cluster
resource "google_container_cluster" "primary" {
  name     = "gcp-devops-project-clust"
  location = var.region       #Takes region value from variables.tf
  deletion_protection = false  # Disable deletion protection
 
  network    = "default"
  subnetwork = "default"
 
# Enabling Autopilot for this cluster
  enable_autopilot = true
}

#resource "kubernetes_namespace" "example" {
#  metadata {
#    name = "gcp-devops-prod"
#  }
#}