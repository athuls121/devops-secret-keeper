output "cluster_name" {
  value = google_container_cluster.my_cluster.name
}

output "cluster_endpoint" {
  value = google_container_cluster.my_cluster.endpoint
}
