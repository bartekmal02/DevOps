import sys
import uuid
import json
import logging
from datetime import datetime, timezone
import settings
from services.network_service import NetworkManager
from services.ecs_service import ECSManager

# Unique correlation ID for log tracing
CORRELATION_ID = str(uuid.uuid4())

class JsonFormatter(logging.Formatter):
    """Custom formatter to output logs in JSON format for better traceability."""
    def format(self, record):
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "correlation_id": CORRELATION_ID,
            "message": record.getMessage()
        }
        return json.dumps(log_entry)

def setup_logger():
    """Configure logger with JSON formatting."""
    logger = logging.getLogger("AWS-Infra")
    logger.setLevel(logging.INFO)
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
    
    # Initialize managers
    network_mgr = NetworkManager(logger)
    ecs_mgr = ECSManager(logger)

    try:
        if command == "up":
            logger.info("Starting 'up' command execution")
            
            # 1. Infrastructure Layer (Network)
            vpc_id = network_mgr.up()
            vpc = network_mgr.ec2.Vpc(vpc_id)
            subnet_ids = [s.id for s in vpc.subnets.all()]
            sg_id = network_mgr.create_security_group(vpc_id)
            
            # 2. Orchestration Layer (ECS)
            cluster_arn = ecs_mgr.create_cluster()
            task_arn = ecs_mgr.register_task_definition()
            
            # 3. Execution Layer (Service)
            ecs_mgr.create_service(cluster_arn, task_arn, subnet_ids, [sg_id])
            
            logger.info("Full deployment completed successfully")
            
        elif command in ["--cleanup", "down"]:
            logger.info("Starting full cleanup sequence")
            
            try:
                # 1. Orchestration Layer Cleanup (ECS Service first)
                # Musimy najpierw usunąć serwis, bo trzyma on interfejsy sieciowe (ENI) w VPC
                ecs_mgr.delete_service()
                
                # 2. Cluster Cleanup
                ecs_mgr.delete_cluster()
                
                # 3. Infrastructure Layer Cleanup (Network)
                # Teraz, gdy ENI są zwolnione, VPC można bezpiecznie usunąć
                network_mgr.down()
                
                logger.info("Full cleanup completed successfully")
                
            except Exception as e:
                logger.error(f"Cleanup failed: {str(e)}")
                sys.exit(1)
            
        else:
            logger.warning(f"Unknown command: {command}")
            
    except Exception as e:
        logger.error(f"Execution failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()