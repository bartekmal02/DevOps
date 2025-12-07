# Role: database

## Description
The `database` role installs and configures the MySQL server.  
It creates the database and user required for the application.

## Tasks
- Install MySQL server (`mysql-server`)  
- Ensure MySQL service is running  
- Create a database (`{{ mysql_db_name }}`)  
- Create a MySQL user (`{{ mysql_user }}`) with privileges on the database

## Variables (defaults/main.yml)
- `mysql_db_name` – name of the database to create  
- `mysql_user` – MySQL user for the application  
- `mysql_password` – password for the MySQL user  
- `mysql_login_user` – user for connecting to MySQL to create DB and user  
- `mysql_login_password` – password for the login user

## Handlers (handlers/main.yml)
- None (no handlers needed for this role)

## Templates (templates/)
- None

## Tags
- `database` – all tasks in the `database` role  
- `dev` – tasks specific to the development environment

## Notes
- Ensure that the `mysql_login_user` has sufficient privileges to create databases and users  
- All operations are idempotent – safe to run multiple times

## Example usage
```bash
ansible-playbook -i localhost, role_playbook.yaml -t database -e "env=dev" -c local
