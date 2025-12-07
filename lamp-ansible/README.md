# Ansible LAMP Project

## Overview
This project sets up a basic LAMP stack (Linux, Apache, MySQL, PHP) using Ansible with a modular, role-based structure. It supports multiple environments (`dev`, `staging`, `prod`) and follows best practices for maintainability and readability.

## Roles Overview
- **base** – Updates the system and installs basic packages  
- **web** – Installs and configures Apache, enables PHP module, deploys virtual host  
- **php** – Installs PHP and required packages (`php-mysql`, `libapache2-mod-php`)  
- **database** – Installs MySQL, ensures it is running, creates database and user for the application  
- **app** – Deploys a sample PHP application to the web directory

## Features
- Idempotent operations – safe to run multiple times  
- Environment-specific configurations (`dev`, `staging`, `prod`)  
- Host-specific variables via `host_vars/localhost.yaml`  
- Tags support for granular execution of roles or tasks  
- Handlers used for service restarts where needed  
- Modular role-based structure for easier maintenance

## Configuration
- `group_vars/<env>.yaml` – environment-specific variables (e.g., dev, staging, prod)  
- `host_vars/localhost.yaml` – host-specific variables (e.g., Apache port, DB host)  
- Defaults are defined in each role under `defaults/main.yml`  

## Running the Playbook
1. Select the environment using `-e "env=<environment>"` (e.g., `dev`, `staging`, `prod`)  
2. Run the playbook locally with administrator privileges:
```bash
ansible-playbook -i localhost, role_playbook.yaml -e "env=dev" -c local --ask-become-pass
