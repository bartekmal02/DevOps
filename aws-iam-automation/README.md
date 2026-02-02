# AWS Infrastructure Automation

Automatyzacja infrastruktury AWS przy użyciu Python i Boto3.

## Zadanie 1: Zarządzanie IAM
Projekt implementuje zasadę **Least Privilege** oraz wzorce **SOLID**.

### Wymagania
* Python 3.x
* Skonfigurowany profil CLI: `infra-mgr`

### Użycie
* **Wdrożenie (Up):** `python3 main.py`
* **Czyszczenie (Down):** `python3 main.py --cleanup`

### Struktura
* `services/` - Logika Boto3 (krótkie metody `up`/`down`).
* `core/` - Konfiguracja i ustawienia.
* `main.py` - Punkt wejścia aplikacji.