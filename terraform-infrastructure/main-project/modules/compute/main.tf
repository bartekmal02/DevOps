# Pobieranie najnowszego obrazu Amazon Linux 2
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# Instancja EC2
resource "aws_instance" "web" {
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = "t3.micro"
  
  # Wybieramy pierwszą z brzegu publiczną podsieć
  subnet_id     = var.public_subnet_ids[0]
  
  # Podpinamy grupę bezpieczeństwa
  vpc_security_group_ids = [var.web_sg_id]

  tags = {
    Name        = "${var.project_name}-web-server"
    Environment = var.environment
  }
}