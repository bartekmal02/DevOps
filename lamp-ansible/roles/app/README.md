# Role: app

## Description
The `app` role deploys a sample PHP application to the web server.  
It ensures the application directory exists and deploys the main PHP page that connects to the database.

## Tasks
- Create the application directory (`{{ web_dir }}`)  
- Deploy the PHP page from the template (`index.php.j2`) to the application directory

## Variables (defaults/main.yml)
- `web_dir` – path where the application files will be deployed (e.g., `/var/www/html/ansible_demo`)

## Handlers (handlers/main.yml)
- None (this role does not require service restarts; Apache restarts are handled by the `web` role)

## Templates (templates/)
- `index.php.j2` – main PHP page for the application

## Tags
- `app` – all tasks in the `app` role  
- `dev` – tasks specific to the development environment

## Notes
- Make sure the `web` and `php` roles have run before this role  
- All operations are idempotent – safe to run multiple times

## Example usage
```bash
ansible-playbook -i localhost, role_playbook.yaml -t app -e "env=dev" -c local
