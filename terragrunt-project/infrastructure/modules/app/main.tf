# Zmienne
variable "vpc_id" {
  type        = string
  description = "ID sieci pobrane z modułu VPC przez dependency"
}

variable "name" {
  type        = string
  description = "Nazwa z pliku env.hcl"
}

# Tworzymy prosty zasób (Security Group)
resource "aws_security_group" "app_sg" {
  name        = "${var.name}-sg"
  description = "Security group dla aplikacji w sieci ${var.vpc_id}"
  vpc_id      = var.vpc_id

  tags = {
    Name = "${var.name}-sg"
  }
}