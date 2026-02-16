# Konfiguruje Terraform tak, aby zamiast pliku lokalnego używał zdalnego bucketu S3 [cite: 769, 1748]
terraform {
  backend "s3" {
    bucket         = "bartek-storage-lab-2026"
    key            = "infrastructure/terraform.tfstate" # Lokalizacja pliku wewnątrz S3
    region         = "eu-central-1"
    encrypt        = true
    dynamodb_table = "terraform-state-locks" # Aktywuje blokowanie przez DynamoDB [cite: 780, 1762]
  }
}