# Terragrunt Infrastructure Project - AWS

This project demonstrates a modular AWS infrastructure setup using Terragrunt and Terraform, following a multi-region deployment model (N. Virginia and Frankfurt).

## Repository Structure

- `infrastructure/modules/` - Reusable Terraform modules (VPC, Application).
- `infrastructure/dev/` - Development environment configuration (region: us-east-1).
- `infrastructure/staging/` - Staging environment configuration (region: eu-central-1).
- `infrastructure/terragrunt.hcl` - Root configuration file managing S3 remote state and DynamoDB locking.

## Tech Stack

* **Terraform** - Infrastructure as Code (IaC) definition.
* **Terragrunt** - Orchestration tool to keep the code DRY and manage multiple environments.
* **AWS** - Cloud provider (VPC, EC2, S3 for backend, DynamoDB for state locking).

## Operational Notes (Troubleshooting)

During the infrastructure teardown (`run-all destroy`), an unexpected process interruption occurred, which led to a **State Lock** issue in DynamoDB.

**Resolution steps:**
1. Identified the specific Lock ID from the terminal error logs.
2. Manually released the lock using the command: `terragrunt force-unlock <LOCK_ID>`.
3. Completed the resource destruction step-by-step (folder by folder) to ensure proper dependency cleanup after the session
