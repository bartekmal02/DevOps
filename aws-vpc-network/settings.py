# AWS Global Configuration
AWS_PROFILE = 'infra-mgr'
AWS_REGION = 'eu-central-1'

# Network Configuration
NETWORK_CONFIG = {
    'vpc_cidr': '10.0.0.0/16',
    'subnet_cidr': '10.0.1.0/24',
}

# ECS / Fargate Configuration
ECS_CLUSTER_NAME = "fargate-cluster"
ECS_SERVICE_NAME = "fargate-app-service"
ECS_TASK_FAMILY = "fargate-app-task"

# Konfiguracja kontenera
CONTAINER_NAME = "web-app"
CONTAINER_IMAGE = "public.ecr.aws/nginx/nginx:latest"
CONTAINER_PORT = 80
CPU_UNITS = "256"
MEMORY_LIMIT = "512"