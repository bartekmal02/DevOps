# main-project/variables.tf

variable "aws_region" {
  description = "Region AWS, w którym powstanie infrastruktura"
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Nazwa projektu używana do nazywania wszystkich zasobów"
  type        = string
}

variable "vpc_cidr" {
  description = "Główny zakres adresów IP dla sieci VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "environment" {
  description = "Environment name (e.g. dev, prod)"
  type        = string
}