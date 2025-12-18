# Environment
environment = "dev"
aws_region = "ap-south-2"

# Networking
vpc_cidr = "10.0.0.0/16"

public_subnets = [
  "10.0.1.0/24",
  "10.0.2.0/24"
]

private_subnets = [
  "10.0.101.0/24",
  "10.0.102.0/24"
]

# ECS
ecs_cluster_name = "workforce360-cluster"
ecs_service_name = "workforce360-service"
desired_count = 1

container_port = 8000
cpu    = 256
memory = 1024

# App
app_name = "workforce360"
image_tag = "latest"
