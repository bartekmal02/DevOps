# Wyświetla publiczny adres IP serwera z modułu compute
output "web_public_ip" {
  description = "Public IP address of the web server"
  value       = module.compute.public_ip
}

# Wyświetla adres (endpoint) bazy danych z modułu database
output "db_endpoint" {
  description = "The connection endpoint for the database"
  value       = module.database.db_instance_endpoint
}