# To ID pozwoli bazie danych (RDS) przypisać do siebie reguły firewalla
output "web_sg_id" {
  description = "ID grupy bezpieczenstwa dla bazy danych"
  value       = aws_security_group.web_sg.id 
}