import boto3
from botocore.exceptions import ClientError
from settings import NETWORK_CONFIG
from exceptions.network_exceptions import NetworkError, VpcCreationError

class NetworkManager:
    """Class responsible for managing AWS VPC infrastructure with idempotency and HA."""

    def __init__(self, logger):
        self.session = boto3.Session(profile_name=NETWORK_CONFIG['profile'])
        self.ec2 = self.session.resource('ec2', region_name=NETWORK_CONFIG['region'])
        self.logger = logger

    def _get_existing_vpc(self):
        """Sprawdza czy VPC o nazwie fargate-vpc już istnieje."""
        vpcs = list(self.ec2.vpcs.filter(Filters=[{'Name': 'tag:Name', 'Values': ['fargate-vpc']}]))
        return vpcs[0] if vpcs else None

    def up(self):
        """Provision network with idempotency check."""
        try:
            # 1. Sprawdzenie czy VPC istnieje (Idempotentność)
            vpc = self._get_existing_vpc()
            if vpc:
                self.logger.info(f"VPC już istnieje ({vpc.id}). Pomijam tworzenie.")
            else:
                self.logger.info("Tworzenie nowego VPC...")
                vpc = self.ec2.create_vpc(CidrBlock=NETWORK_CONFIG['vpc_cidr'])
                vpc.wait_until_available()
                vpc.create_tags(Tags=[{"Key": "Name", "Value": "fargate-vpc"}])

            # 2. Internet Gateway (IGW) - wymagane do komunikacji światem
            igws = list(vpc.internet_gateways.all())
            if not igws:
                igw = self.ec2.create_internet_gateway()
                vpc.attach_internet_gateway(InternetGatewayId=igw.id)
                self.logger.info(f"Podpięto IGW: {igw.id}")
            else:
                igw = igws[0]

            # 3. Dwa Subnety w różnych AZ (High Availability - wymaganie z PDF)
            # Używamy eu-central-1a i eu-central-1b
            zones = [f"{NETWORK_CONFIG['region']}a", f"{NETWORK_CONFIG['region']}b"]
            for i, az in enumerate(zones):
                cidr = f"10.0.{i+1}.0/24"
                existing = list(vpc.subnets.filter(Filters=[{'Name': 'availability-zone', 'Values': [az]}]))
                
                if not existing:
                    s = vpc.create_subnet(CidrBlock=cidr, AvailabilityZone=az)
                    s.create_tags(Tags=[{"Key": "Name", "Value": f"fargate-subnet-{az}"}])
                    self.logger.info(f"Utworzono subnet w strefie {az}")

            self.logger.info("Infrastruktura sieciowa jest gotowa i spójna.")
            return vpc.id

        except ClientError as e:
            self.logger.error(f"Błąd AWS: {e.response['Error']['Code']}")
            raise NetworkError(str(e))

    def down(self):
        """Clean up all network resources in correct order (IGW -> Subnets -> VPC)."""
        self.logger.info("Rozpoczynam bezpieczne usuwanie infrastruktury...")
        try:
            vpc = self._get_existing_vpc()
            if not vpc:
                self.logger.info("Nie znaleziono infrastruktury do usunięcia.")
                return

            # 1. Odpięcie i usunięcie Internet Gateway
            for igw in vpc.internet_gateways.all():
                self.logger.info(f"Odpinam i usuwam IGW: {igw.id}")
                vpc.detach_internet_gateway(InternetGatewayId=igw.id)
                igw.delete()

            # 2. Usunięcie podsieci
            for subnet in vpc.subnets.all():
                self.logger.info(f"Usuwam podsieć: {subnet.id}")
                subnet.delete()

            # 3. Usunięcie VPC
            vpc_id = vpc.id
            vpc.delete()
            self.logger.info(f"VPC {vpc_id} zostało pomyślnie usunięte.")

        except ClientError as e:
            self.logger.error(f"Błąd AWS podczas sprzątania: {e}")
            raise NetworkError(f"Cleanup failed: {str(e)}")
    
    def create_security_group(self, vpc_id):
        """Tworzy Security Group z dostępem HTTP (port 80)."""
        try:
            # Sprawdzenie czy grupa już istnieje (Idempotentność)
            existing_groups = list(self.ec2.security_groups.filter(
                Filters=[{'Name': 'group-name', 'Values': ['fargate-sg']},
                         {'Name': 'vpc-id', 'Values': [vpc_id]}]
            ))
            
            if existing_groups:
                self.logger.info(f"Security Group już istnieje: {existing_groups[0].id}")
                return existing_groups[0].id

            # Tworzenie nowej grupy
            sg = self.ec2.create_security_group(
                GroupName='fargate-sg',
                Description='Allow HTTP access',
                VpcId=vpc_id
            )
            
            # Dodanie reguły Inbound (port 80 na świat)
            sg.authorize_ingress(
                IpProtocol='tcp',
                FromPort=80,
                ToPort=80,
                CidrIp='0.0.0.0/0'
            )
            self.logger.info(f"Security Group utworzona: {sg.id}")
            return sg.id
        except ClientError as e:
            self.logger.error(f"Błąd przy tworzeniu SG: {e}")
            raise NetworkError(str(e))