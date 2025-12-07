# Role: web

## Description
The `web` role installs and configures the Apache web server and enables PHP support.  
Additionally, it deploys a virtual host for the sample application.

## Tasks
- Install Apache (`apache2`)  
- Enable PHP module (`a2enmod php8.3`)  
- Deploy virtual host (`vhost.conf.j2`)

## Variables (defaults/main.yml)
- `apache_port` – port on which Apache listens (e.g., 8080)  
- Other global variables are loaded from `group_vars` (dev/staging/prod)

## Handlers (handlers/main.yml)
- `restart apache` – restarts Apache service after configuration changes

## Templates (templates/)
- `vhost.conf.j2` – Apache virtual host configuration template

## Tags
- `web` – all tasks in the `web` role  
- `dev` – tasks specific to the development environment

## Notes
- The role requires PHP to be installed first (`php` role)  
- All tasks are idempotent – the playbook can be run multiple times safely

## Example usage
```bash
ansible-playbook -i localhost, role_playbook.yaml -t web -e "env=dev" -c local
