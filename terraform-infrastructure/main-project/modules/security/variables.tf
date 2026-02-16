# Nazwa projektu do nazywania grup bezpieczeństwa
variable "project_name" {
  type = string
}

# ID sieci VPC, w której zostaną utworzone grupy bezpieczeństwa
variable "vpc_id" {
  type = string
}

variable "environment" {
  description = "Environment name (e.g. dev, prod)"
  type        = string
}