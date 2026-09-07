import os

import boto3
from botocore.exceptions import ClientError
from logger import Logger

log = Logger(__name__)


def terminate_instance(instance_id, region="ca-central-1"):
    pass


def delete_security_group(security_group_id, region="ca-central-1"):
    pass


def delete_route_table(route_table_id, region="ca-central-1"):
    pass


def delete_internet_gateway(internet_gateway_id, vpc_id, region="ca-central-1"):
    pass


def delete_subnet(subnet_id, region="ca-central-1"):
    pass


def delete_vpc(vpc_id, region="ca-central-1"):
    pass


def delete_key_pair(key_name, region="ca-central-1"):
    pass