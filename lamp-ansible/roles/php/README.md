# Role: php

## Description
The `php` role installs PHP and required packages for the LAMP stack.  
It ensures that Apache can use PHP to run web applications and that MySQL support is available.

## Tasks
- Install PHP (`php`)  
- Install PHP MySQL module (`php-mysql`)  
- Install Apache PHP module (`libapache2-mod-php`)

## Variables (defaults/main.yml)
- No default variables are required for this role (all variables come from group_vars if needed)

## Handlers (handlers/main.yml)
- None (empty, the role does not trigger any service restarts)

## Templates (templates/)
- None

## Tags
- `php` – all tasks in the `php` role  
- `dev` – tasks specific to the development environment

## Notes
- The role must be run before deploying the application pages (`app` role)  
- All operations are idempotent – running the role multiple times will not break the system

## Example usage
```bash
ansible-playbook -i localhost, role_playbook.yaml -t php -e "env=dev" -c local
