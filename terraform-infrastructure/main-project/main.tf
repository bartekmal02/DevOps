# Wywołanie modułu networking
module "networking" {
  source       = "./modules/networking"
  
  project_name = var.project_name
  vpc_cidr     = var.vpc_cidr
  environment  = var.environment # Zmienione na var, aby lapało z tfvars
}

# Wywołanie modułu security
module "security" {
  source       = "./modules/security"
  
  project_name = var.project_name
  vpc_id       = module.networking.vpc_id 
  environment  = var.environment
}

# NOWY BLOK: Wywołanie modułu bazy danych
module "database" {
  source = "./modules/database"

  project_name         = var.project_name
  environment          = var.environment
  
  # Pobieramy ID podsieci prywatnych z outputu modułu networking
  private_subnet_ids   = module.networking.private_subnet_ids
  
  # Pobieramy ID grupy bezpieczeństwa z outputu modułu security
  db_security_group_id = module.security.web_sg_id
}

module "compute" {
  source = "./modules/compute"

  project_name      = var.project_name
  environment       = var.environment
  public_subnet_ids = module.networking.public_subnet_ids
  web_sg_id         = module.security.web_sg_id # Używamy tego samego SG co wcześniej
}