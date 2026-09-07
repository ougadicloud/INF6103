import boto3
from botocore.exceptions import ClientError
from logger import Logger

log = Logger(__name__)


def create_vpc(region="ca-central-1", cidr_block="10.0.0.0/16", name="default-vpc"):
    log.info(f"Creating VPC: {name} ({cidr_block})")

    try:
        ec2 = boto3.client("ec2", region_name=region)
        response = ec2.create_vpc(CidrBlock=cidr_block)
        vpc_id = response["Vpc"]["VpcId"]

        ec2.create_tags(Resources=[vpc_id], Tags=[{"Key": "Name", "Value": name}])

        log.info(f"VPC created: {vpc_id}")
        return vpc_id

    except ClientError as e:
        log.error(f"Failed to create VPC: {e}")
        return None


def create_subnet(
    vpc_id,
    region="ca-central-1",
    cidr_block="10.0.1.0/24",
    availability_zone="ca-central-1a",
    name="default-subnet",
    is_public=True,
):
    log.info(f"Creating subnet: {name} ({cidr_block}) - Public: {is_public}")

    try:
        ec2 = boto3.client("ec2", region_name=region)
        response = ec2.create_subnet(VpcId=vpc_id, CidrBlock=cidr_block, AvailabilityZone=availability_zone)
        subnet_id = response["Subnet"]["SubnetId"]

        ec2.create_tags(Resources=[subnet_id], Tags=[{"Key": "Name", "Value": name}])

        log.info(f"Subnet created: {subnet_id}")
        return subnet_id

    except ClientError as e:
        log.error(f"Failed to create subnet: {e}")
        return None


def create_security_group():
    pass


def create_routing_Table():
    pass


def create_internet_gateway():
    pass


def create_ec2_instance():
    pass
