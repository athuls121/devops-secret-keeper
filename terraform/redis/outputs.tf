output "redis_name" {
  value = google_redis_instance.my_redis.name
}

output "redis_host" {
  value = google_redis_instance.my_redis.host
}
