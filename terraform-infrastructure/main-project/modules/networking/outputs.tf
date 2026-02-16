# Przekazuje ID utworzonego VPC do innych modułów
output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.main.id
}

# Przekazuje listę ID publicznych podsieci (dla Load Balancera lub EC2)
output "public_subnet_ids" {
  description = "List of IDs of public subnets"
  value       = aws_subnet.public[*].id
}

# Przekazuje listę ID prywatnych podsieci (dla RDS lub serwerów aplikacji)
output "private_subnet_ids" {
  description = "List of IDs of private subnets"
  value       = aws_subnet.private[*].id
}