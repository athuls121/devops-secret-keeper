provider "google" {
  credentials = file("path/to/your/credentials.json")
  project     = var.project_id
  region      = "us-central1"  # Replace with your desired region
}

resource "google_container_cluster" "my_cluster" {
  name               = "my-gke-cluster"
  location           = "us-central1"  # Replace with your desired region
  initial_node_count = 1  # Adjust as needed

  node_config {
    machine_type = "n1-standard-2"  # Replace with your desired machine type
  }
}
