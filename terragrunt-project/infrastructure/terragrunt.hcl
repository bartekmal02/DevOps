locals {
  env_vars    = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  region_vars = read_terragrunt_config(find_in_parent_folders("region.hcl"))

  environment = local.env_vars.locals.env_name
  aws_region  = local.region_vars.locals.aws_region
}

# Dynamiczny provider korzystający z wykrytego regionu [cite: 161, 232, 253]
generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
  region = "${local.aws_region}"
  default_tags {
    tags = {
      ManagedBy   = "Terragrunt"
      Environment = "${local.environment}"
    }
  }
}
EOF
}

# Wspólny backend dla wszystkich modułów [cite: 21, 45, 141]
remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    bucket         = "bartek-bucket-terragrunt-homework"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = "eu-central-1"
    encrypt        = true
    dynamodb_table = "terraform-lock-table"
  }
}