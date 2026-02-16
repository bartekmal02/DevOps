# Definicja dostawcy chmury i regionu operacyjnego
provider "aws" {
  region = "eu-central-1"
}

# Tworzy unikalny identyfikator, aby nazwa bucketu S3 była niepowtarzalna
resource "random_id" "suffix" {
  byte_length = 4
}

# Tworzy bucket S3 do przechowywania pliku stanu terraform.tfstate
resource "aws_s3_bucket" "terraform_state" {
  bucket = "terraform-state-web-app-${random_id.suffix.hex}"
}

# Włącza wersjonowanie pliku stanu, co pozwala na powrót do poprzedniej konfiguracji (rollback) [cite: 787, 1668]
resource "aws_s3_bucket_versioning" "state_ver" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Szyfruje plik stanu za pomocą algorytmu AES256 dla ochrony danych wrażliwych [cite: 786, 1674]
resource "aws_s3_bucket_server_side_encryption_configuration" "state_enc" {
  bucket = aws_s3_bucket.terraform_state.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Tworzy tabelę DynamoDB służącą do blokowania stanu (Locking)
# Zapobiega to jednoczesnej edycji infrastruktury przez dwie osoby [cite: 785, 1692]
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-state-locks"
  billing_mode = "PAY_PER_REQUEST" # Opłaty tylko za faktyczne użycie (brak stałego kosztu)
  hash_key     = "LockID"         # Wymagany atrybut dla mechanizmu blokady Terraform [cite: 1695]

  attribute {
    name = "LockID"
    type = "S"
  }
}

# Wyświetla nazwę stworzonego bucketu po zakończeniu operacji
output "s3_bucket_name" {
  value = aws_s3_bucket.terraform_state.bucket
}