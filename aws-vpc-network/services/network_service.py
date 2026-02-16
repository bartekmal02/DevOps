import boto3
import settings
from botocore.exceptions import ClientError
from exceptions.network_exceptions import NetworkError, VpcCreationError

class NetworkManager:
    """
    Class responsible for managing AWS VPC infrastructure with idempotency and HA.
    Ensures network connectivity for Fargate clusters.
    """

    def __init__(self, logger):
        """Initializes the EC2 resource using settings profile and region."""
        self.session = boto3.Session(profile_name=settings.AWS_PROFILE)
        self.ec2 = self.session.resource('ec2', region_name=settings.AWS_REGION)
        self.logger = logger

    def _get_existing_vpc(self):
        """Checks if a VPC with the name fargate-vpc already exists in the region."""
        vpcs = list(self.ec2.vpcs.filter(Filters=[{'Name': 'tag:Name', 'Values': ['fargate-vpc']}]))
        return vpcs[0] if vpcs else None

    def up(self):
        """
        Provision the network infrastructure including VPC, IGW, Routing, and Subnets.
        """
        try:
            # 1. VPC Check (Idempotency)
            vpc = self._get_existing_vpc()
            if vpc:
                self.logger.info(f"VPC already exists ({vpc.id}). Skipping creation.")
            else:
                self.logger.info("Creating new VPC...")
                vpc = self.ec2.create_vpc(CidrBlock=settings.NETWORK_CONFIG['vpc_cidr'])
                vpc.wait_until_available()
                vpc.create_tags(Tags=[{"Key": "Name", "Value": "fargate-vpc"}])

            # 2. Internet Gateway (IGW)
            igws = list(vpc.internet_gateways.all())
            if not igws:
                igw = self.ec2.create_internet_gateway()
                vpc.attach_internet_gateway(InternetGatewayId=igw.id)
                self.logger.info(f"Attached IGW: {igw.id}")
            else:
                igw = igws[0]

            # 3. Routing Configuration (Crucial for Public IP access)
            main_route_table = list(vpc.route_tables.all())[0]
            routes = main_route_table.routes
            has_internet_route = any(r.destination_cidr_block == '0.0.0.0/0' for r in routes)

            if not has_internet_route:
                main_route_table.create_route(
                    DestinationCidrBlock='0.0.0.0/0',
                    GatewayId=igw.id
                )
                self.logger.info(f"Added route 0.0.0.0/0 to IGW: {igw.id}")

            # 4. Two Subnets (High Availability)
            zones = [f"{settings.AWS_REGION}a", f"{settings.AWS_REGION}b"]
            for i, az in enumerate(zones):
                cidr = f"10.0.{i+1}.0/24"
                existing = list(vpc.subnets.filter(Filters=[{'Name': 'availability-zone', 'Values': [az]}]))
                
                if not existing:
                    s = vpc.create_subnet(CidrBlock=cidr, AvailabilityZone=az)
                    s.create_tags(Tags=[{"Key": "Name", "Value": f"fargate-subnet-{az}"}])
                    self.logger.info(f"Created subnet in zone {az}")

            self.logger.info("Network infrastructure is ready and consistent.")
            return vpc.id

        except ClientError as e:
            self.logger.error(f"AWS Error: {e.response['Error']['Code']}")
            raise NetworkError(str(e))

    def down(self):
        """
        Clean up all network resources in the correct order (SG -> IGW -> Subnets -> VPC).
        """
        self.logger.info("Starting safe infrastructure removal...")
        try:
            vpc = self._get_existing_vpc()
            if not vpc:
                self.logger.info("No infrastructure found to remove.")
                return

            # 1. Usuwamy Security Groups (poza domyślną)
            for sg in vpc.security_groups.all():
                if sg.group_name != 'default':
                    self.logger.info(f"Removing Security Group: {sg.group_name} ({sg.id})")
                    sg.delete()

            # 2. Usuwamy IGW
            for igw in vpc.internet_gateways.all():
                self.logger.info(f"Detaching and removing IGW: {igw.id}")
                vpc.detach_internet_gateway(InternetGatewayId=igw.id)
                igw.delete()

            # 3. Usuwamy Subnety
            for subnet in vpc.subnets.all():
                self.logger.info(f"Removing subnet: {subnet.id}")
                subnet.delete()

            # 4. Na samym końcu VPC
            vpc_id = vpc.id
            vpc.delete()
            self.logger.info(f"VPC {vpc_id} successfully deleted.")

        except ClientError as e:
            self.logger.error(f"AWS Error during cleanup: {e}")
            raise NetworkError(f"Cleanup failed: {str(e)}")
    
    def create_security_group(self, vpc_id):
        """
        Creates a Security Group with HTTP access (port 80).
        """
        try:
            existing_groups = list(self.ec2.security_groups.filter(
                Filters=[
                    {'Name': 'group-name', 'Values': ['fargate-sg']},
                    {'Name': 'vpc-id', 'Values': [vpc_id]}
                ]
            ))
            
            if existing_groups:
                self.logger.info(f"Security Group already exists: {existing_groups[0].id}")
                return existing_groups[0].id

            sg = self.ec2.create_security_group(
                GroupName='fargate-sg',
                Description='Allow HTTP access',
                VpcId=vpc_id
            )
            
            sg.authorize_ingress(
                IpProtocol='tcp',
                FromPort=80,
                ToPort=80,
                CidrIp='0.0.0.0/0'
            )
            self.logger.info(f"Security Group created: {sg.id}")
            return sg.id
        except ClientError as e:
            self.logger.error(f"Error creating Security Group: {e}")
            raise NetworkError(str(e))