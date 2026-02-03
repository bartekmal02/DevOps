import boto3
from botocore.exceptions import ClientError
import settings
from exceptions.network_exceptions import NetworkError

class ECSManager:
    """Manager for AWS ECS Fargate resources providing cluster, task, and service management."""

    def __init__(self, logger):
        """Initialize ECS client using global settings."""
        self.session = boto3.Session(profile_name=settings.AWS_PROFILE)
        self.ecs = self.session.client('ecs', region_name=settings.AWS_REGION)
        self.logger = logger

    def create_cluster(self):
        """
        Creates an ECS cluster with the name defined in settings.
        This operation is idempotent.
        """
        try:
            self.logger.info(f"Initializing ECS cluster: {settings.ECS_CLUSTER_NAME}")
            response = self.ecs.create_cluster(
                clusterName=settings.ECS_CLUSTER_NAME,
                capacityProviders=['FARGATE'],
                settings=[{'name': 'containerInsights', 'value': 'enabled'}]
            )
            cluster_arn = response['cluster']['clusterArn']
            self.logger.info(f"ECS Cluster ready. ARN: {cluster_arn}")
            return cluster_arn
        except ClientError as e:
            self.logger.error(f"Error creating ECS cluster: {str(e)}")
            raise NetworkError(f"Cluster creation failed: {str(e)}")

    def register_task_definition(self):
        """
        Registers a new Fargate task definition for the application.
        Creates a new revision each time it is called.
        """
        try:
            self.logger.info(f"Registering task definition: {settings.ECS_TASK_FAMILY}")
            response = self.ecs.register_task_definition(
                family=settings.ECS_TASK_FAMILY,
                networkMode='awsvpc',
                requiresCompatibilities=['FARGATE'],
                cpu=settings.CPU_UNITS,
                memory=settings.MEMORY_LIMIT,
                containerDefinitions=[
                    {
                        'name': settings.CONTAINER_NAME,
                        'image': settings.CONTAINER_IMAGE,
                        'portMappings': [
                            {
                                'containerPort': settings.CONTAINER_PORT,
                                'hostPort': settings.CONTAINER_PORT,
                                'protocol': 'tcp'
                            }
                        ],
                        'essential': True
                    }
                ]
            )
            task_arn = response['taskDefinition']['taskDefinitionArn']
            self.logger.info(f"Task definition registered. ARN: {task_arn}")
            return task_arn
        except ClientError as e:
            self.logger.error(f"Error registering task definition: {str(e)}")
            raise NetworkError(f"Task registration failed: {str(e)}")

    def create_service(self, cluster_arn, task_arn, subnets, security_groups):
        """
        Creates or skips creation of an ECS Service based on existing services.
        Ensures the application runs with the specified network configuration.
        """
        try:
            self.logger.info(f"Ensuring ECS Service exists: {settings.ECS_SERVICE_NAME}")
            
            existing = self.ecs.list_services(cluster=settings.ECS_CLUSTER_NAME)
            if any(settings.ECS_SERVICE_NAME in arn for arn in existing.get('serviceArns', [])):
                self.logger.info(f"Service {settings.ECS_SERVICE_NAME} already exists. Skipping creation.")
                return

            response = self.ecs.create_service(
                cluster=cluster_arn,
                serviceName=settings.ECS_SERVICE_NAME,
                taskDefinition=task_arn,
                desiredCount=1,
                launchType='FARGATE',
                networkConfiguration={
                    'awsvpcConfiguration': {
                        'subnets': subnets,
                        'securityGroups': security_groups,
                        'assignPublicIp': 'ENABLED'
                    }
                }
            )
            self.logger.info(f"ECS Service created: {response['service']['serviceArn']}")
            return response['service']['serviceArn']
        except ClientError as e:
            self.logger.error(f"Error creating ECS Service: {str(e)}")
            raise NetworkError(f"Service creation failed: {str(e)}")

    def delete_service(self):
        """
        Safely deletes the ECS service by updating desired count to 0 first.
        """
        try:
            self.logger.info(f"Scaling down and deleting service: {settings.ECS_SERVICE_NAME}")
            # Najpierw ustawiamy liczbę zadań na 0, inaczej AWS nie pozwoli usunąć serwisu
            self.ecs.update_service(
                cluster=settings.ECS_CLUSTER_NAME,
                service=settings.ECS_SERVICE_NAME,
                desiredCount=0
            )
            self.ecs.delete_service(
                cluster=settings.ECS_CLUSTER_NAME,
                service=settings.ECS_SERVICE_NAME
            )
            self.logger.info("ECS Service deleted successfully.")
        except ClientError as e:
            self.logger.warning(f"Could not delete service (maybe already gone): {e}")

    def delete_cluster(self):
        """
        Removes the ECS cluster.
        """
        try:
            self.logger.info(f"Deleting cluster: {settings.ECS_CLUSTER_NAME}")
            self.ecs.delete_cluster(cluster=settings.ECS_CLUSTER_NAME)
            self.logger.info("ECS Cluster deleted successfully.")
        except ClientError as e:
            self.logger.error(f"Error deleting cluster: {e}")