# AWS Serverless Infrastructure Automation (VPC & ECS Fargate)

## 📋 Project Description
This repository contains a professional Python-based automation tool for provisioning a complete, serverless container stack on AWS. Using **Boto3**, it automates the deployment of a high-availability network and an **ECS Fargate** cluster running an Nginx web server. 

The project strictly follows **SOLID principles**, ensuring the code is extensible and maintainable. All infrastructure is designed to be **idempotent**, meaning the scripts can be run repeatedly without causing resource duplication or deployment errors.

## 🚀 Key Features
* **Infrastructure as Code (IaC):** Full automation of AWS resources using Python, replacing manual AWS Console management.
* **Networking (VPC & HA):** Automated creation of a VPC with two public subnets across different Availability Zones for high availability.
* **Compute (ECS Fargate):** Serverless container orchestration including Cluster creation, Task Definition registration, and Service management.
* **Automated Routing:** Dynamic configuration of Route Tables and Internet Gateways to ensure public connectivity.
* **Structured Logging (JSON):** Professional logging with unique **Correlation IDs (UUID)** for tracing execution across sessions.
* **Dependency-Aware Cleanup:** Intelligent destruction of resources in the correct order (Service -> Cluster -> Security Group -> Network) to avoid AWS dependency violations.

## 📂 Project Structure
Following the project requirements, the code is modularized:
* `main.py` – Entry point (CLI) with JSON logger implementation and UUID tracing.
* `services/` – Business logic for AWS resources:
    * `network_service.py` – Manages VPC, Subnets, IGW, and Security Groups.
    * `ecs_service.py` – Manages ECS Clusters, Tasks, and Fargate Services.
* `exceptions/` – Dedicated directory for custom error classes grouped by domain.
* `settings.py` – Central configuration (AWS Region, Profiles, CIDR, and Container specs).

## 🛠 Setup & Usage
1.  **Initial Setup:**
    Ensure you have an AWS profile configured (default: `infra-mgr`) in your `~/.aws/credentials`.

2.  **Deploy Full Stack:**
    ```bash
    python3 main.py up
    ```
    *This will provision the VPC, setup networking, and launch the Nginx container.*

3.  **Teardown Infrastructure:**
    ```bash
    python3 main.py down
    # or
    python3 main.py --cleanup
    ```
    *This safely removes all resources in the correct order to ensure a clean account state.*

## 🏗 Technical Standards
* **SOLID Principles:** Code is designed to be extensible but not modifiable, separating concerns between networking and orchestration.
* **Language Policy:** All docstrings are written in English; technical comments in Polish.
* **Error Handling:** Custom exceptions are grouped in the `exceptions/` directory for precise error tracking.
* **Formatting:** Clean and scannable code structure with clear separation of configuration, imports, and logic.

---
*Created as part of AWS Cloud Infrastructure Tasks - 2026*