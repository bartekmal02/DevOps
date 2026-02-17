include "root" {
  path = find_in_parent_folders()
}

terraform {
  source = "../../modules/app"
}

# Pobieramy dane z modułu VPC obok
dependency "vpc" {
  config_path = "../vpc"
}

# Wczytujemy nazwę środowiska z env.hcl
locals {
  env_vars = read_terragrunt_config(find_in_parent_folders("env.hcl"))
}

inputs = {
  name   = local.env_vars.locals.env_name
  vpc_id = dependency.vpc.outputs.vpc_id
}