# main-project/modules/database/main.tf

# Grupa podsieci dla RDS - musi korzystać z podsieci prywatnych
resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-db-subnet-group"
  subnet_ids = var.private_subnet_ids

  tags = {
    Name        = "${var.project_name}-db-subnet-group"
    Environment = var.environment
  }
}

# Instancja bazy danych RDS (MySQL)
resource "aws_db_instance" "main" {
  allocated_storage      = 20
  engine                 = "mysql"
  engine_version         = "8.0"
  instance_class         = "db.t3.micro"
  db_name                = "appdb"
  username               = "admin"
  password               = "TwojeHaslo123!" # W produkcji używamy zmiennych/Secrets Manager
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [var.db_security_group_id]
  skip_final_snapshot    = true

  tags = {
    Name = "${var.project_name}-db"
  }
}