output "ecs_service_name" {
  value = aws_ecs_service.main.name
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.main.name
}
