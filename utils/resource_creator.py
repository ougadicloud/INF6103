import os

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


def create_security_group(
    vpc_id,
    ingress_rules=None,
    egress_rules=None,
    region="ca-central-1",
    name="default-sg",
    description="Default security group",
):
    log.info(f"Creating security group: {name}")

    try:
        ec2 = boto3.client("ec2", region_name=region)
        response = ec2.create_security_group(GroupName=name, Description=description, VpcId=vpc_id)
        sg_id = response["GroupId"]

        ec2.create_tags(Resources=[sg_id], Tags=[{"Key": "Name", "Value": name}])

        if ingress_rules:
            ec2.authorize_security_group_ingress(GroupId=sg_id, IpPermissions=ingress_rules)
            log.info(f"Ingress rules added: {len(ingress_rules)}")

        if egress_rules:
            ec2.authorize_security_group_egress(GroupId=sg_id, IpPermissions=egress_rules)
            log.info(f"Egress rules added: {len(egress_rules)}")

        log.info(f"Security group created: {sg_id}")
        return sg_id

    except ClientError as e:
        log.error(f"Failed to create security group: {e}")
        return None


def create_ec2_instance(
    subnet_id,
    security_group_id,
    region="ca-central-1",
    instance_type="t3.medium",
    key_name="lab-keypair",
    image_id="ami-0c55b159cbfafe1f0",
    name="default-instance",
    user_data=None,
    volume_size=20,
    min_count=1,
    max_count=1,
):
    log.info(f"Creating EC2 instance: {name} ({instance_type}) - Count: {min_count}")

    try:
        ec2 = boto3.client("ec2", region_name=region)
        response = ec2.run_instances(
            ImageId=image_id,
            MinCount=min_count,
            MaxCount=max_count,
            InstanceType=instance_type,
            KeyName=key_name,
            SubnetId=subnet_id,
            SecurityGroupIds=[security_group_id],
            UserData=user_data,
            BlockDeviceMappings=[
                {
                    "DeviceName": "/dev/sda1",
                    "Ebs": {"VolumeSize": volume_size, "VolumeType": "gp2", "DeleteOnTermination": True},
                }
            ],
            TagSpecifications=[{"ResourceType": "instance", "Tags": [{"Key": "Name", "Value": name}]}],
        )

        instance_ids = [inst["InstanceId"] for inst in response["Instances"]]

        log.info(f"EC2 instance(s) created: {instance_ids}")
        return instance_ids

    except ClientError as e:
        log.error(f"Failed to create EC2 instance: {e}")
        return None


def create_internet_gateway(vpc_id, region="ca-central-1", name="default-igw"):
    log.info(f"Creating Internet Gateway: {name}")

    try:
        ec2 = boto3.client("ec2", region_name=region)
        response = ec2.create_internet_gateway()
        igw_id = response["InternetGateway"]["InternetGatewayId"]

        ec2.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)

        ec2.create_tags(Resources=[igw_id], Tags=[{"Key": "Name", "Value": name}])

        log.info(f"Internet Gateway created and attached: {igw_id}")
        return igw_id

    except ClientError as e:
        log.error(f"Failed to create Internet Gateway: {e}")
        return None


def create_route_table(
    vpc_id,
    internet_gateway_id,
    region="ca-central-1",
    name="default-rt",
):
    log.info(f"Creating route table: {name}")

    try:
        ec2 = boto3.client("ec2", region_name=region)
        response = ec2.create_route_table(VpcId=vpc_id)
        route_table_id = response["RouteTable"]["RouteTableId"]

        ec2.create_tags(Resources=[route_table_id], Tags=[{"Key": "Name", "Value": name}])

        ec2.create_route(
            RouteTableId=route_table_id,
            DestinationCidrBlock="0.0.0.0/0",
            GatewayId=internet_gateway_id,
        )
        log.info("Route to Internet Gateway added")

        log.info(f"Route table created: {route_table_id}")
        return route_table_id

    except ClientError as e:
        log.error(f"Failed to create route table: {e}")
        return None


def create_key_pair(region="ca-central-1", key_name="lab-keypair"):
    log.info(f"Creating key pair: {key_name}")

    try:
        ec2 = boto3.client("ec2", region_name=region)
        response = ec2.create_key_pair(KeyName=key_name)

        with open(f"{key_name}.pem", "w") as f:
            f.write(response["KeyMaterial"])

        os.chmod(f"{key_name}.pem", 0o600)

        log.info(f"Key pair created and saved: {key_name}.pem")
        return key_name

    except ClientError as e:
        log.error(f"Failed to create key pair: {e}")
        return None


def load_user_data(file_path="tp1/user_data.tpl"):
    log.info(f"Loading user data from {file_path}")

    try:
        if not os.path.exists(file_path):
            log.error(f"User data file not found: {file_path}")
            return None

        with open(file_path, "r") as f:
            user_data = f.read()

        log.info(f"User data loaded: {len(user_data)} bytes")
        return user_data

    except OSError as e:
        log.error(f"Failed to load user data: {e}")
        return None
