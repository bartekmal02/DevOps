# Role: base

## Description
The `base` role performs basic system setup and ensures that the server is updated.  
It is intended to prepare the environment for other roles like `web`, `php`, `database`, and `app`.

## Tasks
- Update all packages to the latest version

## Variables (defaults/main.yml)
- None required (all configuration is default system behavior)

## Handlers (handlers/main.yml)
- None (no service restarts required)

## Templates (templates/)
- None

## Tags
- `base` – all tasks in the `base` role  
- `dev` – tasks specific to the development environment

## Notes
- This role should be executed first in the playbook to ensure the system is up-to-date  
- All operations are idempotent – running multiple times will not break the system

## Example usage
```bash
ansible-playbook -i localhost, role_playbook.yaml -t base -e "env=dev" -c local

