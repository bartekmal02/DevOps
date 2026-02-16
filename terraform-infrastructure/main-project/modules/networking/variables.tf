# Definicja zmiennej dla regionu
variable "aws_region" {
  type    = string
  default = "eu-central-1"
}

# Definicja zmiennej dla nazwy projektu
variable "project_name" {
  type    = string
}

# Definicja zakresu IP dla sieci
variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "environment" {
  description = "Environment name (e.g. dev, prod)"
  type        = string
}