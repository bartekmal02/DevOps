# AWS Infrastructure Automation - Task 2 (VPC & HA)

## 📋 Project Description
This repository contains a professional Python-based automation tool for provisioning AWS network infrastructure. The project is built with **SOLID principles**, focusing on high availability, observability, and idempotency. It serves as a foundation for serverless deployments like ECS Fargate.

## 🚀 Key Features
* **High Availability (HA):** Automated creation of a VPC with two public subnets across different Availability Zones (`eu-central-1a` and `eu-central-1b`).
* **Idempotency:** Advanced state-checking logic ensures that re-running the script won't create duplicate resources or cause errors.
* **Structured Logging (JSON):** All execution logs are output in JSON format, making them ready for professional log management systems.
* **Observability:** Each execution session is tagged with a unique **Correlation ID (UUID)** for easy tracking and debugging.
* **Safe Cleanup:** Implements a graceful `--cleanup` mechanism that respects AWS resource dependencies (Internet Gateway -> Subnets -> VPC).

## 📂 Project Structure
Zgodnie z wymaganiami projektowymi, kod został podzielony na moduły:
* `main.py` – Punkt wejścia (CLI) z implementacją loggera JSON i obsługą UUID.
* `services/` – Logika biznesowa zarządzania siecią AWS (NetworkManager).
* `exceptions/` – Katalog dedykowany dla własnych klas błędów (np. `NetworkError`).
* `settings.py` – Centralny plik konfiguracyjny (Region, Profile, CIDR).

## 🛠 Setup & Usage
1.  **Initial Setup:**
    Upewnij się, że posiadasz profil AWS o nazwie `infra-mgr` w pliku `~/.aws/credentials`.

2.  **Deploy Network:**
    ```bash
    python main.py up
    ```

3.  **Safe Cleanup:**
    ```bash
    python main.py --cleanup
    ```

## 🏗 Technical Standards
* **Language:** Wszystkie docstringi są w języku angielskim; komentarze techniczne w języku polskim.
* **Error Handling:** Wyjątki są pogrupowane w dedykowanym katalogu `exceptions`.
* **Best Practices:** Zastosowano zasady SOLID (extensible, not modifiable) oraz zasadę Least Privilege dla Security Groups.

---
*Created as part of AWS Cloud Infrastructure Tasks - 2026*