import os

import boto3
from botocore.exceptions import ClientError
from logger import Logger

log = Logger(__name__)


def terminate_instance(instance_ids, region="ca-central-1"):
    log.info(f"Terminating instances: {instance_ids}")

    try:
        ec2 = boto3.client("ec2", region_name=region)
        ec2.terminate_instances(InstanceIds=instance_ids)

        log.info(f"Waiting for instances to terminate: {instance_ids}")
        waiter = ec2.get_waiter("instance_terminated")
        waiter.wait(InstanceIds=instance_ids)

        log.info(f"Instances terminated: {instance_ids}")
        return True

    except ClientError as e:
        log.error(f"Failed to terminate instances: {e}")
        return False


def delete_security_group(security_group_id, region="ca-central-1"):
    log.info(f"Deleting security group: {security_group_id}")

    try:
        ec2 = boto3.client("ec2", region_name=region)
        ec2.delete_security_group(GroupId=security_group_id)

        log.info(f"Security group deleted: {security_group_id}")
        return True

    except ClientError as e:
        log.error(f"Failed to delete security group: {e}")
        return False


def delete_route_table(route_table_id, region="ca-central-1"):
    log.info(f"Deleting route table: {route_table_id}")

    try:
        ec2 = boto3.client("ec2", region_name=region)
        ec2.delete_route_table(RouteTableId=route_table_id)

        log.info(f"Route table deleted: {route_table_id}")
        return True

    except ClientError as e:
        log.error(f"Failed to delete route table: {e}")
        return False


def delete_internet_gateway(internet_gateway_id, vpc_id, region="ca-central-1"):
    log.info(f"Deleting Internet Gateway: {internet_gateway_id}")

    try:
        ec2 = boto3.client("ec2", region_name=region)
        ec2.detach_internet_gateway(InternetGatewayId=internet_gateway_id, VpcId=vpc_id)

        log.info(f"Internet Gateway detached from VPC: {vpc_id}")

        ec2.delete_internet_gateway(InternetGatewayId=internet_gateway_id)

        log.info(f"Internet Gateway deleted: {internet_gateway_id}")
        return True

    except ClientError as e:
        log.error(f"Failed to delete Internet Gateway: {e}")
        return False


def delete_subnet(subnet_id, region="ca-central-1"):
    log.info(f"Deleting subnet: {subnet_id}")

    try:
        ec2 = boto3.client("ec2", region_name=region)
        ec2.delete_subnet(SubnetId=subnet_id)

        log.info(f"Subnet deleted: {subnet_id}")
        return True

    except ClientError as e:
        log.error(f"Failed to delete subnet: {e}")
        return False


def delete_vpc(vpc_id, region="ca-central-1"):
    log.info(f"Deleting VPC: {vpc_id}")

    try:
        ec2 = boto3.client("ec2", region_name=region)
        ec2.delete_vpc(VpcId=vpc_id)

        log.info(f"VPC deleted: {vpc_id}")
        return True

    except ClientError as e:
        log.error(f"Failed to delete VPC: {e}")
        return False


def delete_key_pair(key_name, region="ca-central-1"):
    log.info(f"Deleting key pair: {key_name}")

    try:
        ec2 = boto3.client("ec2", region_name=region)
        ec2.delete_key_pair(KeyName=key_name)

        log.info(f"Key pair deleted from AWS: {key_name}")

        pem_file = f"{key_name}.pem"
        if os.path.exists(pem_file):
            os.remove(pem_file)
            log.info(f"Local key file deleted: {pem_file}")

        return True

    except ClientError as e:
        log.error(f"Failed to delete key pair: {e}")
        return False
