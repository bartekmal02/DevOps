import sys
import uuid
import json
import logging
from datetime import datetime, timezone  # Dodano timezone
from services.network_service import NetworkManager

# Unikalny identyfikator dla każdego uruchomienia (Correlation ID)
CORRELATION_ID = str(uuid.uuid4())

class JsonFormatter(logging.Formatter):
    """Custom formatter to output logs in JSON format as per requirements."""
    def format(self, record):
        # Poprawiona obsługa czasu UTC dla standardu ISO
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "correlation_id": CORRELATION_ID,
            "message": record.getMessage()
        }
        return json.dumps(log_entry)

def setup_logger():
    """Konfiguracja loggera z formatem JSON."""
    logger = logging.getLogger("AWS-Infra")
    logger.setLevel(logging.INFO)
    
    # Zapobieganie dublowaniu logów przy wielokrotnym wywołaniu
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
    
    return logger

def main():
    logger = setup_logger()
    
    if len(sys.argv) < 2:
        logger.error("Missing command. Usage: python main.py [up|--cleanup]")
        return

    command = sys.argv[1].lower()
    manager = NetworkManager(logger)

    try:
        if command == "up":
            logger.info("Starting 'up' command execution")
            vpc_id = manager.up()
            # Idempotentność jest zachowana wewnątrz managera
            
        elif command == "--cleanup" or command == "down":
            logger.info("Starting '--cleanup' command execution")
            manager.down()
            
        else:
            logger.warning(f"Unknown command: {command}")
            
    except Exception as e:
        # Graceful shutdown - informacja o przyczynie zgodnie z wymaganiami
        logger.error(f"Execution failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()