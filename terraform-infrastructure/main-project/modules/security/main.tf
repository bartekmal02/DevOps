# Grupa bezpieczeństwa dla serwerów webowych
resource "aws_security_group" "web_sg" {
  name        = "${var.project_name}-web-sg"
  description = "Allow HTTP and SSH traffic"
  vpc_id      = var.vpc_id # Pobierane z modułu networking

  # Ruch przychodzący: HTTP
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Dostęp publiczny
  }

  # Ruch przychodzący: SSH (tylko do administracji)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # W produkcji warto tu wpisać tylko swoje IP
  }

  # Ruch wychodzący: Pozwól na wszystko
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}