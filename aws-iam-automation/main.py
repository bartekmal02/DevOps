import sys
import uuid
import logging
from core.settings import GROUP_CONFIG, USER_ASSIGNMENTS
from services.iam_service import IAMManager

def run():
    """Główna funkcja uruchomieniowa skryptu."""
    # Unikalny identyfikator uruchomienia dla logów
    run_id = str(uuid.uuid4())
    
    # Konfiguracja loggera
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
    logger = logging.getLogger("IAM")
    
    # Inicjalizacja menedżera
    mgr = IAMManager(logger)
    
    # Sprawdzenie flagi czyszczenia
    if "--cleanup" in sys.argv:
        logger.info("Rozpoczynanie sprzątania infrastruktury...")
        mgr.down(GROUP_CONFIG.keys(), USER_ASSIGNMENTS.keys())
        logger.info("Sprzątanie zakończone.")
        return

    # Standardowe wdrożenie infrastruktury
    logger.info(f"Start Run ID: {run_id}")
    mgr.up(GROUP_CONFIG, USER_ASSIGNMENTS)
    logger.info("Wdrożenie zakończone sukcesem.")

if __name__ == "__main__":
    run()