# AWS Infrastructure via Terraform

This repository contains a professional multi-tier AWS infrastructure setup, designed for scalability and security.

## Project Architecture

The project is divided into two main logical parts:

### 1. [Backend Setup](./terraform-backend-setup)
Responsible for bootstrapping the Terraform environment.
- **S3 Bucket**: Stores the `.tfstate` files remotely.
- **DynamoDB Table**: Handles State Locking to prevent concurrent changes.
- **Security**: Includes AES256 encryption and versioning for the state file.

### 2. [Main Infrastructure](./terraform-main-project)
The core infrastructure deployed using reusable modules:
- **Networking**: Custom VPC with public and private subnets.
- **Security**: Granular Security Groups for web and database layers.
- **Database**: RDS/Database instances isolated in private subnets.
- **Compute**: EC2 instances for application hosting.

## Key Features
- **Remote State**: Fully managed remote state with locking.
- **Modular Design**: Infrastructure is broken down into clean, manageable modules.
- **Security First**: Database isolation and encrypted state management.

## Deployment Order
1. Deploy `terraform-backend-setup` to create the S3 and DynamoDB resources.
2. Update the `backend.tf` in `terraform-main-project` with the generated S3 bucket name.
3. Deploy `terraform-main-project`.
